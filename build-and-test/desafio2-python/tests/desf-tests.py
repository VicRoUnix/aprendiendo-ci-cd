import pytest, json
from desafio2 import desafio2, dividir, inpar

@pytest.fixture
def client():
    desafio2.config['TESTING'] = True
    with desafio2.test_client() as client:
        yield client

def test_local(client):
    r = client.get('/')
    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['status'] == 'success'

def test_status(client):
    r = client.get('/status')
    assert json.loads(r.data)['status'] == 'ok'

def test_restar(client):
    r = client.get('/restar/8/4')
    assert json.loads(r.data)['resultado'] == 4

def test_despedida(client):
    r = client.get('/despedida/amigo')
    assert '¡Goodbye amigo!' in r.get_data(as_text=True)

def test_dividir(): assert dividir(10, 2) == 5
def test_inpar(): assert inpar(7)