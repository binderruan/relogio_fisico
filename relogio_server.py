import socket
import threading
import time
from tempo import Tempo, timeToSeconds, timeToArray

class Server:
    def __init__(self, port):
        self.HOST = '127.0.0.1'
        self.PORT = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.HOST, self.PORT))
        self.tcp.listen()
        self.receives = 0

        self.relogios = {
            5001: 0,
            5002: 0,
            5003: 0,
            5004: 0
        }
        self.tempo = Tempo()

        print(f"Servidor rodando em {self.HOST}:{self.PORT}")
        threading.Thread(target=self.clock).start()
        threading.Thread(target=self.receive).start()

    def clock(self):
        aux = 0
        while True:
            time.sleep(1)
            self.tempo.add_seconds()
            aux += 1
            print(f"Tempo servidor -> {self.tempo.hora:02}:{self.tempo.minuto:02}:{self.tempo.segundo:02}")
            if aux == 10:
                print("Executando algoritmo de Berkeley Unix")
                threading.Thread(target=self.sendFlag).start()
                aux = 0

    def receive(self):
        while True:
            connection, address = self.tcp.accept()
            msg = connection.recv(1024).decode()
            porta, tempo = map(int, msg.split(','))
            self.relogios[porta] = tempo
            self.receives += 1
            if self.receives == len(self.relogios):
                self.receives = 0
                print("Recebeu o tempo de todos os relógios!")
                threading.Thread(target=self.sendRealTime).start()

    def sendFlag(self):
        for relogio in self.relogios.keys():
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect(("127.0.0.1", relogio))
                client.sendall(str.encode("SEND"))
            except:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            finally:
                client.close()

    def sendRealTime(self):
        total_tempo = timeToSeconds([self.tempo.hora, self.tempo.minuto, self.tempo.segundo])
        for tempo in self.relogios.values():
            total_tempo += tempo

        media = round(total_tempo / (len(self.relogios) + 1))  # +1 relacionado ao servidor
        print(f"Média gerada -> {media}")

        self.tempo.hora, self.tempo.minuto, self.tempo.segundo = timeToArray(media)
        for relogio, tempo in self.relogios.items():
            retorno = tempo - media
            print(f"Relógio {relogio} recebeu diferença de -> {retorno} s")

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect(("127.0.0.1", relogio))
                client.sendall(str.encode(f"{retorno}"))
            except:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            finally:
                client.close()
