# publisher.py

import zmq
import sys
import tkinter as tk
from threading import Thread
import numpy as np
import base64
from PIL import Image, ImageTk

topic = input("Selecione o tópico que deseja se inscrever, opções: alo - primeirochat -")
nome = input("Insira seu nome para participar de algum topico")

def Publisher(messagedata):
    # Definindo a porta do broker 
    Broker_port = "5557"
    Video_topic = "VIDEO"  # Tópico para os quadros de vídeo

    # Verifica se foi passada uma porta como argumento de linha de comando
    if len(sys.argv) > 1:
        Broker_port = sys.argv[1]
        int(Broker_port)  

    # Criando um contexto zmq
    context = zmq.Context()
    global socket

    # Criando um socket do tipo PUB (publicador)
    socket = context.socket(zmq.PUB)

    # Conectando o socket ao endereço TCP local e à porta 
    socket.connect("tcp://127.0.0.1:{0}".format(Broker_port))

    # Se a mensagem começar com "VIDEO:", trata-se de um quadro de vídeo
    if messagedata.startswith("VIDEO:"):
        with open(messagedata.split(":")[1], "rb") as video_file:
            # Lê o quadro de vídeo
            frame = video_file.read()
            # Codifica o quadro de vídeo em base64 para envio
            encoded_frame = base64.b64encode(frame).decode('utf-8')
            # Envia o quadro de vídeo para o tópico de vídeo
            socket.send_string("%s %s %s" % (Video_topic, encoded_frame, nome))
    else:
        # Imprimindo a mensagem no console
        print("Mensagem enviada em", topic, " -> ", messagedata)
        # Enviando a mensagem pelo socket
        socket.send_string("%s %s %s" % (topic, messagedata, nome))
