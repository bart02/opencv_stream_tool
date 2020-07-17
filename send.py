import cv2
from base64 import b64encode
import zmq


class Streamer:
    def __init__(self, ip='localhost', port=5555, mode='slave', resolution=(200, 150)):
        self.ip = ip
        self.port = port
        self.resolution = resolution

        self.context = zmq.Context()
        self.footage_socket = self.context.socket(zmq.PUB)

        if mode == 'master' or self.ip == '0.0.0.0':
            self.footage_socket.bind('tcp://*:{}'.format(self.port))
        else:
            self.footage_socket.connect('tcp://{}:{}'.format(self.ip, self.port))

    def stream(self, wnidow_name, frame):
        resized = cv2.resize(frame, self.resolution)  # resize the frame
        _, buffer = cv2.imencode('.jpg', resized)
        base64_image = b64encode(buffer).decode()
        self.footage_socket.send_string(wnidow_name + ';' + base64_image)
