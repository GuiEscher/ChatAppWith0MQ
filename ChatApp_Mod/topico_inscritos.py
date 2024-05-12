import zmq
import sys

# Portas para diferentes tipos de dados
port_audio = "5560"
port_video = "5561"
port_text = "5562"

# Criando um contexto zmq
context = zmq.Context()

# Usuário escolhe o tipo de conteúdo
tipo = input("Escolha o tipo de conteúdo para receber ('audio', 'video', 'text'): ")

# Decidindo a porta com base no tipo de conteúdo
if tipo == 'audio':
    port = port_audio
elif tipo == 'video':
    port = port_video
elif tipo == 'text':
    port = port_text
else:
    raise ValueError("Tipo de conteúdo não reconhecido")

# Criando um socket do tipo SUB (assinante)
socket = context.socket(zmq.SUB)
socket.connect(f"tcp://127.0.0.1:{port}")

# Permitindo múltiplas inscrições em tópicos
topicos_inscritos = {}
while True:
    novo_topico = input("Inscreva-se em um tópico ou digite 'pronto' para começar a receber mensagens: ")
    if novo_topico.lower() == 'pronto':
        break
    if novo_topico not in topicos_inscritos:
        socket.setsockopt_string(zmq.SUBSCRIBE, novo_topico)
        topicos_inscritos[novo_topico] = []

print(f"Aguardando atualizações do {tipo} nos tópicos {', '.join(topicos_inscritos.keys())}...")

# Loop para receber mensagens
while True:
    string = socket.recv_string()
    topic, messagedata, nome = string.split(' ', 2)
    if topic in topicos_inscritos:
        topicos_inscritos[topic].append(f"{nome}: {messagedata}")
        print(f"\\n{nome}: {messagedata} (Tópico: {topic})")
