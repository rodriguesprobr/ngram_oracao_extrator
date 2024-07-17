from datetime import datetime


class log:
    def imprime(self, mensagem):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}")
