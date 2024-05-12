import zmq

# Portas para diferentes tipos de dados
PUB_PORT = "5557"
SUB_PORT_AUDIO = "5560"
SUB_PORT_VIDEO = "5561"
SUB_PORT_TEXT = "5562"

context = zmq.Context()

# Socket para receber mensagens de todos os tipos
pub_socket = context.socket(zmq.SUB)
pub_socket.bind("tcp://127.0.0.1:{0}".format(PUB_PORT))
pub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# Sockets para enviar mensagens de áudio, vídeo e texto
sub_socket_audio = context.socket(zmq.PUB)
sub_socket_audio.bind("tcp://127.0.0.1:{0}".format(SUB_PORT_AUDIO))

sub_socket_video = context.socket(zmq.PUB)
sub_socket_video.bind("tcp://127.0.0.1:{0}".format(SUB_PORT_VIDEO))

sub_socket_text = context.socket(zmq.PUB)
sub_socket_text.bind("tcp://127.0.0.1:{0}".format(SUB_PORT_TEXT))

print("Broker inicializado para Audio, Video e Texto")

# Loop para encaminhar mensagens para os canais correspondentes
while True:
    message = pub_socket.recv_string()
    data_type, topic, content = message.split(' ', 2)

    if data_type == 'audio':
        sub_socket_audio.send_string(f"{topic} {content}")
    elif data_type == 'video':
        sub_socket_video.send_string(f"{topic} {content}")
    elif data_type == 'text':
        sub_socket_text.send_string(f"{topic} {content}")
