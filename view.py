import cv2
import zmq
from base64 import b64decode
import numpy as np
from threading import Thread


class Viewer:
    def __init__(self, callback, ip='localhost', port=5555, mode='master'):
        self.ip = ip
        self.port = port
        self.callback = callback

        self.context = zmq.Context()
        self.footage_socket = self.context.socket(zmq.SUB)

        if mode == 'master' or self.ip == '0.0.0.0':
            self.footage_socket.bind('tcp://*:{}'.format(self.port))
        else:
            self.footage_socket.connect('tcp://{}:{}'.format(self.ip, self.port))

        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

        self.thread = Thread(target=self._threaded_func)
        self.thread.start()

    def _threaded_func(self):
        while True:
            window, frame = self.footage_socket.recv_string().split(';')
            npimg = np.fromstring(b64decode(frame), dtype=np.uint8)
            img = cv2.imdecode(npimg, 1)
            self.callback(window, img)
