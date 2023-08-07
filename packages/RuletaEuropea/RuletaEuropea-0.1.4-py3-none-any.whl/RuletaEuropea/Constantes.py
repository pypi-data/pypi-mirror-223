APUESTA_COLOR = "Color"
PAGA_COLOR_NEGRO_ROJO = 1
PAGA_COLOR_VERDE = 35
VERDE = "Verde"
NEGRO = "Negro"
ROJO = "Rojo"

APUESTA_PAR_IMPAR = "ParImpar"
PAGA_PAR_IMPAR = 1
PAR = "Par"
IMPAR = "Impar"

APUESTA_BAJO_ALTO = "BajoAlto"
PAGA_BAJO_ALTO = 1
ALTO = "Alto"
BAJO = "Bajo"

APUESTA_NUMERO = "Numero"
PAGA_NUMERO = 35

APUESTA_DOCENA = "Docena"
PAGA_DOCENA = 2

APUESTA_COLUMNA = "Columna"
PAGA_COLUMNA = 2

APUESTA_CALLE = "Calle"
PAGA_CALLE = 11

APUESTAS_PERMITIDAS = {
    APUESTA_COLOR: [VERDE, ROJO, NEGRO],
    APUESTA_PAR_IMPAR: [PAR, IMPAR],
    APUESTA_BAJO_ALTO: [ALTO, BAJO],
    APUESTA_NUMERO: [numero for numero in range(0, 37)],
    APUESTA_DOCENA: [numero for numero in range(1, 4)],
    APUESTA_COLUMNA: [numero for numero in range(1, 4)],
    APUESTA_CALLE: [numero for numero in range(1, 13)],
}