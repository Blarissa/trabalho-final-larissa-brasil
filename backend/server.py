from flask import Flask, request, jsonify, send_from_directory # type: ignore
from flask_cors import CORS
from conversor_er import ConversorER
import os

app = Flask(__name__)
CORS(app)

conversor = ConversorER()
afn_atual = None

@app.route('/')
def index():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

# Serve arquivos estáticos da pasta frontend
@app.route('/<path:path>')
def serve_static(path):
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, path)

@app.route('/api/converter', methods=['POST'])
def converter():
    global afn_atual
    try:
        data = request.json
        expressao = data.get('expressao', '')
        
        if not expressao:
            return jsonify({'erro': 'Expressão vazia'}), 400
        
        # Converte ER para AFN
        afn_atual = conversor.converter(expressao)
        
        # Formata resposta
        estados = [str(e) for e in afn_atual.estados]
        alfabeto = list(afn_atual.alfabeto)
        estado_inicial = str(afn_atual.estado_inicial)
        estados_finais = [str(e) for e in afn_atual.estados_finais]
        
        transicoes = []
        for (origem, simbolo), destinos in afn_atual.transicoes.items():
            for destino in destinos:
                transicoes.append({
                    'origem': str(origem),
                    'simbolo': simbolo,
                    'destino': str(destino)
                })
        
        return jsonify({
            'estados': sorted(estados, key=lambda x: x),
            'alfabeto': sorted(alfabeto),
            'estadoInicial': estado_inicial,
            'estadosFinais': sorted(estados_finais, key=lambda x: x),
            'transicoes': transicoes
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/reconhecer', methods=['POST'])
def reconhecer():
    global afn_atual
    try:
        if afn_atual is None:
            return jsonify({'erro': 'Nenhum AFN foi criado ainda'}), 400
        
        data = request.json
        cadeia = data.get('cadeia', '')
        
        aceita = afn_atual.reconhecer(cadeia)
        
        return jsonify({'aceita': aceita})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)