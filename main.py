import tkinter as tk
import zmq
from threading import Thread
from queue import Queue
import pub
import sub
import cv2
import base64
import numpy as np
from PIL import Image, ImageTk

def send_message():
    message = entry_field.get()
    pub.socket.send_string("%s %s %s %s" % (pub.topic, "TEXT", message, pub.nome))
    entry_field.delete(0, tk.END)

def start_video():
    video_thread = Thread(target=pub.Publisher)
    video_thread.daemon = True
    video_thread.start()

def handle_video_message(message):
    frame_data = message
    frame_array = cv2.imdecode(np.frombuffer(base64.b64decode(frame_data), dtype=np.uint8), cv2.IMREAD_COLOR)
    frame_rgb = cv2.cvtColor(frame_array, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

def receive_messages():
    while True:
        messageReceived = sub.Subscriber()
        parts = messageReceived.split(" ", 3)
        if parts[1] == "VIDEO":
            handle_video_message(parts[2])
        else:
            message_queue.put('{}: {}'.format(parts[3], parts[2]))

def process_messages():
    while True:
        if not message_queue.empty():
            message = message_queue.get()
            message_listbox.insert(tk.END, message)

def main():
    root = tk.Tk()
    root.title("Chat " + pub.topic)

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

    video_frame = tk.Frame(root)
    video_frame.pack(side=tk.RIGHT)

    global video_label
    video_label = tk.Label(video_frame)
    video_label.pack()

    start_video_button = tk.Button(video_frame, text="Start Video", command=start_video)
    start_video_button.pack()

    pub.setup_publisher_socket()  # Configurar o socket antes de iniciar o envio de mensagens

    receive_thread = Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    process_thread = Thread(target=process_messages)
    process_thread.daemon = True
    process_thread.start()

    update_gui(root)

    root.mainloop()

def update_gui(root):
    if not message_queue.empty():
        message = message_queue.get()
        message_listbox.insert(tk.END, message)
    root.after(2000, update_gui, root)

if __name__ == "__main__":
    message_queue = Queue()
    main()
