import pika
import json

def callback(ch, method, properties, body):
    mensaje = json.loads(body)
    print(f"[Reservas] Pago recibido para reserva: {mensaje['reserva_id']}")

credentials = pika.PlainCredentials('user', 'password')
conexion = pika.BlockingConnection(
    pika.ConnectionParameters('rabbitmq', credentials=credentials)
)
canal = conexion.channel()
canal.queue_declare(queue='pagos_confirmados')
canal.basic_consume(queue='pagos_confirmados', on_message_callback=callback, auto_ack=True)

print('[Reservas] Esperando mensajes de pagos...')
canal.start_consuming()
