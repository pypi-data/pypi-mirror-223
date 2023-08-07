from .Constantes import *

class Numero:
    def __init__(self, numero):
        self.numero = int(numero)
        self.color = self.calcular_color()
        self.columna = self.calcular_columna()
        self.docena = self.calcular_docena()
        self.par = self.calcular_par()
        self.impar = self.calcular_impar()
        self.bajo = self.calcular_bajo()
        self.alto = self.calcular_alto()
        self.calle = self.calcular_calle()

    def __str__(self):
        info_numero = f"Numero: {self.numero}"
        info_numero += f", Color: {self.color}"
        if self.par:
            info_numero += f", Es: Par"
        if self.impar:
            info_numero += f", Es: Impar"
        if self.bajo:
            info_numero += f", Es: Bajo"
        if self.alto:
            info_numero += f", Es: Alto"
        if self.columna:
            info_numero += f", Columna: {self.columna}"
        if self.docena:
            info_numero += f", Docena: {self.docena}"
        if self.calle:
            info_numero += f", Calle: {self.calle}"

        return info_numero

    def calcular_color(self):
        if self.numero == 0:
            return VERDE
        elif self.numero % 2 == 0:
            return NEGRO if self.numero <= 10 or (self.numero >= 20 and self.numero <= 28) else ROJO
        else:
            return ROJO if self.numero <= 10 or (self.numero >= 20 and self.numero <= 28) else NEGRO

    def calcular_columna(self):
        if self.numero == 0:
            return None
        return (self.numero - 1) % 3 + 1

    def calcular_docena(self):
        if self.numero == 0:
            return None
        return (self.numero - 1) // 12 + 1

    def calcular_par(self):
        if self.numero == 0:
            return False
        return self.numero % 2 == 0

    def calcular_impar(self):
        if self.numero == 0:
            return False
        return self.numero % 2 != 0

    def calcular_bajo(self):
        return 1 <= self.numero <= 18

    def calcular_alto(self):
        return 19 <= self.numero <= 36

    def calcular_calle(self):
        if self.numero == 0:
            return None
        elif 1 <= self.numero <= 3:
            return 1
        elif 4 <= self.numero <= 6:
            return 2
        elif 7 <= self.numero <= 9:
            return 3
        elif 10 <= self.numero <= 12:
            return 4
        elif 13 <= self.numero <= 15:
            return 5
        elif 16 <= self.numero <= 18:
            return 6
        elif 19 <= self.numero <= 21:
            return 7
        elif 22 <= self.numero <= 24:
            return 8
        elif 25 <= self.numero <= 27:
            return 9
        elif 28 <= self.numero <= 30:
            return 10
        elif 31 <= self.numero <= 33:
            return 11
        elif 34 <= self.numero <= 36:
            return 12