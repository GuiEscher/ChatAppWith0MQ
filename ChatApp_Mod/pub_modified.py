import zmq
import sys
import tkinter as tk

# Definindo a porta do broker
Broker_port = "5557"

# Criando um contexto zmq
context = zmq.Context()

# Criando um socket do tipo PUB (publicador)
socket = context.socket(zmq.PUB)
socket.connect("tcp://127.0.0.1:{0}".format(Broker_port))

# Interface para o usuário
tipo = input("Escolha o tipo de conteúdo ('audio', 'video', 'text'): ")
topic = input("Selecione o tópico que deseja se inscrever, opções: alo - primeirochat -")
nome = input("Insira seu nome para participar de algum tópico")

# Laço infinito para enviar mensagens continuamente
while True:
    messagedata = input("Eu: ")
    # Enviando a mensagem pelo socket
    socket.send_string(f"{tipo} {topic} {messagedata} {nome}")
