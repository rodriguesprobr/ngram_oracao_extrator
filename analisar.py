from util.log import log

from util.sql import ngram_por_ano_selecionar

log("- N-gramas por Ano")
csv = open("dados/analise_ngram_por_ano.csv", "w", encoding="UTF-8")
dados = ngram_por_ano_selecionar()
for dado in dados:
    csv.write(''.join(str(f"{x}\t") for x in dado) + "\n")
csv.close()
log("Fim da Análise.")
