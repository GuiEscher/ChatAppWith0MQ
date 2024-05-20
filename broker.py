import zmq

PUB_PORT = "5557"
SUB_PORT = "5559"

context = zmq.Context()

# Criando sockets de comunicação com pubs e subs (assinantes)
pub_socket = context.socket(zmq.SUB)
pub_socket.bind("tcp://127.0.0.1:{0}".format(PUB_PORT))

sub_socket = context.socket(zmq.PUB)
sub_socket.bind("tcp://127.0.0.1:{0}".format(SUB_PORT))

pub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

print('Iniciando broker...')
# Inicializa um loop de encaminhamento de mensagens
while True:
    # Recebe a mensagem do PUB
    string = pub_socket.recv_string()
    topic, message_type, message, nome = string.split(" ", 3)
    print("Topico, tipo de mensagem, mensagem e nome recebidos no broker: ", topic, ",", message_type, ",", message, ",", nome)
    
    # Encaminha mensagem para os assinantes
    sub_socket.send_string(string)
