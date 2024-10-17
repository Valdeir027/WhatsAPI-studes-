from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/message', methods=['POST','GET'])
def create_message():
    if request.method == 'POST':
        # json_data = request.json
        data = request.json
        print(f"{data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]}: {data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]}")

        return jsonify({'veify_token': f'hohr6w6SpX'}), 201
    else:
        # Para o método GET, obtenha os parâmetros de consulta
        query_params = request.args  # Obtém os parâmetros de consulta
        print("Parâmetros de consulta:", query_params)

        # Você pode acessar parâmetros individuais assim:
        hub_mode = query_params.get('hub.mode')
        hub_challenge = query_params.get('hub.challenge')
        hub_verify_token = query_params.get('hub.verify_token')

        print("hub.mode:", hub_mode)
        print("hub.challenge:", hub_challenge)
        print("hub.verify_token:", hub_verify_token)
        
        return hub_challenge




if __name__ == '__main__':
    app.run(debug=False)