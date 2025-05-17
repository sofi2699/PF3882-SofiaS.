from flask import Flask, jsonify
from flasgger import Swagger
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)

swagger_template = {
    "info": {
        "title": "API de Productos y Servicios",
        "version": "1.0",
        "description": "Para gestionar productos y servicios relacionados con el lavado de vehículos.",
        "contact": {
            "responsibleOrganization": "LavaCar Pro S.A.",
            "responsibleDeveloper": "Sofia",
            "email": "sofia@ejemplo.com",
            "url": "https://www.ejemplo.com",
        },
    }
}
swagger = Swagger(app, template=swagger_template)

# Datos acerca de los productos y servicios.
productos_servicios = [
    {"id": 1, "nombre": "Carwash Sencillo", "descripcion": "Lavado básico interior y exterior del vehículo", "precio": 10000},
    {"id": 2, "nombre": "Carwash Premium", "descripcion": "Lavado interior y exterior, limpieza de chasis y motor con pulido profesional", "precio": 15000},
    {"id": 3, "nombre": "Lavado de Tapicería", "descripcion": "Lavado profundo de asientos, alfombras y superficies textiles", "precio": 18000},
    {"id": 4, "nombre": "Champú y Cera", "descripcion": "Aplicación de champú especial para carrocería y encerado con cera líquida", "precio": 12000},
    {"id": 5, "nombre": "Aromatización", "descripcion": "Aplicación de ambientador personalizado (vainilla, pino, cítricos, etc.)", "precio": 5000},
    {"id": 6, "nombre": "Lavado de Asientos", "descripcion": "Limpieza profunda únicamente de los asientos", "precio": 14000},
    {"id": 7, "nombre": "Encerado Profesional", "descripcion": "Pulido y protección de pintura con cera de alta gama", "precio": 20000},
    {"id": 8, "nombre": "Lavado de Motor", "descripcion": "Limpieza cuidadosa del motor con productos no corrosivos", "precio": 10000},
]

@app.route('/productos_servicios', methods=['GET'])
def get_productos_servicios():
    """
    Obtener todos los productos y servicios disponibles
    ---
    responses:
      200:
        description: Lista de productos y servicios
    """
    app.logger.info("Retornando lista de todos los productos y servicios con tamaño: %d", len(productos_servicios))
    return jsonify(productos_servicios), 200

@app.route('/productos_servicios/<int:producto_id>', methods=['GET'])
def get_producto_servicio(producto_id):
    """
    Obtener producto o servicio por ID
    ---
    parameters:
      - name: producto_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Producto o servicio encontrado
        schema:
          id: Producto
          properties:
            id:
              type: integer
            nombre:
              type: string
            descripcion:
              type: string
            precio:
              type: number
              format: float
      404:
        description: Producto o servicio no encontrado
        schema:
          id: Error
          properties:
            error:
              type: string
    """
    producto = find_producto_servicio(producto_id)
    if producto:
        app.logger.info("Producto con id %d encontrado", producto_id)
        return jsonify(producto), 200
    app.logger.info("Producto con id %d NO encontrado", producto_id)
    return jsonify({"error": "Producto no encontrado"}), 404

def find_producto_servicio(producto_id):
    # Buscar en la lista de productos y servicios
    for producto in productos_servicios:
        if producto["id"] == producto_id:
            return producto
    return None

if __name__ == '__main__':
    app.run(debug=True, port=5003)
