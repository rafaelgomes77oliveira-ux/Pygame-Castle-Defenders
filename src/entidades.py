import pygame
import random
import math
import config


imagem_torre = pygame.image.load("assets/imagens/tower.png").convert_alpha()
imagem_torre = pygame.transform.scale(imagem_torre, (200, 200))

imagem_inimigo = pygame.image.load("assets/imagens/Cultista-Sheet.png").convert_alpha()
imagem_inimigo = pygame.transform.scale(imagem_inimigo, (30, 60))


class Torre:
    def __init__(self, x_centro, y_centro):
        self.imagem = imagem_torre
        self.rect = self.imagem.get_rect()
        self.rect.center = (x_centro, y_centro)
        self.vida = 100
        self.vida_maxima = 100
        self.barra_vida_largura = 100
        self.ratio_vida = self.barra_vida_largura / self.vida_maxima


class Inimigo:
    def __init__(self, x_centro, y_centro, velocidade, imagem, vida, dano):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.vida = vida
        self.dano = dano
        self.ultimo_ataque = 0

        angulo = random.uniform(0, 2 * math.pi)
        raio_spawn = max(config.largura, config.altura) // 2 + 50

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


class InimigoCultista(Inimigo):
    def __init__(self, x_centro, y_centro):
        super().__init__(x_centro, y_centro, velocidade=2, imagem=imagem_inimigo, vida=10, dano=5)