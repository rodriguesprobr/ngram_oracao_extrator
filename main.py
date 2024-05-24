import fnmatch
import os
from datetime import datetime

import spacy
from spacy_ngram import NgramComponent

comunicacoes_cientificas_dir = "data/comunicacoes_cientificas"
comunicacoes_cientificas_csv = "data/dados_tratados.csv"
remocoes = ["\t", "\r", "\n", "  "]


def log(mensagem):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}")


def limpar(texto):
    for remocao in remocoes:
        while texto.find(remocao) != -1:
            texto = texto.replace(remocao, " ")
    return texto.strip().lower()


nlp = spacy.load('pt_core_news_lg')
nlp.add_pipe('spacy-ngram')
dados_tratados = open(file=comunicacoes_cientificas_csv, mode="w", encoding="utf-8")
dados_tratados.write("ANO\tARQUIVO\tCORPUS\n")
for ano in os.listdir(comunicacoes_cientificas_dir):
    log(f"Processando: {ano}")
    for comunicacao_cientifica in os.listdir(os.path.join(comunicacoes_cientificas_dir, ano)):
        log(f"- {comunicacao_cientifica}")
        # Se o nome de arquivo possui a extensão txt, processa
        if fnmatch.fnmatch(comunicacao_cientifica, '*.txt'):
            conteudo = limpar(open(os.path.join(comunicacoes_cientificas_dir, ano, comunicacao_cientifica), "r", encoding="UTF-8").read())
            dados_tratados.write(f"{ano}\t{comunicacao_cientifica}\t{conteudo}\n")
            doc = nlp(conteudo)
            unigram = doc._.ngram_1
            bigram = doc._.ngram_2
            trigram = doc._.ngram_3


dados_tratados.close()
