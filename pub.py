# publisher.py

import zmq
import sys
import tkinter as tk

# Definindo a porta do broker 
Broker_port = "5557"

# Verifica se foi passada uma porta como argumento de linha de comando
if len(sys.argv) > 1:
    Broker_port = sys.argv[1]
    int(Broker_port)  

# Criando um contexto zmq
context = zmq.Context()

# Criando um socket do tipo PUB (publicador)
socket = context.socket(zmq.PUB)

# Conectando o socket ao endereço TCP local e à porta 
socket.connect("tcp://127.0.0.1:{0}".format(Broker_port))

topic = input("Selecione o tópico que deseja se inscrever, opções: alo - primeirochat -")

nome = input("Insira seu nome para participar de algum topico")



def ClicaBotao():
    print("O botão foi clicado")

# root = tk.Tk() 
# root.title("Chat")
# entry_field = tk.Entry(root, width=50)
# entry_field.pack()
# send_button = tk.Button(root, text="Send message", command=ClicaBotao, bg="blue")
# send_button.pack()
# root.mainloop()

# Laço infinito para enviar mensagens continuamente
while True:
   
    
    messagedata = input("Eu: ")
    
    # Imprimindo a mensagem no console (depuração)
    print("Mensagem enviada em", topic, " -> ", messagedata)
    
    # Enviando a mensagem pelo socket
    socket.send_string("%s %s %s" % (topic, messagedata, nome))
    
    
