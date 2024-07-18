import os
import threading

import spacy, spacy_ngram

from util.config import config
from util.log import log
from util.preprocessamento import PreProcessamento
from util.sql import ano_inserir, comunicacao_cientifica_inserir, excluir_dados, comunicacao_cientifica_analisar
from util.thread import processar_comunicacao_cientifica

if config("excluir_dados") is True:
    log("Excluindo Dados.")
    excluir_dados()

for ano in os.listdir(config("comunicacoes_cientificas_dir")):
    ano_id = ano_inserir(ano)
    log(f"Processando: {ano}")
    for comunicacao_cientifica in os.listdir(os.path.join(config("comunicacoes_cientificas_dir"), ano)):
        comunicacao_cientifica_id = comunicacao_cientifica_inserir(
            comunicacao_cientifica,
            ano_id,
            "Na fila"
        )
log("Iniciando as Threads de Processamento.")
nlp = spacy.load('pt_core_news_lg')
nlp.add_pipe('spacy-ngram', config={'ngrams': (1, 2, 3)})
preprocessor = PreProcessamento(
    spacy_model=PreProcessamento.load_model("pt_core_news_lg"),
    remove_numbers=True,
    remove_special=True,
    pos_to_remove=None,
    remove_stopwords=False,
    lemmatize=False
    )
for i in range(0, config("threads_quantidade")):
    threading.Thread(
        target=processar_comunicacao_cientifica,
        args=(comunicacao_cientifica_analisar(), nlp, preprocessor)
    ).start()
