import os
import threading
from concurrent.futures import ThreadPoolExecutor

import spacy
import spacy_ngram

from util.config import config
from util.db import db
from util.log import log
from util.preprocessamento import PreProcessamento


class processamento:
    config = None
    instancia = None
    logger = None
    nlp = None
    threads = {}

    def __init__(self):
        self.instancia = db()
        self.logger = log()
        self.nlp = spacy.load('pt_core_news_lg')
        self.nlp.add_pipe('spacy-ngram', config={'ngrams': (1, 2, 3)})
        self.config = config()
        if self.config.recuperar("excluir_dados") is True:
            self.excluir_dados()

    def excluir_dados(self):
        self.logger.imprime("Excluindo Dados.")
        self.instancia.excluir_dados()

    def processar(self):
        for ano in os.listdir(self.config.recuperar("local_comunicacoes_cientificas")):
            ano_id = self.instancia.ano_inserir(ano)
            self.logger.imprime(f"Processando: {ano}")
            for comunicacao_cientifica in os.listdir(
                    os.path.join(self.config.recuperar("local_comunicacoes_cientificas"), ano)):
                self.instancia.comunicacao_cientifica_inserir(
                    comunicacao_cientifica,
                    ano_id,
                    "Na fila"
                )
        self.iniciar_threads()

    def iniciar_threads(self):
        self.logger.imprime("Iniciando as Threads de Processamento.")
        with ThreadPoolExecutor() as e:
            futures = []
            for i in range(0, self.config.recuperar("threads_quantidade")):
                futures.append(e.submit(
                    self.processar_comunicacao_cientifica,
                    self.instancia.comunicacao_cientifica_analisar(),
                    self.nlp,
                    PreProcessamento(
                        spacy_model=PreProcessamento.load_model("pt_core_news_lg"),
                        remove_numbers=True,
                        remove_special=True,
                        remove_hyperlinks=True,
                        pos_to_remove=None,
                        remove_stopwords=False,
                        lemmatize=False
                    )
                ))
        self.logger.imprime("Término das Threads de Processamento.")
        self.logger.imprime("Iniciando as Threads de Análise.")
        with ThreadPoolExecutor() as e:
            e.submit(self.ngram_ocorrencia_por_ano())
            e.submit(self.ngram_frequencia_por_ano())
        self.logger.imprime("Término das Threads de Análise.")

    def processar_comunicacao_cientifica(self, comunicacao_cientifica, nlp, preprocessor):
        if comunicacao_cientifica is not False:
            ano = self.instancia.ano_selecionar_um(comunicacao_cientifica.ano_id)
            self.logger.imprime(f"Thread {threading.get_ident()} - Processando - "
                                f"Ano {ano.ano} - Comunicação Científica {comunicacao_cientifica.arquivo_nome}")
            conteudo = preprocessor.preprocess_text(
                open(
                    os.path.join(
                        self.config.recuperar("local_comunicacoes_cientificas"),
                        str(ano.ano),
                        comunicacao_cientifica.arquivo_nome),
                    "r",
                    encoding="UTF-8"
                ).read()
            )
            doc = nlp(conteudo)
            unigramas = doc._.ngram_1
            self.instancia.ngram_inserir_multiplos(unigramas, 1)
            bigramas = doc._.ngram_2
            self.instancia.ngram_inserir_multiplos(bigramas, 2)
            trigramas = doc._.ngram_3
            self.instancia.ngram_inserir_multiplos(trigramas, 3)
            multigramas = {'unigramas': unigramas, 'bigramas': bigramas, 'trigramas': trigramas}
            for ngramas in multigramas:
                self.instancia.comunicacao_cientifica_ngram_inserir_multiplos(
                    comunicacao_cientifica.id, multigramas[ngramas])
            self.instancia.comunicacao_cientifica_analisar_finalizar(comunicacao_cientifica.id)
            self.logger.imprime(f"Thread {threading.get_ident()} - Término - "
                                f"Ano {ano.ano} - Comunicação Científica {comunicacao_cientifica.arquivo_nome}")
            comunicacao_cientifica = self.instancia.comunicacao_cientifica_analisar()
            if comunicacao_cientifica is not False:
                self.processar_comunicacao_cientifica(comunicacao_cientifica, nlp, preprocessor)
        else:
            self.logger.imprime(f"Thread {threading.get_ident()} - Não há dados a serem processados pela Thread.")

    def ngram_frequencia_por_ano(self):
        self.logger.imprime("- Frequência de N-gramas por Ano")
        csv = open(self.config.recuperar("local_analise_ngram_frequencia_por_ano"), "w", encoding="UTF-8")
        dados = self.instancia.ngram_por_ano_selecionar("frequencia")
        for dado in dados:
            csv.write(''.join(str(f"{x}\t") for x in dado) + "\n")
        csv.close()

    def ngram_ocorrencia_por_ano(self):
        self.logger.imprime("- Ocorrência de N-gramas por Ano")
        csv = open(self.config.recuperar("local_analise_ngram_ocorrencia_por_ano"), "w", encoding="UTF-8")
        dados = self.instancia.ngram_por_ano_selecionar("ocorrencia")
        for dado in dados:
            csv.write(''.join(str(f"{x}\t") for x in dado) + "\n")
        csv.close()
