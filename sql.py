import sqlalchemy as db
from sqlalchemy import ForeignKey

engine = db.create_engine("sqlite:///database.sqlite", isolation_level="AUTOCOMMIT")
conn = engine.connect()
metadata = db.MetaData()

Ano = db.Table(
    "ano",
    metadata,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("ano", db.Integer, unique=True, nullable=False)
)
ComunicacaoCientifica = db.Table(
    "comunicacao_cientifica",
    metadata,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("ano_id", db.Integer, ForeignKey("ano.id")),
    db.Column("arquivo_nome", db.String(1000), nullable=False),
    db.Column("processado", db.String(50), nullable=False)
)
Ngram = db.Table(
    "ngram",
    metadata,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("ngram", db.String(1000), nullable=False),
    db.Column("tipo", db.Integer, nullable=False)
)
ComunicacaoCientificaNgram = db.Table(
    "comunicacao_cientifica_ngram",
    metadata,
    db.Column("comunicacao_cientifica_id", db.Integer, primary_key=True, foreign_key="comunicacao_cientifica.id"),
    db.Column("ngram_id", db.Integer, primary_key=True, foreign_key="ngram.id")
)
metadata.create_all(engine)


def excluir_dados():
    metadata.drop_all(engine)
    metadata.create_all(engine)


def executar(sql):
    return conn.execute(db.sql.text(sql))


def ano_inserir(ano):
    qtde = conn.execute(
        db.select(db.func.count().label("qtde")).select_from(Ano).where(Ano.c.ano == ano)
    ).first().qtde
    if qtde == 0:
        result = conn.execute(db.insert(Ano).values(ano=ano)).lastrowid
        # conn.commit()
    else:
        result = conn.execute(
            db.select(Ano).where(Ano.c.ano == ano)).first().id
    return result


def ano_selecionar():
    return conn.execute(
        db.select(Ano).order_by(Ano.c.ano)
    ).all()


def ano_selecionar_um(ano_id):
    return conn.execute(
        db.select(Ano).where(Ano.c.id == ano_id).order_by(Ano.c.ano)
    ).first()


def comunicacao_cientifica_inserir(arquivo_nome, ano_id, processado):
    qtde = conn.execute(
        db.select(db.func.count().label("qtde")).select_from(ComunicacaoCientifica).where(
            ComunicacaoCientifica.c.arquivo_nome == arquivo_nome).where(ComunicacaoCientifica.c.ano_id == ano_id)
    ).first().qtde
    if qtde == 0:
        result = conn.execute(db.insert(ComunicacaoCientifica).values(
            arquivo_nome=arquivo_nome,
            ano_id=ano_id,
            processado=processado)
        ).lastrowid
        # conn.commit()
    else:
        result = conn.execute(
            db.select(ComunicacaoCientifica).where(ComunicacaoCientifica.c.arquivo_nome == arquivo_nome).where(
                ComunicacaoCientifica.c.ano_id == ano_id)).first().id
    return result


def comunicacao_cientifica_analisar():
    qtde = conn.execute(
        db.select(db.func.count().label("qtde")).select_from(ComunicacaoCientifica).where(
            ComunicacaoCientifica.c.processado == "Na fila")
    ).first().qtde
    if qtde == 0:
        return False
    else:
        result = conn.execute(
            db.select(ComunicacaoCientifica).where(
                ComunicacaoCientifica.c.processado == "Na fila"
            ).order_by(ComunicacaoCientifica.c.id)).first()
        conn.execute(
            db.sql.text("UPDATE comunicacao_cientifica SET processado = 'Em processamento' WHERE id = %s" % result.id)
        )
        # conn.commit()
        return result


def comunicacao_cientifica_analisar_finalizar(comunicacao_cientifica_id):
    conn.execute(
        db.sql.text("UPDATE comunicacao_cientifica SET processado = 'Processado' WHERE id = %s" % comunicacao_cientifica_id)
    )
    # conn.commit()


def ngram_por_ano_selecionar():
    retorno = []
    cabecalho = ["ngram", "tipo"]
    sql = """
        SELECT
            n.ngram,
            n.tipo,
        """
    anos = ano_selecionar()
    for ano in anos:
        cabecalho.append(ano.ano)
        sql += f"count(case when ano = {ano.ano} then 1 end) as '{ano.ano}',"
    sql += """
            count(ccn.ngram_id) as total
        FROM ngram n
        LEFT JOIN comunicacao_cientifica_ngram ccn ON ccn.ngram_id = n.id
        LEFT JOIN comunicacao_cientifica cc ON cc.id = ccn.comunicacao_cientifica_id
        LEFT JOIN ano a ON a.id = cc.ano_id
        GROUP BY n.ngram, n.tipo
        ORDER BY total DESC
        """
    cabecalho.append("Total")
    retorno.append(cabecalho)
    dados = executar(sql)
    for dado in dados:
        linha = [dado.ngram, dado.tipo]
        for ano in anos:
            linha.append(getattr(dado, str(ano.ano)))
        linha.append(dado.total)
        retorno.append(linha)
    return retorno


def ngram_inserir(ngram, tipo):
    qtde = conn.execute(
        db.select(db.func.count().label("qtde")).select_from(Ngram).where(Ngram.c.ngram == ngram).where(
            Ngram.c.tipo == tipo)
    ).first().qtde
    if qtde == 0:
        result = conn.execute(db.insert(Ngram).values(ngram=ngram, tipo=tipo)).lastrowid
        # conn.commit()
    else:
        result = conn.execute(db.select(Ngram).where(Ngram.c.ngram == ngram).where(Ngram.c.tipo == tipo)).first().id
    return result


def ngram_por_ano_selecionar():
    retorno = []
    cabecalho = ["ngram", "tipo"]
    sql = """
        SELECT
            n.ngram,
            n.tipo,
        """
    anos = ano_selecionar()
    for ano in anos:
        cabecalho.append(ano.ano)
        sql += f"count(case when ano = {ano.ano} then 1 end) as '{ano.ano}',"
    sql += """
            count(ccn.ngram_id) as total
        FROM ngram n
        LEFT JOIN comunicacao_cientifica_ngram ccn ON ccn.ngram_id = n.id
        LEFT JOIN comunicacao_cientifica cc ON cc.id = ccn.comunicacao_cientifica_id
        LEFT JOIN ano a ON a.id = cc.ano_id
        GROUP BY n.ngram, n.tipo
        ORDER BY total DESC
        """
    cabecalho.append("Total")
    retorno.append(cabecalho)
    dados = executar(sql)
    for dado in dados:
        linha = [dado.ngram, dado.tipo]
        for ano in anos:
            linha.append(getattr(dado, str(ano.ano)))
        linha.append(dado.total)
        retorno.append(linha)
    return retorno


def ngram_ano_selecionar(ano_id):
    return conn.execute(
        db.select(
            Ngram.c.ngram,
            db.func.count().label("qtde")
        ).select_from(
            ComunicacaoCientificaNgram
        ).join(
            ComunicacaoCientifica,
            ComunicacaoCientifica.c.id == ComunicacaoCientificaNgram.c.comunicacao_cientifica_id
        ).join(
            Ano,
            Ano.c.id == ComunicacaoCientifica.c.ano_id
        ).where(
            Ano.c.id == ano_id
        ).group_by(Ngram.c.ngram)
    ).first().qtde


def comunicacao_cientifica_ngram_inserir(comunicacao_cientifica_id, ngram_id):
    qtde = conn.execute(
        db.select(db.func.count().label("qtde")).select_from(ComunicacaoCientificaNgram).where(
            ComunicacaoCientificaNgram.c.comunicacao_cientifica_id == comunicacao_cientifica_id).where(
            ComunicacaoCientificaNgram.c.ngram_id == ngram_id)
    ).first().qtde
    if qtde == 0:
        result = conn.execute(
            db.insert(ComunicacaoCientificaNgram).values(comunicacao_cientifica_id=comunicacao_cientifica_id,
                                                         ngram_id=ngram_id)).lastrowid
        # conn.commit()
    else:
        result = conn.execute(db.select(ComunicacaoCientificaNgram).where(
            ComunicacaoCientificaNgram.c.comunicacao_cientifica_id == comunicacao_cientifica_id).where(
            ComunicacaoCientificaNgram.c.ngram_id == ngram_id)).first()
    return result
