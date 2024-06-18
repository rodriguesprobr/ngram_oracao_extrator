import fnmatch
import os

import spacy, spacy_ngram

import util
from preprocessamento import PreProcessamento
from sql import ngram_inserir, comunicacao_cientifica_ngram_inserir, comunicacao_cientifica_analisar, ano_selecionar_um, \
    comunicacao_cientifica_analisar_finalizar


def processar_comunicacao_cientifica(comunicacao_cientifica):
    ano = ano_selecionar_um(comunicacao_cientifica.ano_id)
    util.log(f"Processando - Ano {ano.ano} - Comunicação Científica {comunicacao_cientifica.arquivo_nome}")
    # conteudo = limpar(
    #     open(os.path.join(comunicacoes_cientificas_dir, ano, comunicacao_cientifica), "r", encoding="UTF-8").read(),
    #     ["\t", "\r", "\n", "  "]
    # )
    nlp = spacy.load('pt_core_news_lg')
    nlp.add_pipe('spacy-ngram', config={'ngrams': (1, 2, 3)})
    spacy_model = PreProcessamento.load_model("pt_core_news_lg")
    preprocessor = PreProcessamento(
        spacy_model=spacy_model,
        remove_numbers=True,
        remove_special=True,
        pos_to_remove=None,
        remove_stopwords=False,
        lemmatize=False
    )
    conteudo = preprocessor.preprocess_text(
        open(
            os.path.join(util.get_config("comunicacoes_cientificas_dir"), str(ano.ano), comunicacao_cientifica.arquivo_nome),
            "r",
            encoding="UTF-8"
        ).read()
    )
    doc = nlp(conteudo)
    unigrams = doc._.ngram_1
    for unigram in unigrams:
        unigram_id = ngram_inserir(unigram, 1)
        comunicacao_cientifica_ngram_inserir(comunicacao_cientifica.id, unigram_id)
    bigrams = doc._.ngram_2
    for bigram in bigrams:
        bigram_id = ngram_inserir(bigram, 2)
        comunicacao_cientifica_ngram_inserir(comunicacao_cientifica.id, bigram_id)
    trigrams = doc._.ngram_3
    for trigram in trigrams:
        trigram_id = ngram_inserir(trigram, 3)
        comunicacao_cientifica_ngram_inserir(comunicacao_cientifica.id, trigram_id)
    comunicacao_cientifica_analisar_finalizar(comunicacao_cientifica.id)
    util.log(f"Término - Ano {ano.ano} - Comunicação Científica {comunicacao_cientifica.arquivo_nome}")
    comunicacao_cientifica_thread = comunicacao_cientifica_analisar()
    if comunicacao_cientifica_thread is not False:
        processar_comunicacao_cientifica(comunicacao_cientifica_thread)
