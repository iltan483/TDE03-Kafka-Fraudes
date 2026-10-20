
import json
import random
import time
import uuid
from datetime import datetime, timezone

from kafka import KafkaProducer

CIDADES = ["Macapá", "Belém", "Manaus", "São Paulo", "Brasília"]

CLIENTES = ["C001", "C002", "C003", "C004", "C005"]


def gerar_transacao():
    return {
        "id_transacao": str(uuid.uuid4()),
        "cliente_id": random.choice(CLIENTES),
        "valor": round(random.uniform(50, 15000), 2),
        "cidade": random.choice(CIDADES),
        "data_hora": datetime.now(timezone.utc).isoformat()
    }


def main():
    produtor = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda dados: json.dumps(dados).encode("utf-8")
    )

    print("Produtor iniciado. Enviando transações a cada 3 segundos...")

    try:
        while True:
            transacao = gerar_transacao()

            produtor.send("transacoes", value=transacao)
            produtor.flush()

            print(f"Transação enviada: {transacao}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nProdutor encerrado.")

    finally:
        produtor.close()


if __name__ == "__main__":
    main()
