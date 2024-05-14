import sys
import zmq
import pub

messagedata = ""
nomeClient = ""

def Subscriber():
    Broker_port = "5559"
    # Verifica se foi passada uma porta como argumento de linha de comando
    if len(sys.argv) > 1:
        Broker_port = sys.argv[1]
        int(Broker_port)  

    # Criando um contexto zmq
    context = zmq.Context()

    # Criando um socket do tipo SUB (assinante)
    socket = context.socket(zmq.SUB)

    print("Aguardando atualizações do chat...")

    # Conectando o socket ao endereço TCP do broker
    socket.connect("tcp://127.0.0.1:{0}".format(Broker_port))

    # Definindo um filtro de tópico para o assinante
    topicfilter = pub.topic
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

    # Recebendo a mensagem do socket
    string = str(socket.recv())
    parts = string.split()
    if len(parts) > 3:
        topic = parts[0]
        messagedata = " ".join(parts[1:len(parts)-1])  # do segundo ao penultimo
        nomeClient = "".join(parts[len(parts)-1])  # ultimo elemento
    else:
        topic, messagedata, nomeClient = string.split()

    return '{}: {}'.format(nomeClient, messagedata)
