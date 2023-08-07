from .Constantes import *

def es_numero(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

class Apuesta:
    def __init__(self, usuario, apuesta, jugada, cantidad_apostada: int):
        
        if apuesta not in APUESTAS_PERMITIDAS:
            raise ValueError("Apuesta no permitida")
        if jugada not in APUESTAS_PERMITIDAS[apuesta]:
            raise ValueError(f"Jugada no permitida para la apuesta {apuesta}")
        
        self.usuario = usuario
        self.apuesta = apuesta
        if es_numero(jugada):
            self.jugada = int(jugada)
        else:
            self.jugada = jugada
        self.cantidad_apostada = int(cantidad_apostada)
        self.cantidad_a_ganar = self.calcular_paga()

    def __str__(self):
        return f"Usuario: {self.usuario}, Apuesta: {self.apuesta}, Jugada: {self.jugada}, Cantidad apostada: {self.cantidad_apostada}, Cantidad a ganar: {self.cantidad_a_ganar}"

    def str_apuesta(self):
        return f"{self.usuario} apostó ¢ {self.cantidad_apostada} jugando {self.apuesta} {self.jugada}!"

    def str_ganador(self):
        return f"{self.usuario} apostó ¢ {self.cantidad_apostada} jugando {self.apuesta} {self.jugada} y ganó ¢ {self.cantidad_ganada()}!"
    
    def str_perdedor(self):
        return f"{self.usuario} perdió ¢ {self.cantidad_apostada} jugando {self.apuesta} {self.jugada} :c"

    def calcular_paga(self):
        if self.apuesta == APUESTA_COLOR:
            if self.jugada == VERDE:
                return self.cantidad_apostada * PAGA_COLOR_VERDE
            else:
                return self.cantidad_apostada * PAGA_COLOR_NEGRO_ROJO
        elif self.apuesta == APUESTA_PAR_IMPAR:
            return self.cantidad_apostada * PAGA_PAR_IMPAR
        elif self.apuesta == APUESTA_BAJO_ALTO:
            return self.cantidad_apostada * PAGA_BAJO_ALTO
        elif self.apuesta == APUESTA_NUMERO:
            return self.cantidad_apostada * PAGA_NUMERO
        elif self.apuesta == APUESTA_DOCENA:
            return self.cantidad_apostada * PAGA_DOCENA
        elif self.apuesta == APUESTA_COLUMNA:
            return self.cantidad_apostada * PAGA_COLUMNA
        elif self.apuesta == APUESTA_CALLE:
            return self.cantidad_apostada * PAGA_CALLE

    def cantidad_ganada(self):
        return int(self.cantidad_a_ganar + self.cantidad_apostada)