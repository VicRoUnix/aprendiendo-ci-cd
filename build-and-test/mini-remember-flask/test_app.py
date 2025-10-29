import pytest
from app import app as flask_app # IMportamos nuestra 'app' desde app.py

#   1.  Que es esto? Es una "fixture" de pytest.
#       Piensa en ello como una funcion de "preparacion".
#       Antes de cada prueba, esta funcion se ejecutara.
#       Crea un "cliente de pruieba" (un navegador falso) para nosotros.
@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

#   2. NUestra primera prueba!
#       Debe emmpezar con 'test_'.
#       NOta como 'client' se pasa como argumento. pytest ve esto
#       y aitomaticamente nos da el 'client' que preparamos en la fixture.
def test_hola(client):
    #   3. Usamos el cliente para "visitar" nuestra ruta '/'
    response = client.get('/')

    #   4. Las comprobaciones!
    #   'assert' significa "asegurate de que..."
    #   Si la condicion no es verdadera, la prueba falla.

    #   Comprobacion 1: La pagina cargo correctamente? (Codigo 200 = OK)
    assert response._status_code == 200

    #   Comprobacion 2: La pagina contiene el texto que esperamos?
    #   (Usamos b'...' por que la respuesta 'data' esta en 'bytes', no en texto normal)
    assert b'HOla, mundo!' in response.data