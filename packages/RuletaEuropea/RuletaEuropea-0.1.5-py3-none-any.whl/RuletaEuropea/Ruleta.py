import random
from .Constantes import *
from .Numero import *
from .Apuesta import *

class Ruleta:
    def __init__(self):
        self.numeros = [Numero(numero) for numero in range(0, 37)]
        self.apuestas = []
        self.bola = None

    def caer_bola(self):
        self.bola = random.choice(self.numeros)
        return self.bola

    def girar_ruleta(self):
        self.caer_bola()
        return f"La bola cayó en: {self.bola}"

    def añadir_apuesta(self, apuesta: Apuesta):
        self.apuestas.append(apuesta)
        return apuesta.str_apuesta()

    def obtener_ganadores(self):
        if not self.bola:
            raise ValueError("No se ha tirado la bola")

        ganadores = []
        for apuesta in self.apuestas:
            if apuesta.apuesta == APUESTA_NUMERO:
                if apuesta.jugada == self.bola.numero:
                    ganadores.append(apuesta)
            elif apuesta.apuesta == APUESTA_COLOR:
                if apuesta.jugada == self.bola.color:
                    ganadores.append(apuesta)
            elif apuesta.apuesta == APUESTA_PAR_IMPAR:
                if apuesta.jugada == PAR and self.bola.par:
                    ganadores.append(apuesta)
                elif apuesta.jugada == IMPAR and self.bola.impar:
                    ganadores.append(apuesta)
            elif apuesta.apuesta == APUESTA_BAJO_ALTO:
                if apuesta.jugada == ALTO and self.bola.alto:
                    ganadores.append(apuesta)
                elif apuesta.jugada == BAJO and self.bola.bajo:
                    ganadores.append(apuesta)
            elif apuesta.apuesta == APUESTA_DOCENA:
                if apuesta.jugada == self.bola.docena:
                    ganadores.append(apuesta)
            elif apuesta.apuesta == APUESTA_COLUMNA:
                if apuesta.jugada == self.bola.columna:
                    ganadores.append(apuesta)
            elif apuesta.apuesta == APUESTA_CALLE:
                if apuesta.jugada == self.bola.calle:
                    ganadores.append(apuesta)

        return ganadores

    def obtener_perdedores(self):
        if not self.bola:
            raise ValueError("No se ha tirado la bola")

        ganadores = self.obtener_ganadores()
        perdedores = [apuesta for apuesta in self.apuestas if apuesta not in ganadores]
        return perdedores