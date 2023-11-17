#Importaciones
import pygame
import os
import sys
import math
import time
import random

#Inicio de elementos
pygame.init()
pygame.font.init()
pygame.mixer.init()

#Variables
alt_Boton= 30
medida_Cuadro=200

#Definición de la parte no visible de los cuadros
nombre_carta_oculta="Elementos/oculta.png"
imagen_oculta= pygame.image.load(nombre_carta_oculta)
segs_visible_carta = 2

class Cuadro: #
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False

        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)

#Lista con todos los elementos
cuadros=[
    [Cuadro("Elementos/Alomomola.png"), Cuadro("Elementos/Alomomola.png"),
    Cuadro("Elementos/Charizard.png"), Cuadro("Elementos/Charizard.png")],
    [Cuadro("Elementos/Drednaw.png"), Cuadro("Elementos/Drednaw.png"),
    Cuadro("Elementos/Florges.png"), Cuadro("Elementos/Florges.png")],
    [Cuadro("Elementos/Krabby.png"), Cuadro("Elementos/Krabby.png"),
    Cuadro("Elementos/Miraidon.png"), Cuadro("Elementos/Miraidon.png")],
    [Cuadro("Elementos/Yveltal.png"), Cuadro("Elementos/Yveltal.png"),
    Cuadro("Elementos/Toxapex.png"), Cuadro("Elementos/Toxapex.png")],
]

#Definir colores
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREY  = ( 206, 206, 206)
BLUE  = (  30, 136, 229)

#Sonidos
sond_fondo= pygame.mixer.Sound("Elementos/fondo.mp3")
sond_clic= pygame.mixer.Sound("Elementos/clic.mp3")
sond_ganador= pygame.mixer.Sound("Elementos/ganador.mp3")
sond_error= pygame.mixer.Sound("Elementos/error.mp3")
sond_vuelta= pygame.mixer.Sound("Elementos/vuelta.mp3")

#Calculo de tamaño de la pantalla
ancho_ptn = len(cuadros[0]) * medida_Cuadro
altura_ptn = (len(cuadros) * medida_Cuadro)+alt_Boton
anchura_btn = ancho_ptn

#Fuente del btn
tmn_fuente = 20
fuente = pygame.font.SysFont("Arial", tmn_fuente)
xFuente = int((anchura_btn/2)-(tmn_fuente/2))
yFuente = int(altura_ptn - alt_Boton)

#Boton
boton = pygame.Rect(0, altura_ptn - alt_Boton, anchura_btn, altura_ptn)

#Indicadores
ultimos_segs = None
puede_jugar = True

juego_iniciado= False

#Indicadores para las tarjetas son pares
x1= None
y1= None
x2= None
y2= None

#Ocultar cuadros
def oculta_todos_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False
#Mezclar el juego
def mezclar_cuadros():
    cant_filas = len(cuadros)
    cant_columnas = len(cuadros[0])
    for y in range(cant_filas):
        for x in range(cant_columnas):
            x_random = random.randint(0, cant_columnas - 1)
            y_random = random.randint(0, cant_filas - 1)
            cuadro_temp = cuadros[y][x]
            cuadros[y][x]= cuadros[y_random][x_random]
            cuadros[y_random][x_random]= cuadro_temp

#Def para validar si ganó
def validar_victoria():
    if victoria():
        pygame.mixer.Sound.play(sond_ganador)
        reiniciar_juego()

def victoria():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True

def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False



#Def iniciar el juego
def iniciar_juego():
    pygame.mixer.Sound.play(sond_clic)
    global juego_iniciado
    #Para mezclar x veces
    for i in range (3):
        mezclar_cuadros()
    oculta_todos_cuadros()
    juego_iniciado = True

#Creacion de ventana
pantalla_juego = pygame.display.set_mode((ancho_ptn,altura_ptn))
pygame.display.set_caption('Poke-Memoria')
pygame.mixer.Sound.play(sond_fondo, -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:
            #X e Y Abslto son las coords del click
            xAbslto, yAbslto = event.pos
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()
            else:
                if not juego_iniciado:
                    continue
                #Este math floor permite calcular las posiciones de los cuadros e indicar que imagen clicamos
                x = math.floor(xAbslto/medida_Cuadro)
                y = math.floor(yAbslto/medida_Cuadro)
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierto:
                    continue
                if x1 is None and y1 is None:
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                    pygame.mixer.Sound.play(sond_vuelta)
                else:
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                #Comparacion si los cuadros dados vuelta son iguales
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        cuadros[y1][x1].descubierto = True
                        cuadros[y2][x2].descubierto = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                        pygame.mixer.Sound.play(sond_clic)
                    else:
                        pygame.mixer.Sound.play(sond_error)
                        ultimos_segs = int(time.time())
                        puede_jugar = False
                validar_victoria()
    ahora = int(time.time())

    if ultimos_segs is not None and ahora - ultimos_segs >= segs_visible_carta:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        x2 = None
        y1 = None
        y2 = None
        ultimos_segs = None
        puede_jugar = True

    #Colorear la pantalla
    pantalla_juego.fill(WHITE)

    x=0
    y=0
    for fila in cuadros:
        x=0
        for cuadro in fila:
            if cuadro.descubierto or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x,y))
            else:
                pantalla_juego.blit(imagen_oculta, (x,y))
            x+=medida_Cuadro
        y+=medida_Cuadro

    if juego_iniciado:
        pygame.draw.rect(pantalla_juego, WHITE, boton)
        pantalla_juego.blit(fuente.render("Iniciar juego", True, GREY), (xFuente,yFuente))
    else:
        pygame.draw.rect(pantalla_juego, BLUE, boton)
        pantalla_juego.blit(fuente.render("Iniciar juego", True, WHITE), (xFuente,yFuente))

    pygame.display.update()
    

