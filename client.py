from flask import Flask, render_template, request, Response, jsonify
import rpyc
from env import CHUNK_SIZE
HOST = "192.168.0.121"
PORT = 9999

app = Flask(__name__)
connection = rpyc.connect_by_service('DATANODE_MANAGER')
connection._config['sync_request_timeout'] = None
datanode_manager = connection.root

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    def file_reader(file):
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            yield chunk
    
    file = request.files['file']
    file_name = file.filename
    file_generator = file_reader(file)
    datanode_manager.upload_file(file_name, file_generator)
    return "Upload realizado com sucesso!"

@app.route('/stream')
def stream():
    video_id = request.args.get('id')
    file_generator = datanode_manager.stream_file(video_id)
    return Response(file_generator, content_type='video/mp4')

@app.route('/list-videos', methods=['GET', 'POST'])
def list_videos():
    list_videos = datanode_manager.list_files()
    print(list_videos)
    return jsonify(list_videos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)