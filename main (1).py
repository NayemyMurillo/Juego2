import pygame
import random
import math

#inicializando la libreria
pygame.init()
#reloj
reloj=pygame.time.Clock()
FPS=60
#creacion de la ventana
ancho = 1500
alto = 900
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Cat, run!")

# Música de fondo
#pygame.mixer.music.load("musica.mpeg")
#pygame.mixer.music.play(-1)

# Logo del juego
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

#IMAGENES JUGADOR:
#escalas
scala_personaje=2
scala_arma=1

#funcion para escalar una nueva imagen 
def escalar(image, scale):
    al_personaje=image.get_width()
    an_personaje=image.get_height()
    imagen_escalada=pygame.transform.scale(image,(al_personaje*scale,an_personaje*scale))
    return imagen_escalada

#cambios de imagen de jugador
jugador_animaciones=[]
for i in range(1,7):
    cambios=pygame.image.load(f"run//cat{i}.png")
    cambios=escalar(cambios,scala_personaje)
    jugador_animaciones.append(cambios)


#IMAGEN ARMA Y BALA:
arma_imagen=pygame.image.load("arma3.png").convert_alpha()
arma_imagen=escalar(arma_imagen,scala_arma)

#bala_imagen=pygame.image.load("bala.png")

#IMAGENES ENEMIGOS:
#FONDOS:
background = pygame.image.load("fondo1.png")
game_over = pygame.image.load("gameover.png")

#IMAGENES ITEMS:
moneda_image = pygame.image.load("moneda.png").convert_alpha()

#IMAGENES SONIDO:
sonido_abajo = pygame.image.load("bajar.png").convert_alpha()
sonido_mute = pygame.image.load("apagado.png").convert_alpha()
sonido_subir = pygame.image.load("subir.png").convert_alpha()

#IMAGENES: (FALTA PISTOLA)

#VARIABLES DE CAMBIO
alto_personaje=90
ancho_personaje=90
#MOVIMIENTO DEL JUGADOR
arriba=False
abajo=False
izquierda=False
derecha=False
velocidad_jugador=10

#TIEMPO
clock = pygame.time.Clock()
score = 0
#LOOP
loop = True
fondo_x = 0
fondo_velocidad = 8

#IMAGENES ITEMS:
monedas = []


#IMAGENES OBSTACULOS:
obstaculos = []
misiles = []  
obstaculos_linea = []

#NO SE QUE HACE ESTO
GENERAR_MONEDAS_EVENTO = pygame.USEREVENT + 1
GENERAR_OBSTACULO_EVENTO = pygame.USEREVENT + 2
GENERAR_MISIL_EVENTO = pygame.USEREVENT + 3  
GENERAR_LINEA_EVENTO = pygame.USEREVENT + 4

class Jugador:
    def __init__(self, x, y,animaciones):
        self.flip=False
        self.animaciones=animaciones
        self.frame_index=1
        #imagen que se muestra en la actualidad
        self.image=animaciones[self.frame_index]
        self.update_time=pygame.time.get_ticks()
        self.forma= self.image.get_rect()
        self.forma.center=(x,y)
        
    def actualizar(self):
        tiempo_animacion=100
        self.image=self.animaciones[self.frame_index]
        if pygame.time.get_ticks()- self.update_time >= tiempo_animacion:
            self.frame_index=self.frame_index +1 #actualizacion cada milisegundo
            self.update_time=pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index=1

    def movimiento(self, pos_x, pos_y):
        if pos_x < 0: #va a la izquierda
            self.flip=True
        if pos_x > 0: #va a la derecha
            self.flip=False
        self.forma.x = self.forma.x + pos_x
        self.forma.y = self.forma.y + pos_y
    
    def mirar(self,interfaz):
        imagen_flip=pygame.transform.flip(self.image,self.flip,False)
        interfaz.blit(imagen_flip,self.forma)
        #pygame.draw.rect(interfaz, (255, 255, 0), self.forma,1)

    def disparo(self):
        pass

# Cambios en la clase de disparos
class Arma:
    def __init__(self,image):
        self.image_original = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.image_original,self.angle)
        self.rect= self.image.get_rect()#encapsular

    def actualizar_arma(self,personaje):
        self.rect.center=personaje.forma.center
        if personaje.flip ==False:
            self.rect.x += personaje.forma.width/2
            self.rotacion_personaje(False)
        else: 
            self.rect.x -= personaje.forma.width/2
            self.rotacion_personaje(True)

        #mover mouse
        posicion_mouse=pygame.mouse.get_pos()
        diferencia_x=posicion_mouse[0] - self.rect.centerx
        diferencia_y=- (posicion_mouse[1] - self.rect.centery)
        self.angle= math.degrees(math.atan2(diferencia_y,diferencia_x)) #arco tng

    def mirar(self,ventana):
        self.image=pygame.transform.rotate(self.image,self.angle)
        ventana.blit(self.image,self.rect)
        #pygame.draw.rect(ventana, (255, 255, 0), self.rect,1)
    
    def rotacion_personaje(self,rotando):
        if rotando==True:
            imagen_flip= pygame.transform.flip(self.image_original,True, False)
            self.image = pygame.transform.rotate(imagen_flip,self.angle)
        else:
            imagen_flip= pygame.transform.flip(self.image_original,False, False)
            self.image = pygame.transform.rotate(imagen_flip,self.angle)

        
#INICIALIZAMOS OBJETOS:
jugador = Jugador(90,450,jugador_animaciones)
arma=Arma(arma_imagen)


#PANTALLA
def pantalla():
    #fondo
    global fondo_x
    fondo_avanza = fondo_x % background.get_rect().width
    screen.blit(background, (fondo_avanza - background.get_rect().width, 0))
    if fondo_avanza < ancho:
        screen.blit(background, (fondo_avanza, 0))
    fondo_x -= fondo_velocidad
    

#BUCLE PRINCIPAL: Es decir un loop
while loop:
    reloj.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    #fondo
    #calculo del movimiento
        delta_x=0
        delta_y=0
        if derecha==True:
            delta_x=velocidad_jugador
        if izquierda==True:
            delta_x=-velocidad_jugador
        if arriba==True:
            delta_y=-velocidad_jugador
        if abajo==True:
            delta_y=velocidad_jugador
#COMANDOS:
        keys = pygame.key.get_pressed()
        if event.type==pygame.KEYDOWN:
        #cuando el jugador toque la tecla
            if event.key ==pygame.K_a:
                izquierda=True
            if event.key ==pygame.K_d:
                derecha=True
            if event.key ==pygame.K_s:
                abajo=True
            if event.key ==pygame.K_w:
                arriba=True
        #cuando el jugador deje de tocar la tecla
        if event.type== pygame.KEYUP:
            if event.key ==pygame.K_a:
                izquierda=False
            if event.key ==pygame.K_d:
                derecha=False
            if event.key ==pygame.K_s:
                abajo=False
            if event.key ==pygame.K_w: 
                arriba=False
        #mover al jugador

    #teclas de la musica
        #Volumen baja
        if keys[pygame.K_o] and pygame.mixer.music.get_volume() > 0.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
            screen.blit(sonido_abajo, (100, 87))
        elif keys[pygame.K_o] and pygame.mixer.music.get_volume() == 0.0:
            screen.blit(sonido_mute, (100, 87))
        # Volumen sube
        if keys[pygame.K_p] and pygame.mixer.music.get_volume() < 1.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
            screen.blit(sonido_subir, (100, 87))
        # Desactivar volumen 
        elif keys[pygame.K_i]:
            pygame.mixer.music.set_volume(0.0)
            screen.blit(sonido_mute, (100, 87))

    pantalla()
    jugador.movimiento(delta_x,delta_y)
    jugador.actualizar()
    jugador.mirar(screen)
    arma.actualizar_arma(jugador)
    arma.mirar(screen)
    pygame.display.update()


pygame.quit()



   