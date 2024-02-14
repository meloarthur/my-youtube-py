import rpyc
import os

class FileService(rpyc.Service):
    PORT = 8084
    diretorio = f"uploads{PORT}"

    def on_connect(self, conn):
        # Cria o diretório se não existir
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)

    def on_disconnect(self, conn):
        pass

    def exposed_upload_file(self, file_name, data):
        # Handle file upload request
        print(f"Receiving file: {file_name}")
        with open(f"{self.diretorio}/{file_name}", "wb") as file:
            file.write(data)
        print(f"File '{file_name}' received and saved.")

    def exposed_stream_file(self, file_name):
        # Handle streaming request
        print(f"Streaming video: {file_name}")
        with open(f"{self.diretorio}/{file_name}", "rb") as video_file:
            video_data = video_file.read()
        print(f"Video '{file_name}' streamed.")
        return video_data

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(FileService, port=FileService.PORT)
    t.start()