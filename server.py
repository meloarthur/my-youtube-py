import socket
import threading
import rpyc

# Defina o endereço e a porta do servidor
host = '0.0.0.0'
port = 9999

def handle_client(client_socket):
    conn = rpyc.connect("localhost", 10000)  # Conexão com o DataManager

    request = client_socket.recv(2**20)
    request = request.decode('utf-8')

    if request.startswith("UPLOAD "):
        file_name = request[7:]
        print(f"Receiving file: {file_name}")

        done = False
        temp = b""
        while not done:
            data = client_socket.recv(2**20)
            if data[-5:] == b"<END>":
                done = True
                temp += data[:-5]
            else:
                temp += data

        conn.root.upload_file(file_name, temp)
        print(f"File '{file_name}' received and saved.")

    elif request.startswith("STREAM "):
        video_file = request[7:]
        print(f"Streaming video: {video_file}")

        video_data = conn.root.stream_file(video_file)
        if video_data:
            client_socket.sendall(video_data)
            client_socket.send(b"<END>")
        client_socket.close()
        print(f"Video '{video_file}' streamed.")

    elif request.startswith("LISTAR "):
        files_list = conn.root.list_files()
        client_socket.send(','.join(files_list).encode('utf-8'))
        client_socket.close()

    conn.close()
    

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f"Servidor escutando conexões em {host}:{port}")

while True:
    client, address = server.accept()
    print(f"Conexão de {address[0]}:{address[1]}")

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()