import sqlalchemy as sqlalchemy
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.sqlite import insert as insert2


class db:

    engine = None
    conn = None
    metadata = None
    Ano = None
    ComunicacaoCientifica = None
    Ngram = None
    ComunicacaoCientificaNgram = None

    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///database.sqlite", isolation_level="AUTOCOMMIT")
        self.conn = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.Ano = sqlalchemy.Table(
            "ano",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
            sqlalchemy.Column("ano", sqlalchemy.Integer, unique=True, nullable=False)
        )
        self.ComunicacaoCientifica = sqlalchemy.Table(
            "comunicacao_cientifica",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
            sqlalchemy.Column("ano_id", sqlalchemy.Integer, ForeignKey("ano.id")),
            sqlalchemy.Column("arquivo_nome", sqlalchemy.String(1000), nullable=False),
            sqlalchemy.Column("processado", sqlalchemy.String(50), nullable=False)
        )
        self.Ngram = sqlalchemy.Table(
            "ngram",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
            sqlalchemy.Column("ngram", sqlalchemy.String(1000), nullable=False),
            sqlalchemy.Column("tipo", sqlalchemy.Integer, nullable=False),
            UniqueConstraint("ngram", sqlite_on_conflict="IGNORE")
        )
        self.ComunicacaoCientificaNgram = sqlalchemy.Table(
            "comunicacao_cientifica_ngram",
            self.metadata,
            sqlalchemy.Column(
                "comunicacao_cientifica_id",
                sqlalchemy.Integer,
                primary_key=True,
                foreign_key="comunicacao_cientifica.id"),
            sqlalchemy.Column("ngram_id", sqlalchemy.Integer, primary_key=True, foreign_key="ngram.id"),
            sqlalchemy.Column("contador", sqlalchemy.Integer, nullable=False),
            UniqueConstraint("comunicacao_cientifica_id", "ngram_id", name="uix_comunicacao_cientifica_id_ngram_id")
        )
        self.metadata.create_all(self.engine)

    def excluir_dados(self):
        self.metadata.drop_all(self.engine)
        self.metadata.create_all(self.engine)

    def executar(self, sql, tipo):
        if tipo == "sql":
            return self.conn.execute(sqlalchemy.sql.text(sql))
        elif tipo == "objeto":
            return self.conn.execute(sql)

    def ano_inserir(self, ano):
        qtde = self.executar(
            sqlalchemy.select(sqlalchemy.func.count().label("qtde")).select_from(self.Ano).where(
                self.Ano.c.ano == ano),  # type: ignore
            "objeto"
        ).first().qtde
        if qtde == 0:
            result = self.executar(sqlalchemy.insert(self.Ano).values(ano=ano), "objeto").lastrowid
        else:
            result = self.executar(
                sqlalchemy.select(self.Ano).where(
                    self.Ano.c.ano == ano),  # type: ignore
                "objeto").first().id
        return result

    def ano_selecionar(self):
        return self.executar(sqlalchemy.select(self.Ano).order_by(self.Ano.c.ano), "objeto").all()

    def ano_selecionar_um(self, ano_id):
        return self.executar(
            sqlalchemy.select(self.Ano).where(
                self.Ano.c.id == ano_id).order_by(  # type: ignore
                self.Ano.c.ano),
            "objeto").first()

    def comunicacao_cientifica_inserir(self, arquivo_nome, ano_id, processado):
        qtde = self.executar(
            sqlalchemy.select(sqlalchemy.func.count().label("qtde")).select_from(self.ComunicacaoCientifica).where(
                self.ComunicacaoCientifica.c.arquivo_nome == arquivo_nome).where(  # type: ignore
                self.ComunicacaoCientifica.c.ano_id == ano_id),
            "objeto"
        ).first().qtde
        if qtde == 0:
            result = self.executar(
                sqlalchemy.insert(self.ComunicacaoCientifica).values(
                    arquivo_nome=arquivo_nome,
                    ano_id=ano_id,
                    processado=processado),
                "objeto"
            ).lastrowid
        else:
            result = self.executar(
                sqlalchemy.select(self.ComunicacaoCientifica).where(
                    self.ComunicacaoCientifica.c.arquivo_nome == arquivo_nome).where(  # type: ignore
                    self.ComunicacaoCientifica.c.ano_id == ano_id),
                "objeto"
            ).first().id
        return result

    def comunicacao_cientifica_analisar(self):
        qtde = self.executar(
            sqlalchemy.select(sqlalchemy.func.count().label("qtde")).select_from(self.ComunicacaoCientifica).where(
                self.ComunicacaoCientifica.c.processado == "Na fila"),
            "objeto"
        ).first().qtde
        if qtde == 0:
            return False
        else:
            result = self.executar(
                sqlalchemy.select(self.ComunicacaoCientifica).where(
                    self.ComunicacaoCientifica.c.processado == "Na fila"
                ).order_by(self.ComunicacaoCientifica.c.id),
                "objeto"
            ).first()
            self.executar(
                "UPDATE comunicacao_cientifica SET processado = 'Em processamento' WHERE id = %s" % result.id,
                "sql"
            )
            return result

    def comunicacao_cientifica_analisar_finalizar(self, comunicacao_cientifica_id):
        self.executar(
            "UPDATE comunicacao_cientifica SET processado = 'Processado' WHERE id = %s" % comunicacao_cientifica_id,
            "sql"
        )

    def ngram_por_ano_selecionar(self, tipo):
        retorno = []
        cabecalho = ["ngram", "tipo"]
        sql = """
            SELECT
                n.ngram,
                n.tipo,
            """
        anos = self.ano_selecionar()
        for ano in anos:
            cabecalho.append(ano.ano)
            if tipo == "ocorrencia":
                sql += f"count(case when ano = {ano.ano} then 1 end) as '{ano.ano}',"
            elif tipo == "frequencia":
                sql += f"sum(case when ano = {ano.ano} then contador else 0 end) as '{ano.ano}',"
        if tipo == "ocorrencia":
            sql += f"count(ccn.ngram_id) as total"
        elif tipo == "frequencia":
            sql += f"sum(ccn.contador) as total"
        sql += """
            FROM ngram n
            LEFT JOIN comunicacao_cientifica_ngram ccn ON ccn.ngram_id = n.id
            LEFT JOIN comunicacao_cientifica cc ON cc.id = ccn.comunicacao_cientifica_id
            LEFT JOIN ano a ON a.id = cc.ano_id
            GROUP BY n.ngram, n.tipo
            ORDER BY total DESC
            """
        cabecalho.append("Total")
        retorno.append(cabecalho)
        dados = self.executar(sql, "sql")
        for dado in dados:
            linha = [dado.ngram, dado.tipo]
            for ano in anos:
                linha.append(getattr(dado, str(ano.ano)))
            linha.append(dado.total)
            retorno.append(linha)
        return retorno

    def ngram_inserir_multiplos(self, ngrams, tipo):
        return self.executar(sqlalchemy.insert(self.Ngram).values(
            [{"ngram": ngram, "tipo": tipo} for ngram in ngrams]), "objeto")

    def ngram_ano_selecionar(self, ano_id):
        return self.executar(
            sqlalchemy.select(
                self.Ngram.c.ngram,
                sqlalchemy.func.count().label("qtde")
            ).select_from(
                self.ComunicacaoCientificaNgram
            ).join(
                self.ComunicacaoCientifica,
                self.ComunicacaoCientifica.c.id == self.ComunicacaoCientificaNgram.c.comunicacao_cientifica_id  # type: ignore
            ).join(
                self.Ano,
                self.Ano.c.id == self.ComunicacaoCientifica.c.ano_id
            ).where(
                self.Ano.c.id == ano_id
            ).group_by(self.Ngram.c.ngram),
            "objeto"
        ).first().qtde

    def comunicacao_cientifica_ngram_inserir_multiplos(self, comunicacao_cientifica_id, ngrams):
        return self.executar(insert2(self.ComunicacaoCientificaNgram).on_conflict_do_update(
            index_elements=["comunicacao_cientifica_id", "ngram_id"],
            set_=dict(contador=self.ComunicacaoCientificaNgram.c.contador+1)
        ).values(
            [{
                "comunicacao_cientifica_id": comunicacao_cientifica_id,
                "ngram_id": self.executar(
                    sqlalchemy.select(self.Ngram).where(self.Ngram.c.ngram == ngram),  # type: ignore
                    "objeto").first().ngram_id,
                "contador": 1
            } for ngram in ngrams]), "objeto")
