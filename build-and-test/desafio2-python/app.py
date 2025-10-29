from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def local():
    return jsonify({
        'message': 'Me podria usted decir que hora es?',
        'datestamp': datetime.datetime.now().isoformat(),
        'satus': 'success'
    })

@app.route('/status')
def status():
    return jsonify({
        'status': 'ok',
        'version': 1.0,
        'app_name': 'Desafio 2'
    })

@app.route('/restar/<int:a>/<int:b>')
def sub(a,b):
    return jsonify({
        'operacion': 'resta',
        'numeros': [a,b],
        'resultado': a-b
    })

@app.route('/despedida/<nombre>')
def despedida(nombre):
    return jsonify({
        'despedida': f'Goodbye {nombre}',
        'mensaje': 'Adios viejo amigo'
    })

def dividir(a,b): return a / b
def inpar(n): return n % 2 != 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)