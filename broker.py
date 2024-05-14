import zmq

PUB_PORT = "5557"
SUB_PORT = "5559"
VIDEO_PORT = "5561"  # Porta para os quadros de vídeo

context = zmq.Context()

# Criando sockets de comunicação com pubs e subs (assinantes)
pub_socket = context.socket(zmq.SUB)
pub_socket.bind("tcp://127.0.0.1:{0}".format(PUB_PORT))

sub_socket = context.socket(zmq.PUB)
sub_socket.bind("tcp://127.0.0.1:{0}".format(SUB_PORT))

video_socket = context.socket(zmq.PUB)
video_socket.bind("tcp://127.0.0.1:{0}".format(VIDEO_PORT))

pub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
print('iniciando broker')
# Inicializa um loop de encaminhamento de mensagens
while True:
    # Recebe a mensagem do PUB
    string = pub_socket.recv_string()
    topic, message = string.split(" ", 1)
    print("Topico e mensagem e nome recebidos no broker: ", topic , ",", message)
    
    # Encaminha mensagem para os assinantes
    sub_socket.send_string(string)

    # Se a mensagem for de vídeo, encaminha também para os assinantes de vídeo
    if topic == "VIDEO":
        # Encaminha mensagem para os assinantes de vídeo
        video_socket.send_string(message)
