import math
from random import randint

class Tempo:
    def __init__(self):
        # Configuração do relógio
        self.qtdRelogios = 0
        self.segundo = 0
        self.hora = 0
        self.minuto = 0

    def add_seconds(self):
        random = randint(0, 100)
        if random <= 3:
            self.segundo += 2
        elif random >= 97:
            self.segundo -= 1
        else:
            self.segundo += 1

        if self.segundo >= 60:
            self.minuto += 1
            self.segundo = 0
        if self.minuto >= 60:
            self.hora += 1
            self.minuto = 0
        if self.hora >= 24:
            self.hora = 0

def timeToArray(tempo=None):
    if tempo is None:
        return [0, 0, 0]

    horas = math.floor(tempo / 3600)
    resto = tempo - (horas * 3600)
    minutos = math.floor(resto / 60)
    resto = resto - (minutos * 60)
    segundos = round(resto)

    return [horas, minutos, segundos]

def timeToSeconds(tempo=None):
    if tempo is None:
        return 0
    return (tempo[0] * 3600) + (tempo[1] * 60) + tempo[2]
