import zmq
import sys
import cv2
import base64
import numpy as np

context = zmq.Context()
client_socket = context.socket(zmq.SUB)
client_socket.connect("tcp://127.0.0.1:5559")
client_socket.setsockopt_string(zmq.SUBSCRIBE, "")

def Subscriber():
    string = client_socket.recv_string()
    topic, message_type, message, nome = string.split(" ", 3)
    return '{} {} {} {}'.format(topic, message_type, message, nome)

def handle_video_message(message):
    parts = message.split()
    frame_data = parts[0]
    frame_array = cv2.imdecode(np.frombuffer(base64.b64decode(frame_data), dtype=np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow("client image", frame_array)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        message = Subscriber()
        if message.split()[1] == "VIDEO":
            handle_video_message(message.split()[2])
