import random
from .Constantes import *
from .Numero import *
from .Apuesta import *

class Ruleta:
    def __init__(self):
        self.numeros = [Numero(numero) for numero in range(0, 37)]
        self.apuestas = []
        self.bola = None

    def tablero(self):
        return """                      Calle    
     01 02 03 04   05 06 07 08  09  10 11 12    
 / | [2;31m03[0m 06 [2;31m09 12[0m | 15 [2;31m18 21[0m 24 | [2;31m27 30[0m 33 [2;31m36[0m | Columna3 
 [2;36m0[0m | 02 [2;31m05[0m 08 11 | [2;31m14[0m 17 20 [2;31m23[0m | 26 29 [2;31m32[0m 35 | Columna2
 \ | [2;31m01[0m 04 [2;31m[2;31m07[0m[2;31m[0m 10 | 13 [2;31m16 19[0m 22 | [2;31m25[0m 28 31 [2;31m34[0m | Columna1 
       1Docena       2Docena       3Docena
        01-18       Par-Impar       19-36
       (Bajos)     [2;31mRojo[0m-Negro      (Altos)  
"""

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