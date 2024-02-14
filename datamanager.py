import rpyc
from rpyc.utils.server import ThreadedServer
import os
import random

class DataNodeManagerService(rpyc.Service):
    def __init__(self):
        self.datanode_list = []
        self.load_datanodes()
        self.index_file = "index.txt"
        self.ensure_index_file()
        self.index = self.load_index()

    def load_datanodes(self):
        with open('database.txt', 'r') as datanode_file:
            for line in datanode_file.readlines():
                ip, port = line.strip().split(' ')
                self.datanode_list.append((ip, int(port)))

    def ensure_index_file(self):
        # Verifica se o arquivo 'index.txt' existe, se não, cria um novo
        if not os.path.exists(self.index_file):
            open(self.index_file, 'w').close()

    def load_index(self):
        index = {}
        with open(self.index_file, "r") as index_file:
            for line in index_file:
                file_name, ip, port = line.strip().split()
                index.setdefault(file_name, []).append((ip, int(port)))
        return index

    def exposed_upload_file(self, file_name, data):
        chosen_datanodes = random.sample(self.datanode_list, 3)
        for ip, port in chosen_datanodes:
            conn = rpyc.connect(ip, port)
            conn.root.upload_file(file_name, data)
            conn.close()
        self.index[file_name] = chosen_datanodes
        with open("index.txt", "a") as index_file:
            for ip, port in chosen_datanodes:
                index_file.write(f"{file_name} {ip} {port}\n")

    def exposed_stream_file(self, file_name):
        print(f"Streaming video: {file_name}")
        if file_name not in self.index:
            return None
        ip, port = random.choice(self.index[file_name])
        conn = rpyc.connect(ip, port)
        video_data = conn.root.stream_file(file_name)
        conn.close()
        print(f"Video '{file_name}' streamed.")
        return video_data

    def exposed_list_files(self):
        return list(self.index.keys())

    def exposed_search_files(self, search_query):
        return [file_name for file_name in self.index if search_query in file_name]

if __name__ == "__main__":
    manager_server = ThreadedServer(DataNodeManagerService, port=10000)
    manager_server.start()