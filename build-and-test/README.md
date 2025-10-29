# Build & Test automaticos con Github Actions
* Como construir y testear una aplicacion automaticamente cada vez que se realiza un cambio. Se preparara una app en Python con Flask, escribirle tests, y crear un workflow que la pruebe solo.

---

## 1.Crearemos una app python simple
* He realizado un remember para aprender los conceptos que se utilizaran en esta app y poder comprender que es lo que se realizara en el ejercicio esta todo en `mini-remember-flask`
* Ahora crearemos la carpeta para realizar la actividad.
```bash
mkdir app-python
cd app-python
mkdir tests
touch app.py requirements.txt tests/test_app.py
```
## 2.Desarrollamos la app.py
```py
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Perfecto que tengas un buen dia!',
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'success'
    })
        
    
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'uptime': 'running'})

@app.route('/suma/<int:a>/<int:b>')
def suma(a, b):
    return jsonify({
        'operacion': 'suma',
        'numeros': [a, b],
        'resultado': a + b
    })

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return jsonify({
        'saludo': f'¡Hola {nombre}!',
        'mensaje': 'Bienvenido a mi aplicación'
    })

# Funciones para test
def multiplicar(a, b): return a * b
def es_par(n): return n % 2 == 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 2. Agregar las dependencias en requirements.txt
```txt
Flask==2.3.3
pytest==7.4.3
pytest-cov==4.1.0
pytest-flask==1.2.0
```
---

## 3.Escribir los tests
```py
import pytest, json
from app import app, multiplicar, es_par

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    r = client.get('/')
    data = json.loads(r.data)
    assert r.status_code == 200
    assert data['status'] == 'success'

def test_health(client):
    r = client.get('/health')
    assert json.loads(r.data)['status'] == 'healthy'

def test_suma(client):
    r = client.get('/suma/3/4')
    assert json.loads(r.data)['resultado'] == 7

def test_saludo(client):
    r = client.get('/saludo/DevBro')
    assert '¡Hola DevBro!' in r.get_data(as_text=True)

def test_multiplicar(): assert multiplicar(2, 3) == 6
def test_es_par(): assert es_par(4)
```

---

## 4.Hacer el Workflow de CI 
```bash
nano .github/worksflows/ci-python.yml
```
```yml
name: CI Básico Python

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Configurar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Instalar dependencias
      run: |
        pip install -r requirements.txt

    - name: Ejecutar tests
      run: |
        pytest tests/ -v

    - name: Ejecutar con cobertura
      run: |
        pytest --cov=app --cov-report=term --cov-report=html

    - name: Guardar reporte
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report
        path: htmlcov/
```
* Este paso cojee la accion preconfigurada del markeetplace de github actions para instalar python dentro de la maquina ubuntu donde se le dira que queremos la version 3.11  
  * Name: Configurar Python
  * Uses: Actions/set-up python@v4
  * with: python-version:3.11
* Instalaremos las dependencias flask y pytest en la maquina ubuntu, para realizar las pruebas automaticas con el archivo requirements.txt
  * pip install -r requirements.txt
* Ejecuta el comando pytest para realizar las pruebas pertineentes de nuestra aplicacion python flask, en el directorio dentro de tests y -v de verbose para que aparezca el prodecimiento 
  * pytest tests/ -v
* En este paso le esta diciendo a pytest una serie de pasos
  * Quiero que cuando ejecutes los test de mientras me midas cuantas lineas de codigo del modulo/paquete app estan siendo probadas
    * pytest --cov=app
  * Muestrame un resumen de la cobertura en la terminal(log de github actions)
    * --cov-report=term
  * Generame un reporte mas detallado en fomrato html creando una nueva carpeta llamada htmlcov/
    * --cov-report=html
* En el ultimo paso usa la accion upload-artifact para guardar los archivos generados en el workflow
  * name: coverage-report: Nombre del archivo descargable
  * path: htmlcov/ Es la carpeta donde tiene que subir el reporte
  


---

## 5.Multiples versiones de Python
```bash
nano .github/worksflows/ci-matrix-py.yml
```
```yml
name: CI Python Matrix

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-matrix:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - run: pip install -r requirements.txt
    - run: pytest tests/ -v

    - name: Verificar app corriendo
      run: |
        timeout 10 python app.py &
        sleep 5
        curl -f http://localhost:5000/health
```
* Cuando dice strategy, matrix, le estamos dando 3 versiones de python , de las cualees va ejecutar las pruebas en todas estas 3 versiones.

---

# Desafio del Dia

* 1.Crea tu app en Flask
* 2.Escribir al menos 5 tests.
* 3.Crear el workflow `ci-python-desf.yml`
* 4.Ejecutarlo en GitHub.
* 5.Probar el matrix CI


