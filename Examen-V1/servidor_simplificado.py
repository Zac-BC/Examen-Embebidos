from flask import Flask, jsonify
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
ESP32_IP = "http://192.168.100.184"

# Configurar reintentos para las solicitudes HTTP
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

@app.route('/status', methods=['GET'])
def get_status():
    try:
        print("Enviando solicitud de estado al ESP32")
        response = session.get(f"{ESP32_IP}/status", timeout=10)
        response.raise_for_status()
        print("Solicitud de estado exitosa")
        print("Respuesta del ESP32:", response.json())
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/toggle', methods=['GET'])
def toggle_led():
    try:
        print("Enviando solicitud de alternar al ESP32")
        response = session.get(f"{ESP32_IP}/toggle", timeout=10)
        response.raise_for_status()
        print("Solicitud de alternar exitosa")
        return response.text, 200
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
