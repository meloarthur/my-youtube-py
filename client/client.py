from flask import Flask, render_template, request, Response, jsonify
import socket

HOST = "192.168.0.121"
PORT = 9999

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    print(file_name)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    client.send(f"UPLOAD {file_name}".encode())

    data = file.read()
    client.sendall(data)
    client.send(b"<END>")
    client.close()
    
    return "Upload realizado com sucesso!"

@app.route('/stream')
def stream():
    video_name = request.args.get('id')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    header = f"STREAM {video_name} ".encode()
    client.send(header)
    
    def generate(client):
        chunk_size = 2**20
        while True:
            data = client.recv(chunk_size)
            if not data:
                break
            yield data
        client.close()
    return Response(generate(client), content_type='video/mp4')

@app.route('/list-videos', methods=['GET', 'POST'])
def list_videos():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.send(f"LISTAR ".encode())  # Use the "STREAM" request format
    # Receba a lista de nomes de arquivo do servidor
    data = client.recv(2**20).decode('utf-8')
    nomes_arquivos = data.split(',')

    client.close()
    return jsonify(nomes_arquivos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)