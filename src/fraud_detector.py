
from collections import defaultdict
from datetime import datetime


class DetectorFraudes:
    def __init__(self):
        self.historico = defaultdict(list)

    def analisar(self, transacao):
        cliente = transacao["cliente_id"]
        cidade = transacao["cidade"]
        valor = float(transacao["valor"])

        momento = datetime.fromisoformat(transacao["data_hora"])
        fraudes = []

        # Regra 1: transação de valor alto
        if valor >= 10000:
            fraudes.append("ALTO_VALOR")

        historico_cliente = self.historico[cliente]

        # Regra 2: quatro transações em menos de 60 segundos
        recentes_60s = [
            item for item in historico_cliente
            if 0 <= (momento - item["momento"]).total_seconds() < 60
        ]

        if len(recentes_60s) + 1 >= 4:
            fraudes.append("TEMPO_60s")

        # Regra 3: transações em cidades diferentes em até 10 minutos
        recentes_10m = [
            item for item in historico_cliente
            if 0 <= (momento - item["momento"]).total_seconds() <= 600
        ]

        if any(item["cidade"] != cidade for item in recentes_10m):
            fraudes.append("GEO_10m")

        # Registra a transação para analisar as próximas
        historico_cliente.append({
            "momento": momento,
            "cidade": cidade
        })

        # Mantém somente o histórico relevante para as regras
        self.historico[cliente] = [
            item for item in historico_cliente
            if 0 <= (momento - item["momento"]).total_seconds() <= 600
        ]

        return fraudes
