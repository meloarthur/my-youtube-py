import tkinter as tk
from tkinter import ttk
import psycopg2
from db_conn import get_db_connection

selected_video_id = None  # Variável para armazenar o videos_id selecionado

def fetch_videos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT videos_id, titulo, duracao, nome_arquivo FROM videos")
    videos = cursor.fetchall()

    conn.close()
    return videos

# Função para formatar a duração
def format_duration(duration):
    minutes, seconds = divmod(duration, 60)
    return f"{minutes}:{seconds:02}"  # Formato MM:SS

# Função para abrir uma janela com a ação "Assistir"
def assistir_video():
    if selected_video_id is not None:
        print(f"Assistir vídeo {selected_video_id}")
        # Aqui você pode implementar a ação de assistir o vídeo

# Função para abrir uma janela com a ação "Editar"
def editar_video():
    if selected_video_id is not None:
        print(f"Editar vídeo {selected_video_id}")
        # Aqui você pode implementar a ação de edição do vídeo

# Função para excluir um vídeo
def excluir_video():
    if selected_video_id is not None:
        print(f"Excluir vídeo {selected_video_id}")
        # Aqui você pode implementar a ação de exclusão do vídeo

# Função para abrir a janela de adição de vídeo
def adicionar_video():
    print("Adicionar vídeo")
    # Aqui você pode implementar a lógica para adicionar um novo vídeo
    # por exemplo, abrir um formulário de adição de vídeo
    
# Função para lidar com a seleção de uma linha na tabela
def handle_selection(event):
    selected_item = table.selection()
    if selected_item:
        selected_values = table.item(selected_item)['values']
        if selected_values:
            global selected_video_id  # Usar a variável global
            selected_video_id = selected_values[0]
            print(f"ID DO VIDEO: {selected_video_id}")

# Crie a janela
window = tk.Tk()
window.title("My YouTube")

# Crie um botão "Adicionar vídeo" acima da tabela
adicionar_button = ttk.Button(window, text="Adicionar vídeo", command=adicionar_video)
adicionar_button.pack(pady=10)  # Espaço entre o botão e a tabela

# Crie um Frame para a tabela
table_frame = tk.Frame(window)
table_frame.pack(fill="both", expand=True)

# Crie uma Treeview para exibir a tabela dentro do Frame
table = ttk.Treeview(table_frame, columns=("ID", "Título", "Duração", "Nome do Arquivo"))
table.heading("#1", text="ID")
table.heading("#2", text="Título")
table.heading("#3", text="Duração")
table.heading("#4", text="Nome do Arquivo")

# Defina o tamanho das colunas
table.column("#1", width=50, anchor="center")
table.column("#2", width=200, anchor="center")
table.column("#3", width=100, anchor="center")
table.column("#4", width=80, anchor="center")

# Busque os dados da tabela e insira na tabela
videos = fetch_videos()
for video in videos:
    videos_id, titulo, duracao, nome_arquivo = video
    formatted_duration = format_duration(duracao)
    
    row_id = table.insert("", "end", values=(videos_id, titulo, formatted_duration, nome_arquivo))

# Empacote a tabela na tela
table.pack(fill="both", expand=True)

# Lidar com a seleção de uma linha na tabela
table.bind("<<TreeviewSelect>>", handle_selection)

# Crie um frame para os botões
button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

# Crie os botões "Assistir", "Editar" e "Excluir" dentro do frame
assistir_button = ttk.Button(button_frame, text="Assistir", command=assistir_video)
editar_button = ttk.Button(button_frame, text="Editar", command=editar_video)
excluir_button = ttk.Button(button_frame, text="Excluir", command=excluir_video)

assistir_button.pack(side="left", padx=10)
editar_button.pack(side="left", padx=10)
excluir_button.pack(side="left", padx=10)

# Defina o tamanho da janela
window.geometry("800x600")

# Obtenha as dimensões da tela
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calcule as coordenadas para centralizar a janela
x = (screen_width - 800) // 2
y = (screen_height - 600) // 2

# Defina a posição da janela centralizada
window.geometry(f"+{x}+{y}")

# Inicie o loop principal do Tkinter
window.mainloop()