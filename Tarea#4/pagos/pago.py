import pika
import json
from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/pagar', methods=['POST'])
def procesar_pago():
    """
    Procesar un pago y enviar un mensaje a RabbitMQ
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            reserva_id:
              type: string
            monto:
              type: number
          required:
            - reserva_id
            - monto
    responses:
      200:
        description: Pago procesado
      400:
        description: Datos incompletos
    """
    datos_pago = request.get_json()
    if datos_pago.get('reserva_id') and datos_pago.get('monto'):
        enviar_mensaje_pago(datos_pago)
        return jsonify({"mensaje": "Pago procesado y mensaje enviado"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

def enviar_mensaje_pago(datos):
    credentials = pika.PlainCredentials('user', 'password')
    conexion = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', credentials=credentials)
    )
    canal = conexion.channel()
    canal.queue_declare(queue='pagos_confirmados')
    canal.basic_publish(exchange='', routing_key='pagos_confirmados',
                        body=json.dumps(datos))
    conexion.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

@app.route('/pagos/confirmar', methods=['POST'])
def confirmar_pago():
    """
    Confirmar el estado de un pago (usado en pruebas de contrato)
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            reserva_id:
              type: string
            estado:
              type: string
        required:
          - reserva_id
          - estado
    responses:
      200:
        description: Pago confirmado
      400:
        description: Datos inválidos
    """
    datos_pago = request.get_json()
    if datos_pago.get('reserva_id') and datos_pago.get('estado') == 'pagado':
        return jsonify({"mensaje": "Pago confirmado"}), 200
    else:
        return jsonify({"error": "Datos inválidos"}), 400
