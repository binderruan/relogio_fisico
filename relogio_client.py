import threading
import socket
from tempo import Tempo
from time import sleep
from tempo import timeToSeconds, timeToArray

class Client:
    def __init__(self, port):
        self.tempo = Tempo()
        self.HOST = '127.0.0.1'
        self.PORT = port
        self.serverPort = 5000

        self.setup_server_socket()

        print(f"Relógio rodando em {self.HOST}:{self.PORT}")
        threading.Thread(target=self.clock).start()
        threading.Thread(target=self.receive_server).start()

    def setup_server_socket(self):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.HOST, self.PORT))
        self.tcp.listen()

    def clock(self):
        while True:
            sleep(1)
            self.tempo.add_seconds()
            print(f"Tempo do relógio -> {self.tempo.hora:02}:{self.tempo.minuto:02}:{self.tempo.segundo:02}")

    def send(self):
        print("Enviando tempo")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("127.0.0.1", self.serverPort))
            time_seconds = timeToSeconds([self.tempo.hora, self.tempo.minuto, self.tempo.segundo])
            client.sendall(str.encode(f"{self.PORT},{time_seconds}"))
        except:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_server(self):
        while True:
            connection, address = self.tcp.accept()
            message = connection.recv(1024).decode()
            if message == "SEND":
                threading.Thread(target=self.send).start()
            else:
                tempo_att = timeToSeconds([self.tempo.hora, self.tempo.minuto, self.tempo.segundo]) - int(message)
                print(f"Diferença -> {int(message)}")
                print(f"Atualizado para -> {tempo_att}")
                self.tempo.hora, self.tempo.minuto, self.tempo.segundo = timeToArray(tempo_att)
