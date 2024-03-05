import pygame
import random
import math
import io
from pygame import mixer

# Inicializar PYGAME
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.ico")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo.jpg")

# Agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variables Jugador
img_jugador = pygame.image.load("Cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
jugador_y_cambio = 0

# Variables Alien
img_alien = []
alien_x = []
alien_y = []
alien_x_cambio = []
alien_y_cambio = []
cantidad_alien = 6

for e in range(cantidad_alien):
    img_alien.append(pygame.image.load("Alien.png"))
    alien_x.append(random.randint(0, 736))
    alien_y.append(random.randint(50, 200))
    alien_x_cambio.append(0.5)
    alien_y_cambio.append(50)

# Variables Meteorito
img_meteorito = []
meteorito_x = []
meteorito_y = []
meteorito_x_cambio = []
meteorito_y_cambio = []
cantidad_meteorito = 3

for m in range(cantidad_meteorito):
    img_meteorito.append(pygame.image.load("asteroide.png"))
    meteorito_x.append(random.randint(0, 736))
    meteorito_y.append(random.randint(58, 236))
    meteorito_x_cambio.append(0.8)
    meteorito_y_cambio.append(55)

# Variables Bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# Variable explosion

col = 0
cont = 0
img1_explosion = pygame.image.load('explosion1.png')
explosion_x = 0
explosion_y = 0

# Variable Puntuacion
puntuacion = 0

# Funcion Fuente Bytes
def fuente_bytes(fuente):
    with open(fuente,'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

#Fuente

fuente_como_bytes = fuente_bytes("Honk-Regular.ttf")
fuente = pygame.font.Font('Honk-Regular.ttf', 32)
text_x = 10
text_y = 10


# Texto final de juego
fuente_final = pygame.font.Font(fuente_como_bytes, 80)


def texto_final():
    mi_fuente_final = fuente_final.render('GAME OVER', True, (242, 221, 255, 100))
    pantalla.blit(mi_fuente_final, (220, 200))


# Funcion mostrar puntuacion
def mostrar_puntuacion(x, y):
    texto = fuente.render(f'PUNTUACION: {puntuacion}', True, (242, 221, 255, 100))
    pantalla.blit(texto, (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion Alien
def alien(x, y, ene):
    pantalla.blit(img_alien[ene], (x, y))


# Funcion Meteorito
def meteorito(x, y, met):
    pantalla.blit(img_meteorito[met], (x, y))


# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False
# Variable estado del juego
juego_activo = True

# Loop del juego
se_ejecuta = True
while se_ejecuta and juego_activo:

    # Imagen
    pantalla.blit(fondo, (0, 0))

    # Iterar EVENTOS
    for evento in pygame.event.get():

        # Iterar Cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento PRESIONAR FLECHAS
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                jugador_y_cambio = -1
            if evento.key == pygame.K_DOWN:
                jugador_y_cambio = 1
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.set_volume(0.3)
                sonido_bala.play()
                nueva_bala = {'x': jugador_x, 'y': jugador_y, 'velocidad': -3}
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        # Evento SOLTAR FLECHAS
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                jugador_y_cambio = 0
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    # Modificar ubicacion
    jugador_x += jugador_x_cambio
    jugador_y += jugador_y_cambio

    # Mantener dentro bordes
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    elif jugador_y <= 336:
        jugador_y = 336
    elif jugador_y >= 536:
        jugador_y = 536

    # Modificar ubicacion alien
    for e in range(cantidad_alien):
        alien_x[e] += alien_x_cambio[e]
        if hay_colision(alien_x[e], alien_y[e], jugador_x, jugador_y):
            juego_activo = False
            break
    # Mantener dentro bordes alien
        if alien_x[e] <= 0:
            alien_x_cambio[e] = 1
            alien_y[e] += alien_y_cambio[e]
        elif alien_x[e] >= 736:
            alien_x_cambio[e] = -1
            alien_y[e] += alien_y_cambio[e]
            # Colision alien
        for bala in balas:
            colision_bala_alien = hay_colision(alien_x[e], alien_y[e], bala["x"], bala["y"])
            if colision_bala_alien:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntuacion += 1
                alien_x[e] = random.randint(0, 736)
                alien_y[e] = random.randint(20, 200)
                break

        alien(alien_x[e], alien_y[e], e)

    # Modificar ubicacion meteorito
    for m in range(cantidad_meteorito):
        meteorito_x[m] += meteorito_x_cambio[m]
        if hay_colision(meteorito_x[m], meteorito_y[m], jugador_x, jugador_y):
            juego_activo = False
            break
        # Mantener dentro bordes meteorito
        if meteorito_x[m] <= 0:
            meteorito_x_cambio[m] = 1
            meteorito_y[m] += meteorito_y_cambio[m]
        elif meteorito_x[m] >= 736:
            meteorito_x_cambio[m] = -1
            meteorito_y[m] += meteorito_y_cambio[m]
            # Colision meteorito
        for bala in balas:
            colision_bala_meteorito = hay_colision(meteorito_x[m], meteorito_y[m], bala["x"], bala["y"])
            if colision_bala_meteorito:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntuacion += 2
                meteorito_x[m] = random.randint(0, 736)
                meteorito_y[m] = random.randint(20, 200)
                break

        meteorito(meteorito_x[m], meteorito_y[m], m)

    # Detencion del juego
    if not juego_activo:
        texto_final()
        for k in range(cantidad_alien):
            alien_y[k] = 1000
        for t in range(cantidad_meteorito):
            meteorito_y[t] = 1000

    # Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntuacion(text_x, text_y)

    # Actualizar
    pygame.display.update()
