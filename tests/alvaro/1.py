import pygame
import sys
import random
import math

pygame.init()
largura = 1920
altura = 1020
tela = pygame.display.set_mode((largura, altura))
centro_x = largura // 2
centro_y = altura // 2
lista_inimigos = []
velocidade_inimigo = 3

pygame.mixer.music.load(r"C:\Users\silva\Pygame-Castle-Defenders\assets\sons\BeepBox-Song.wav")
pygame.mixer.music.play(-1)

img_inimigo = pygame.image.load(r"C:\Users\silva\Pygame-Castle-Defenders\tests\joao\enemy.png").convert_alpha()
img_inimigo = pygame.transform.scale(img_inimigo, (30,60))
img_torre = pygame.image.load(r"C:\Users\silva\Pygame-Castle-Defenders\tests\joao\tower.png").convert_alpha()
img_torre = pygame.transform.scale(img_torre, (100,100))

torre_rect = img_torre.get_rect()
torre_rect.center = (centro_x, centro_y)

def spawn_inimigo():
    angulo = random.uniform(0, 2 * math.pi)
    raio_spawn = max(largura, altura) // 2 + 50

    x = centro_x + raio_spawn * math.cos(angulo)
    y = centro_y + raio_spawn * math.sin(angulo)

    sentido_x = centro_x - x
    sentido_y = centro_y - y

    distancia = math.hypot(sentido_x, sentido_y)

    dx = (sentido_x / distancia) * velocidade_inimigo
    dy = (sentido_y / distancia) * velocidade_inimigo

    lista_inimigos.append({'x': x, 'y': y, 'dx': dx, 'dy': dy})

def verificar_colisao_inimigo(inimigo, torre_rect):
    inimigo_rect = img_inimigo.get_rect()
    inimigo_rect.center = (int(inimigo['x']), int(inimigo['y']))
    
    if inimigo_rect.colliderect(torre_rect):
        inimigo['dx'] = 0
        inimigo['dy'] = 0

EVENTO_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_SPAWN, 800)

rodando = True
relogio = pygame.time.Clock()
pygame.display.set_caption("Castle Defenders")

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == EVENTO_SPAWN:
            spawn_inimigo()

    tela.fill((0, 0, 0))

    for inimigo in lista_inimigos:
        inimigo['x'] += inimigo['dx']
        inimigo['y'] += inimigo['dy']

        inimigo_rect = img_inimigo.get_rect()
        inimigo_rect.center = (int(inimigo['x']), int(inimigo['y']))
        tela.blit(img_inimigo, inimigo_rect)

        verificar_colisao_inimigo(inimigo, torre_rect)

    posição_mouse = pygame.mouse.get_pos()
    pygame.draw.circle(tela, (255, 0, 0), posição_mouse, 20)
    tela.blit(img_torre, torre_rect)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()