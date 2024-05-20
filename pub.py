import zmq
import sys
import cv2
import base64
import time
import imutils
import queue
import threading

topic = input("Selecione o tópico que deseja se inscrever, opções: alo - primeirochat - ")
nome = input("Insira seu nome para participar de algum topico: ")

socket = None  # Definindo o socket

def setup_publisher_socket():
    global socket
    Broker_port = "5557"

    if len(sys.argv) > 1:
        Broker_port = sys.argv[1]

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:{0}".format(Broker_port))

def Publisher():
    def pyshine_video_queue(vid):
        q = queue.Queue(maxsize=50)  
        def getVideo():
            while vid.isOpened():
                try:
                    ret, frame = vid.read()
                    if not ret:
                        break
                    frame = imutils.resize(frame, width=640)
                    q.put(frame)
                except Exception as e:
                    print("Erro ao capturar vídeo: ", e)
                    break
        thread = threading.Thread(target=getVideo, args=())
        thread.start()
        return q

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FPS, 30)  # Ajustando a taxa de quadros para 15 FPS
    q = pyshine_video_queue(vid)

    while True:
        if not q.empty():
            frame = q.get()
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])  # Melhorando a compressão da imagem
            data = base64.b64encode(buffer).decode('utf-8')
            socket.send_string("%s %s %s %s" % (topic, "VIDEO", data, nome))
        time.sleep(0.066)  # Espera para manter a taxa de quadros consistente

    vid.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    setup_publisher_socket()
