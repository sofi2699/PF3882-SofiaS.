from flask import Flask, jsonify, request
from flasgger import Swagger
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)

# Swagger UI
swagger_template = {
    "info": {
        "title": "API de Clientes",
        "version": "1.0",
        "description": "API para gestionar clientes en el sistema de lavado de vehículos.",
        "contact": {
            "responsibleOrganization": "LavaCar Pro S.A.",
            "responsibleDeveloper": "Sofía Sánchez",
            "email": "sofia@ejemplo.com",
            "url": "https://www.ejemplo.com",
        },
    }
}
swagger = Swagger(app, template=swagger_template)

# Base de datos simulada de clientes
clientes = [
    {"id": 1, "nombre": "Juan Pérez", "telefono": "8888-8888", "correo": "juanp@example.com", "vehiculos": []},
    {"id": 2, "nombre": "María López", "telefono": "8777-7777", "correo": "marial@example.com", "vehiculos": []},
    {"id": 3, "nombre": "Carlos Jiménez", "telefono": "8666-6666", "correo": "carlosj@example.com", "vehiculos": []},
    {"id": 4, "nombre": "Maria Mata", "telefono": "8789-6666", "correo": "mariam@example.com", "vehiculos": []},
    {"id": 5, "nombre": "Mateo Pérez", "telefono": "8899-9658", "correo": "mateopj@example.com", "vehiculos": []},
    {"id": 6, "nombre": "Sofia Mora", "telefono": "8125-7845", "correo": "sofiam@example.com", "vehiculos": []},
    {"id": 7, "nombre": "Marco Quesada", "telefono": "8745-8963", "correo": "marcoq@example.com", "vehiculos": []},
    {"id": 8, "nombre": "Natalia Quesada", "telefono": "8745-2546", "correo": "nataliaq@example.com", "vehiculos": []},
    {"id": 9, "nombre": "Lucia Murillo", "telefono": "8789-5698", "correo": "luciamj@example.com", "vehiculos": []},
    {"id":10, "nombre": "Andres Mendez", "telefono": "8636-8975", "correo": "andresm@example.com", "vehiculos": []},
]

@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    """
    Obtener todos los clientes
    ---
    responses:
      200:
        description: Lista de clientes
    """
    app.logger.info("Retornando lista de clientes: %d", len(clientes))
    return jsonify(clientes), 200

@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def obtener_cliente_por_id(cliente_id):
    """
    Obtener cliente por ID
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cliente encontrado
        schema:
          id: Cliente
          properties:
            id:
              type: integer
            nombre:
              type: string
            telefono:
              type: string
            correo:
              type: string
      404:
        description: Cliente no encontrado
        schema:
          id: Error
          properties:
            error:
              type: string
    """
    cliente = find_cliente(cliente_id)
    if cliente:
        app.logger.info("Cliente con id %d encontrado", cliente_id)
        return jsonify(cliente), 200
    app.logger.warning("Cliente con id %d no encontrado", cliente_id)
    return jsonify({"error": "Cliente no encontrado"}), 404

def find_cliente(cliente_id):
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return None

@app.route('/clientes/<int:cliente_id>/vehiculos', methods=['POST'])
def agregar_vehiculo(cliente_id):
    """
    Agregar un nuevo vehículo al cliente
    ---
    parameters:
      - name: cliente_id
        in: path
        type: integer
        required: true
      - name: vehiculo
        in: body
        required: true
        schema:
          id: Vehiculo
          required:
            - placa
            - marca
            - modelo
            - anio
          properties:
            placa:
              type: string
            marca:
              type: string
            modelo:
              type: string
            anio:
              type: integer
    responses:
      200:
        description: Vehículo agregado correctamente
      404:
        description: Cliente no encontrado
    """
    cliente = find_cliente(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    vehiculo = request.get_json()
    cliente["vehiculos"].append(vehiculo)
    return jsonify(cliente), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004)
