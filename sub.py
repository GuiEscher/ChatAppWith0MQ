# subscriber.py

import sys
import zmq

# Definindo a porta 
port = "5557"

# Verifica se foi passada uma porta como argumento de linha de comando
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)  

# Criando um contexto zmq
context = zmq.Context()

# Criando um socket do tipo SUB (assinante)
socket = context.socket(zmq.SUB)

print("Aguardando atualizações do chat...")

# Vinculando o socket ao endereço TCP local e à porta especificada
socket.bind("tcp://127.0.0.1:%s" % port)

# Definindo um filtro de tópico para o assinante
topicfilter = "alo"
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

# Processando 5 atualizações
total_value = 0 
while(True):
    # Recebendo a mensagem do socket
    string = str(socket.recv())
    parts = string.split()
    if(len(parts) > 3):
        topic = parts[0]
        messagedata = " ".join(parts[1:len(parts)-1]) # do segundo ao penultimo
        nomeClient= "".join(parts[len(parts)-1]) # ultimo elemento
        # print(len(parts), " Tamanho do vetor de receives")
        # print(topic, " topico aqui")
        # print(messagedata, " mensagem aqui")
        # print(nomeClient, " Nome aqui")
    # Imprimindo o tópico e os dados recebidos
    else:
        topic, messagedata, nomeClient = string.split()

    print( '\n', str(nomeClient), ": ", str(messagedata))


