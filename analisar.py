from util import log

from sql import ngram_por_ano_selecionar

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