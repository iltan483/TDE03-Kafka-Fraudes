import unittest
from datetime import datetime, timedelta, timezone

from src.fraud_detector import DetectorFraudes


class TesteDetectorFraudes(unittest.TestCase):
    def criar_transacao(self, cliente, valor, cidade, segundos):
        momento = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)
        momento += timedelta(seconds=segundos)

        return {
            "id_transacao": f"TX-{cliente}-{segundos}",
            "cliente_id": cliente,
            "valor": valor,
            "cidade": cidade,
            "data_hora": momento.isoformat()
        }

    def test_alto_valor(self):
        detector = DetectorFraudes()
        transacao = self.criar_transacao("C001", 10000, "Macapá", 0)

        fraudes = detector.analisar(transacao)

        self.assertIn("ALTO_VALOR", fraudes)

    def test_quatro_transacoes_em_menos_de_60_segundos(self):
        detector = DetectorFraudes()

        for segundos in [0, 10, 20]:
            transacao = self.criar_transacao(
                "C002", 100, "Macapá", segundos
            )
            detector.analisar(transacao)

        quarta = self.criar_transacao("C002", 100, "Macapá", 30)
        fraudes = detector.analisar(quarta)

        self.assertIn("TEMPO_60s", fraudes)

    def test_transacoes_em_cidades_diferentes(self):
        detector = DetectorFraudes()

        primeira = self.criar_transacao("C003", 100, "Macapá", 0)
        segunda = self.criar_transacao("C003", 100, "Belém", 300)

        detector.analisar(primeira)
        fraudes = detector.analisar(segunda)

        self.assertIn("GEO_10m", fraudes)


if __name__ == "__main__":
    unittest.main()
