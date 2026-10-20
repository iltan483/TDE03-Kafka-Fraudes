
import json

from kafka import KafkaConsumer

from database import criar_tabela, salvar_transacao
from fraud_detector import DetectorFraudes


def main():
    criar_tabela()
    detector = DetectorFraudes()

    consumidor = KafkaConsumer(
        "transacoes",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="detector-fraudes",
        value_deserializer=lambda mensagem: json.loads(
            mensagem.decode("utf-8")
        )
    )

    print("Consumidor iniciado. Aguardando transações...")

    try:
        for mensagem in consumidor:
            transacao = mensagem.value
            fraudes = detector.analisar(transacao)

            salvar_transacao(transacao, fraudes)

            print("\n--- Transação recebida ---")
            print(f"ID: {transacao['id_transacao']}")
            print(f"Cliente: {transacao['cliente_id']}")
            print(f"Valor: R$ {transacao['valor']:.2f}")
            print(f"Cidade: {transacao['cidade']}")
            print(f"Data/hora: {transacao['data_hora']}")

            if fraudes:
                print(f"ALERTA DE FRAUDE: {', '.join(fraudes)}")
            else:
                print("Resultado: nenhuma regra de fraude identificada")

    except KeyboardInterrupt:
        print("\nConsumidor encerrado.")

    finally:
        consumidor.close()


if __name__ == "__main__":
    main()
