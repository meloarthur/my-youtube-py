from flask import Flask, render_template, request, Response, jsonify
import socket
import os

HOST = "127.0.0.1"
PORT = 8080

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    header = f"UPLOAD {file_name} "
    header_formatted = f"{header: <1024}"
    print(header_formatted)
    client.send(header_formatted.encode())
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
    header = f"STREAM {video_name} "
    client.send(f"{header: <1024}".encode())
    
    def generate(client):
        chunk_size = 4096
        while True:
            data = client.recv(chunk_size)
            if not data:
                break
            yield data
        client.close()
    return Response(generate(client), content_type='video/mp4')

@app.route('/list-videos')
def list_videos():
    video_folder = 'C:/Users/Arthur/Documents/my-youtube-py/videos/'
    video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f)) and f.endswith(".mp4")]
    return jsonify(video_files)

if __name__ == '__main__':
    app.run(debug=True, port=5000)