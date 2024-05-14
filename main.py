# main.py

import tkinter as tk
import zmq
from threading import Thread
from queue import Queue
import pub
import sub
import cv2
import numpy as np
import base64
from PIL import Image, ImageTk

def send_message():
    message = entry_field.get()
    pub.socket.send_string("%s %s %s" % (pub.topic, message, pub.nome))

def start_video():
    video_thread = Thread(target=capture_video_thread, args=(0,))  # Usando câmera 0
    video_thread.daemon = True
    video_thread.start()

def capture_video_thread(camera_number):
    print("Iniciando captura de vídeo na câmera", camera_number)
    cap = cv2.VideoCapture(camera_number)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera", camera_number)
        return

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())
            video_label.configure(image=photo)
            video_label.image = photo

            # Envia o quadro de vídeo para o broker
            frame_encoded = base64.b64encode(cv2.imencode('.png', frame)[1]).decode('utf-8')
            pub.socket.send_string("VIDEO %s %s" % (frame_encoded, pub.nome))
        else:
            print("Erro: Falha ao capturar o frame da câmera", camera_number)
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Captura de vídeo na câmera", camera_number, "encerrada.")

def handle_video_message(message):
    topic, frame_data, nome = message.split(" ", 2)
    if pub.topic == topic:  # Verifica se o tópico do vídeo é o mesmo do chat atual
        # Converte os dados do frame de volta para um quadro de vídeo
        frame_array = cv2.imdecode(np.frombuffer(base64.b64decode(frame_data), dtype=np.uint8), cv2.IMREAD_COLOR)
        
        # Converte o quadro para o formato compatível com a interface gráfica
        frame_rgb = cv2.cvtColor(frame_array, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Exibe o quadro na interface gráfica
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

def receive_messages():
    while True:
        messageReceived = sub.Subscriber()
        if messageReceived.startswith("VIDEO"):
            handle_video_message(messageReceived)
        else:
            message_queue.put(messageReceived)

def process_messages():
    while True:
        if not message_queue.empty():
            message = message_queue.get()
            message_listbox.insert(tk.END, message)

def main():
    root = tk.Tk()
    root.title("Chat " + pub.topic)

    # Frame para o chat
    chat_frame = tk.Frame(root)
    chat_frame.pack(side=tk.LEFT)

    global message_listbox
    message_listbox = tk.Listbox(chat_frame, width=50, height=20)
    message_listbox.pack()

    global entry_field
    entry_field = tk.Entry(chat_frame, width=50)
    entry_field.pack()

    send_button = tk.Button(chat_frame, text="Send Message", command=send_message)
    send_button.pack()

    # Frame para o vídeo
    video_frame = tk.Frame(root)
    video_frame.pack(side=tk.RIGHT)

    global video_label
    video_label = tk.Label(video_frame)
    video_label.pack()

    start_video_button = tk.Button(video_frame, text="Start Video", command=start_video)
    start_video_button.pack()

    # Definindo as configurações de comunicação com o broker e criando a conexão
    message = ""
    pub.Publisher(message)

    # Inicializando as threads para receber e processar mensagens
    receive_thread = Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    process_thread = Thread(target=process_messages)
    process_thread.daemon = True
    process_thread.start()

    # Inicializando o loop de atualização da interface gráfica
    update_gui(root)

    root.mainloop()

def update_gui(root):
    if not message_queue.empty():
        message = message_queue.get()
        message_listbox.insert(tk.END, message)
    root.after(1000, update_gui, root)  # Atualiza a cada segundo

if __name__ == "__main__":
    message_queue = Queue()
    main()
