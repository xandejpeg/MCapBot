from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

# Variáveis globais para controlar o estado do script
script_path = None
process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_script', methods=['POST'])
def load_script():
    global script_path, process
    script_path = request.form['script_path']
    if script_path:
        if process and process.poll() is None:
            process.terminate()
        script_path = script_path
        return jsonify({'status': f'Arquivo carregado: {os.path.basename(script_path)}'})
    return jsonify({'status': 'Falha ao carregar o arquivo'})

@app.route('/start_script', methods=['POST'])
def start_script():
    global process
    if script_path:
        if process is None or process.poll() is not None:
            process = subprocess.Popen(["python", script_path], shell=True)
            return jsonify({'status': 'Script em execução'})
    return jsonify({'status': 'Falha ao iniciar o script'})

@app.route('/stop_script', methods=['POST'])
def stop_script():
    global process
    if process and process.poll() is None:
        process.terminate()
        process = None
        return jsonify({'status': 'Nenhum script rodando'})
    return jsonify({'status': 'Falha ao parar o script'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
