# Pruebas de Contrato con Pact

Este proyecto implementa pruebas de contrato entre dos microservicios:
- `reservas` (consumidor)
- `pago` (proveedor)

## ¿Cómo hacer las pruebas?

1. Ejecuta el siguiente comando para levantar los contenedores Docker: `docker-compose up --build`.
2. Apagar el servicio pagos, ya que el puerto 5005 esta ocupado, y  el test fallará porque Pact no puede usarlo para levantar el servicio simulado (mock). Para apagar el servicio pagos usar: `docker-compose stop pagos`
2. Con el .venv creado en la carpeta de reservas, activarlo usando: `.\.venv\Scripts\activate`
3. En la carpeta de reservas, ejecutar: `pytest pact_tests/test_contract.py`