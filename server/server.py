import socket
import os
import mimetypes
import time

# Defina o endereço e a porta do servidor
host = '127.0.0.1'  # Substitua pelo endereço do servidor
port = 8080
path = 'C:/Users/Arthur/Documents/my-youtube-py/videos/'
def detect_mimetype(filename):
    # Detecta o tipo MIME do arquivo com base na extensão do arquivo
    return mimetypes.guess_type(filename)[0]

def upload_file(client, filename):
    try:
        with open(path + filename, 'wb') as file:
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                file.write(chunk)
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def serve_file(client, filename):
    try:
        with open(path + filename, 'rb') as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                client.send(chunk)
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

def handle_request(client, address):
    request = client.recv(1024)
    header = request.decode('utf-8')
    method, filename = header.split()
    if(not method or not filename): return
    if method == 'STREAM':
        if os.path.exists(path + filename):
            serve_file(client, filename)
        else:
            response = "ERROR"
            client.send(response.encode())
    elif method == 'UPLOAD':
        print('LETS UPLOAD')
        upload_file(client, filename)
    

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Servidor socket em execução em {host}:{port}")

    while True:
        client, address = server.accept()
        print(f"Conexão de {address[0]}:{address[1]}")

        # Lide com a solicitação em uma nova thread para lidar com várias conexões
        handle_request(client, address)
        client.close()