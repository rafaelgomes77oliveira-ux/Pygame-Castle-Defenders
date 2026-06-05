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
velocidade_inimigo = 1

class Inimigo:
    def __init__(self, nome, vida, x, y, imagem):
        self.nome = nome
        self.vida = vida

        self.imagem = pygame.image.load(imagem).convert_alpha()

        self.rect = self.imagem.get_rect()
        self.rect.x = x
        self.rect.y = y

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)
        
inimigo = Inimigo("Enzo", 100, 300, 200, "inimigo.png" )

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

        tela.blit(inimigo, (int(inimigo['x']) - inimigo.get_width(20) // 2, int(inimigo['y']) - inimigo.get_height(20) // 2))

    posição_mouse = pygame.mouse.get_pos()
    pygame.draw.circle(tela, (255, 0, 0), posição_mouse, 20)
    pygame.draw.circle(tela, (50, 50, 50), (centro_x, centro_y), 10)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()