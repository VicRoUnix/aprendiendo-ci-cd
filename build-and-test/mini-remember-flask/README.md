# Guía: De 0 a "Hola, Mundo" con Flask y Pruebas

Este documento explica, paso a paso, cómo crear una aplicación web "Hola, mundo" usando el *micro-framework* de Python llamado Flask, y cómo crear una prueba automatizada simple para verificar que funciona.

## ¿Qué vamos a hacer?

1.  **Configurar el Entorno**: Crear un espacio de trabajo limpio.
2.  **Crear la Aplicación Flask**: Escribir el código Python para nuestro servidor web.
3.  **Probarla Manualmente**: Verificar que podemos ver "Hola, mundo" en el navegador.
4.  **Escribir una Prueba Automatizada**: Crear un script que verifique la app por nosotros.
5.  **Ejecutar la Prueba**: Correr la prueba usando `pytest`.

---

## Paso 1: Configurar el Entorno

Primero, necesitamos organizar nuestros archivos.

1.  **Crea una carpeta para tu proyecto:**
    ```bash
    mkdir mi-proyecto-flask
    cd mi-proyecto-flask
    ```

2.  **Crea un "Entorno Virtual" (¡Muy recomendado!):**
    Un entorno virtual es como una "burbuja" que aísla las librerías de este proyecto de las de otros proyectos.

    ```bash
    # 'venv' es el nombre de la carpeta de la burbuja
    python3 -m venv venv
    ```

3.  **Activa el Entorno Virtual:**
    Debes hacer esto cada vez que empieces a trabajar en el proyecto.

    ```bash
    # En Linux o macOS
    source venv/bin/activate
    
    # (Si estuvieras en Windows, usarías: venv\Scripts\activate)
    ```

    (Verás que tu terminal ahora muestra `(venv)` al principio de la línea).

4.  **Instala las librerías necesarias (Flask y Pytest):**
    `Flask` es el framework web. `pytest` es la librería para ejecutar pruebas.

    ```bash
    pip install Flask pytest
    ```

¡Nuestro entorno está listo!

---

## Paso 2: Crear la Aplicación Flask (`app.py`)

Ahora, vamos a crear el servidor web.

Crea un archivo llamado `app.py` y pon el siguiente código en él:

```python
# app.py

# 1. Importamos la clase 'Flask' desde la librería 'flask'
from flask import Flask

# 2. Creamos una "instancia" de la aplicación.
#    '__name__' es una variable especial de Python que ayuda a Flask
#    a saber dónde encontrar otros archivos (como plantillas).
app = Flask(__name__)

# 3. Definimos una "ruta".
#    '@app.route("/")' es un "decorador". Le dice a Flask:
#    "Oye, si alguien visita la página principal ('/')...
@app.route("/")
def hola_mundo():
    # 4. "...ejecuta esta función y devuelve el resultado."
    return "¡Hola, mundo!"

# 5. Esta línea (opcional pero recomendada para desarrollo)
#    permite ejecutar la app directamente con 'python app.py'.
if __name__ == '__main__':
    app.run(debug=True)
```

**Explicación del Código:**

* **`from flask import Flask`**: Trae la herramienta principal de Flask.
* **`app = Flask(__name__)`**: Crea nuestra aplicación web.
* **`@app.route("/")`**: Define una URL. `/` es la página de inicio (ej. `http://localhost:5000/`).
* **`def hola_mundo():`**: La función de Python que se ejecuta cuando alguien visita esa URL.
* **`return "¡Hola, mundo!"`**: El contenido (HTML/texto) que se envía de vuelta al navegador.

---

## Paso 3: Probar Manualmente la Aplicación

Vamos a ver si funciona.

1.  **Ejecuta la aplicación:**
    En tu terminal (asegúrate de que el entorno virtual `(venv)` esté activo), escribe:

    ```bash
    flask run
    ```
    (O también `python app.py`, si incluiste las últimas líneas).

2.  **Mira la salida:**
    Verás algo como esto, que te indica que el servidor está funcionando:

    ```
     * Running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    (Press CTRL+C to quit)
    ```

3.  **Abre tu navegador:**
    Visita la dirección `http://127.0.0.1:5000/` (o `http://localhost:5000/`).

4.  **Verifica:**
    ¡Deberías ver el texto "¡Hola, mundo!" en tu navegador!

5.  **Detén el servidor:**
    Vuelve a la terminal y presiona `CTRL + C`.

¡Felicidades! Ya tienes una aplicación web funcional.

---

## Paso 4: Escribir una Prueba Automatizada (`test_app.py`)

Probar manualmente está bien, pero es lento y repetitivo. Vamos a automatizarlo.

Crea un segundo archivo en la **misma carpeta**, llámalo `test_app.py`.

```python
# test_app.py

import pytest
from app import app as flask_app # Importamos nuestra 'app' desde app.py

# 1. ¿Qué es esto? Es una "Fixture" de Pytest.
#    Una "fixture" es una función que prepara algo para nuestras pruebas.
#    Esta función 'client' crea una versión de nuestra app
#    especial para hacer pruebas (un "cliente de prueba").
@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

# 2. ¡Nuestra prueba!
#    El nombre de la función DEBE empezar con 'test_'.
#    Nota que pedimos 'client' como argumento. Pytest verá el nombre
#    y automáticamente ejecutará la fixture de arriba.
def test_hola(client):

    # 3. Usamos el cliente para "visitar" nuestra ruta '/'
    #    Esto simula a un navegador pidiendo la página.
    response = client.get('/')

    # 4. Las comprobaciones!
    #    'assert' significa "asegúrate de que..."
    #    Si la condición no es verdadera, la prueba falla.

    # Comprobación 1: ¿La página cargó correctamente? (Código 200 = OK)
    assert response.status_code == 200

    # Comprobación 2: ¿La página contiene el texto que esperamos?
    #    Usamos b'...' porque la respuesta viene en 'bytes'.
    assert b'Hola, mundo!' in response.data
```

**Explicación del Código:**

* **`from app import app as flask_app`**: Importamos la variable `app` que creamos en `app.py`. Le cambiamos el nombre a `flask_app` para evitar confusiones.
* **`@pytest.fixture`**: Define una función de "preparación".
* **`client()`**: Esta función activa el `TESTING` (modo de prueba) de Flask y nos da un `test_client`. Este cliente nos permite hacer peticiones GET/POST falsas sin necesidad de un navegador.
* **`def test_hola(client):`**: Esta es la prueba real. `pytest` le pasa automáticamente el `client` de la fixture.
* **`response = client.get('/')`**: Simulamos una visita a la página de inicio.
* **`assert response.status_code == 200`**: Verificamos que la página respondió con "OK".
* **`assert b'¡Hola, mundo!' in response.data`**: Verificamos que el contenido de la página (los `data`) incluye nuestro saludo.

---

## Paso 5: Ejecutar la Prueba Automatizada

Ahora, la magia.

1.  Asegúrate de que tu servidor Flask **NO** esté corriendo (presiona `CTRL+C` si lo está). No lo necesitamos para las pruebas.
2.  En tu terminal (con `(venv)` activo), simplemente ejecuta:

    ```bash
    pytest
    ```

3.  **Analiza el resultado:**
    `pytest` buscará automáticamente cualquier archivo llamado `test_...` o `..._test.py` y ejecutará cualquier función llamada `test_...` dentro de él.

    Si todo salió bien, verás una salida en verde que termina así:

    ```
    ================== 1 passed in 0.05s ==================
    ```

¡Eso es todo! Acabas de probar automáticamente que tu aplicación funciona. Si en el futuro cambias el texto en `app.py` (por ej., a "Adiós, mundo"), esta prueba fallará y te avisará *antes* de que subas el error.