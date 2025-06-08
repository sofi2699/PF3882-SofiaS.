import atexit
import requests
from pact import Consumer, Provider

# Pact setup
pact = Consumer('ServicioReservas').has_pact_with(
    Provider('ServicioPago'),
    port=5005,
    log_dir='./logs',
    pact_dir='./pacts'
)

@atexit.register
def cleanup():
    pact.stop_service()

def test_confirmar_pago():
    expected_body = {
        "reserva_id": "abc123",
        "estado": "pagado"
    }

    (pact
     .given("Reserva pendiente")
     .upon_receiving("una solicitud de confirmación de pago")
     .with_request(
         method="POST",
         path="/pagos/confirmar",
         headers={"Content-Type": "application/json"},
         body=expected_body
     )
     .will_respond_with(
         status=200,
         body={"mensaje": "Pago confirmado"}
     ))

    with pact:
        response = requests.post("http://localhost:5005/pagos/confirmar", json=expected_body)
        assert response.status_code == 200
        assert response.json()["mensaje"] == "Pago confirmado"
