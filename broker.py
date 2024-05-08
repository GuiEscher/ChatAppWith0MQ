# Broker.py

import zmq

PUB_PORT = "5557"
SUB_PORT = "5559"

context = zmq.Context()

# Criando sockets de comunicação com pubs e subs (assinantes)
pub_socket = context.socket(zmq.SUB)
pub_socket.bind("tcp://127.0.0.1:{0}".format(PUB_PORT))


sub_socket = context.socket(zmq.PUB)
sub_socket.bind("tcp://127.0.0.1:{0}".format(SUB_PORT))
print("entrando no broker")
pub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
# Inicializa um loop de encaminhamento de mensagens
while True:
    # Recebe a mensagem do PUB
    string = pub_socket.recv_string()
    topic, message = string.split(" ", 1)
    print("Topico, mensagem e nome recebidos no broker: ", topic , ",", message)
    
    # Encaminha mensagem para os assinantes
    sub_socket.send_string(string)


# TESTES REALIZADOS: mostraram que atualmente o broker recebe mensagens de todos os publishers
# e as envia, com base no tópico, para seus respectivos subscribers 