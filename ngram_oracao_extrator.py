import os
import threading

import util
from sql import ano_inserir, comunicacao_cientifica_inserir, excluir_dados, comunicacao_cientifica_analisar
from thread import processar_comunicacao_cientifica

if util.get_config("excluir_dados") is True:
    util.log("Excluindo Dados.")
    excluir_dados()

for ano in os.listdir(util.get_config("comunicacoes_cientificas_dir")):
    ano_id = ano_inserir(ano)
    util.log(f"Processando: {ano}")
    for comunicacao_cientifica in os.listdir(os.path.join(util.get_config("comunicacoes_cientificas_dir"), ano)):
        comunicacao_cientifica_id = comunicacao_cientifica_inserir(
            comunicacao_cientifica,
            ano_id,
            "Na fila"
        )
util.log("Iniciando as Threads de Processamento.")
for i in range(0, util.get_config("threads_quantidade")):
    threading.Thread(target=processar_comunicacao_cientifica, args=(comunicacao_cientifica_analisar(),)).start()
