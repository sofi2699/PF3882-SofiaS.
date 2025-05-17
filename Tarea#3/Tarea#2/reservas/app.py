from flask import Flask, jsonify, request
from flasgger import Swagger
from datetime import datetime

app = Flask(__name__)
swagger = Swagger(app)

# Base de datos simulada
reservas = []
disponibilidad = {}

@app.route('/reservas', methods=['POST'])
def crear_reserva():
    """
    Crear una nueva reserva
    ---
    parameters:
      - name: reserva
        in: body
        required: true
        schema:
          id: Reserva
          required:
            - usuario
            - vehiculo
            - fecha_hora
          properties:
            usuario:
              type: string
            vehiculo:
              type: string
              description: Placa del carro
            fecha_hora:
              type: string
              format: date-time
    responses:
      201:
        description: Reserva creada exitosamente
      400:
        description: Fecha ya reservada
    """
    data = request.get_json()
    fecha = data["fecha_hora"]

    if fecha in disponibilidad:
        return jsonify({"error": "La fecha ya está reservada"}), 400

    reserva = {
        "id": len(reservas) + 1,
        "usuario": data["usuario"],
        "vehiculo": data["vehiculo"],
        "fecha_hora": fecha
    }

    reservas.append(reserva)
    disponibilidad[fecha] = True
    return jsonify(reserva), 201


@app.route('/reservas', methods=['GET'])
def listar_reservas():
    """
    Listar todas las reservas
    ---
    responses:
      200:
        description: Lista de reservas
    """
    return jsonify(reservas), 200


@app.route('/reservas/<int:reserva_id>', methods=['PUT'])
def modificar_reserva(reserva_id):
    """
    Modificar una reserva existente
    ---
    parameters:
      - name: reserva_id
        in: path
        type: integer
        required: true
      - name: datos
        in: body
        required: true
        schema:
          id: ModificarReserva
          properties:
            fecha_hora:
              type: string
              format: date-time
    responses:
      200:
        description: Reserva modificada
      404:
        description: Reserva no encontrada
    """
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            nueva_fecha = request.get_json().get("fecha_hora")
            if nueva_fecha in disponibilidad:
                return jsonify({"error": "La nueva fecha ya está reservada"}), 400

            disponibilidad.pop(reserva["fecha_hora"], None)
            disponibilidad[nueva_fecha] = True
            reserva["fecha_hora"] = nueva_fecha
            return jsonify(reserva), 200

    return jsonify({"error": "Reserva no encontrada"}), 404


@app.route('/reservas/<int:reserva_id>', methods=['DELETE'])
def cancelar_reserva(reserva_id):
    """
    Cancelar una reserva
    ---
    parameters:
      - name: reserva_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Reserva cancelada
      404:
        description: Reserva no encontrada
    """
    global reservas
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            disponibilidad.pop(reserva["fecha_hora"], None)
            reservas = [r for r in reservas if r["id"] != reserva_id]
            return jsonify({"mensaje": "Reserva cancelada"}), 200

    return jsonify({"error": "Reserva no encontrada"}), 404


@app.route('/disponibilidad', methods=['GET'])
def consultar_disponibilidad():
    """
    Consultar disponibilidad por fecha y hora
    ---
    parameters:
      - name: fecha_hora
        in: query
        type: string
        required: true
    responses:
      200:
        description: Disponibilidad
    """
    fecha = request.args.get("fecha_hora")
    disponible = fecha not in disponibilidad
    return jsonify({"fecha_hora": fecha, "disponible": disponible}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5005)
