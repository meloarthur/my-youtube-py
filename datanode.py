import rpyc
import os
from env import CHUNK_SIZE
class FileService(rpyc.Service):
    PORT = 8084
    diretorio = f"uploads{PORT}"

    def on_connect(self, conn):
        # Cria o diretório se não existir
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)

    def exposed_upload_file(self, file_name, file_generator):
        # Handle file upload request
        print(f"Receiving file: {file_name}")
        with open(f"{self.diretorio}/{file_name}", "wb") as file:
            for data in file_generator:
                file.write(data)
        print(f"File '{file_name}' received and saved.")

    def exposed_stream_file(self, file_name):
        def file_reader(file):
            while True:
                chunk = file.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk
        print(f"Streaming video: {file_name}")
        video_file = open(f"{self.diretorio}/{file_name}", "rb")
        print(f"Video '{file_name}' streamed.")
        return file_reader(video_file)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(FileService, port=FileService.PORT)
    print("DATANODE SERVER IS AWAKE")
    t.start()