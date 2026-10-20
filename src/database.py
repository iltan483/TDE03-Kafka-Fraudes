
import json
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "transacoes.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id_transacao TEXT PRIMARY KEY,
                cliente_id TEXT NOT NULL,
                valor REAL NOT NULL,
                cidade TEXT NOT NULL,
                data_hora TEXT NOT NULL,
                fraudes TEXT NOT NULL
            )
        """)


def salvar_transacao(transacao, fraudes):
    with conectar() as conexao:
        conexao.execute("""
            INSERT OR IGNORE INTO transacoes
            (id_transacao, cliente_id, valor, cidade, data_hora, fraudes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            transacao["id_transacao"],
            transacao["cliente_id"],
            transacao["valor"],
            transacao["cidade"],
            transacao["data_hora"],
            json.dumps(fraudes, ensure_ascii=False)
        ))
