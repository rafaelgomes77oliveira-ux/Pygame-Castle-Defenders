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

imagem_torre = pygame.image.load("tower.png").convert_alpha()
imagem_torre = pygame.transform.scale(imagem_torre, (100, 100))

imagem_inimigo = pygame.image.load("enemy.png").convert_alpha()
imagem_inimigo = pygame.transform.scale(imagem_inimigo, (30, 60))

lista_inimigos = []
velocidade_inimigo = 3


class Torre:
    def __init__(self, x_centro, y_centro):
        self.imagem = imagem_torre
        self.rect = self.imagem.get_rect()
        self.rect.center = (x_centro, y_centro)


class Inimigo:
    def __init__(self, x_centro, y_centro, velocidade):
        self.imagem = imagem_inimigo
        self.rect = self.imagem.get_rect()

        angulo = random.uniform(0, 2 * math.pi)
        raio_spawn = max(largura, altura) // 2 + 50

        self.x = x_centro + raio_spawn * math.cos(angulo)
        self.y = y_centro + raio_spawn * math.sin(angulo)

        sentido_x = x_centro - self.x
        sentido_y = y_centro - self.y
        distancia = math.hypot(sentido_x, sentido_y)

        self.dx = (sentido_x / distancia) * velocidade
        self.dy = (sentido_y / distancia) * velocidade

        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))


torre = Torre(centro_x, centro_y)


def spawn_inimigo():
    novo_inimigo = Inimigo(centro_x, centro_y, velocidade_inimigo)
    lista_inimigos.append(novo_inimigo)


def verificar_colisao_inimigo(inimigo, torre):
    if inimigo.rect.colliderect(torre.rect):
        inimigo.dx = 0
        inimigo.dy = 0


evento_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(evento_spawn, 800)

rodando = True
relogio = pygame.time.Clock()
pygame.display.set_caption("Castle Defenders")

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == evento_spawn:
            spawn_inimigo()

    tela.fill((0, 0, 0))

    for inimigo in lista_inimigos:
        inimigo.update()
        tela.blit(inimigo.imagem, inimigo.rect)
        verificar_colisao_inimigo(inimigo, torre)

    posição_mouse = pygame.mouse.get_pos()
    pygame.draw.circle(tela, (255, 0, 0), posição_mouse, 20)
    tela.blit(torre.imagem, torre.rect)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()