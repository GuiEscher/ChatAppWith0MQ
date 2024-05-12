import cv2
import zmq
import base64

# Configuração inicial do ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.PUB)  # Cria um socket de publicação
port = 5561  # Porta especificada para vídeo
socket.bind(f"tcp://127.0.0.1:{port}")  # Bind no socket para a porta correta para vídeo

# Inicializa a captura de vídeo da webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar imagem da câmera")
        break
    
    # Comprimir o frame para JPEG e codificar em base64 para transmissão
    _, buffer = cv2.imencode('.jpg', frame)
    compressed_video = base64.b64encode(buffer).decode()

    # Enviar o frame comprimido
    topic = "video"
    socket.send_string(f"{topic} {compressed_video}")

    # Mostrar o vídeo capturado (opcional)
    cv2.imshow('Video Capture', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpeza
cap.release()
cv2.destroyAllWindows()
socket.close()
context.term()
