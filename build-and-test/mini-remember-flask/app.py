#   1. Importamos la "herramienta" principal de Flask
from flask import Flask

#   2. Creamos nuestra aplicacion web.
#       '__name__' es una variable especial de Python que le dice a Flask
#       donde encontrar los archivos de este proyecto.
app = Flask(__name__)

#   3. Definimos una "ruta" (una URL).
#       El '@' se llama "decorador". Esto le dice a Flask:
#       "Oye, si alguien visita la pagina principal ('/'), ejecuta la funcion que esta justo debajo"
@app.route('/')
def hola_mundo():
    #   4. Esta es la funcion que se ejecuta.
    #       Simplemente devuelve el texto que queremos mostrar en el navegador.
    return '!HOla, mundo!'

#   5. (Opcional pero recomendado para pruebas locales)
#       Esta seccion solo se ejecuta si corremos ela archivo directamente
#       con 'python app.py'. NO se ejecutara en un servidor de produccion.
if  __name__ == '__main__':
    app.run(debug=True) # 'debug=True' reinicia el servidor automaticamente con cada cambio.
