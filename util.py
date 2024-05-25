from datetime import datetime


def log(mensagem):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}")


def limpar(texto, remocoes):
    for remocao in remocoes:
        while texto.find(remocao) != -1:
            texto = texto.replace(remocao, " ")
    return texto.strip().lower()
