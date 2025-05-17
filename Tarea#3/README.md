# Prueba de Comunicación Asíncrona con RabbitMQ

Esta tarea implementa la comunicación asíncrona entre dos microservicios (`pago.py` y `reservas.py`) usando RabbitMQ.

---

## ¿Cómo probar la mensajería?

1. Ejecuta el siguiente comando para levantar los contenedores Docker: `docker-compose up --build`.
2. En el navegador, abra la documentación Swagger del servicio de pagos: `http://localhost:5005/apidocs`.
3. Desde la interfaz de Swagger, usa el método POST en /pagar y completa el JSON con datos de ejemplo:
json :
{
  "reserva_id": "123",
  "monto": 5000
}
4. Envie la solicitud y verifique que el servicio de reservas reciba el mensaje en la consola del contenedor correspondiente.