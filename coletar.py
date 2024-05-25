import fnmatch
import os

import spacy
from sql import ano_inserir, comunicacao_cientifica_inserir, ngram_inserir, comunicacao_cientifica_ngram_inserir, \
    excluir_dados, ngram_por_ano_selecionar
from util import log, limpar

coletar = input("Deseja coletar e processar os dados? (S/N) ")
if coletar.lower().strip() in ["sim", "s"]:
    excluir = input("Deseja excluir dados anteriores? (S/N) ")
    if coletar.lower().strip() in ["sim", "s"]:
        excluir_dados()
    comunicacoes_cientificas_dir = "dados/comunicacoes_cientificas"
    nlp = spacy.load('pt_core_news_lg')
    nlp.add_pipe('spacy-ngram', config={'ngrams': (1, 2, 3)})
    for ano in os.listdir(comunicacoes_cientificas_dir):
        ano_id = ano_inserir(ano)
        log(f"Processando: {ano}")
        for comunicacao_cientifica in os.listdir(os.path.join(comunicacoes_cientificas_dir, ano)):
            comunicacao_cientifica_id = comunicacao_cientifica_inserir(comunicacao_cientifica, ano_id)
            log(f"- {comunicacao_cientifica}")
            # Se o nome de arquivo possui a extensão txt, processa
            if fnmatch.fnmatch(comunicacao_cientifica, '*.txt'):
                conteudo = limpar(
                    open(os.path.join(comunicacoes_cientificas_dir, ano, comunicacao_cientifica), "r", encoding="UTF-8").read(),
                    ["\t", "\r", "\n", "  "]
                )
                doc = nlp(conteudo)
                unigrams = doc._.ngram_1
                for unigram in unigrams:
                    unigram_id = ngram_inserir(unigram, 1)
                    comunicacao_cientifica_ngram_inserir(comunicacao_cientifica_id, unigram_id)
                bigrams = doc._.ngram_2
                for bigram in bigrams:
                    bigram_id = ngram_inserir(bigram, 2)
                    comunicacao_cientifica_ngram_inserir(comunicacao_cientifica_id, bigram_id)
                trigrams = doc._.ngram_3
                for trigram in trigrams:
                    trigram_id = ngram_inserir(trigram, 3)
                    comunicacao_cientifica_ngram_inserir(comunicacao_cientifica_id, trigram_id)
    log("Fim da Coleta e do Processamento.")
analisar = input("Deseja analisar os dados? (S/N) ")
if analisar.lower().strip() in ["sim", "s"]:
    log("- N-gramas por Ano")
    csv = open("dados/analise_ngram_por_ano.csv", "w", encoding="UTF-8")
    dados = ngram_por_ano_selecionar()
    for dado in dados:
        csv.write(''.join(str(f"{x}\t") for x in dado) + "\n")
    csv.close()
    log("Fim da Análise.")
log("Finalizado.")
