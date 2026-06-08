import pygame
import random
import math
from src import config


sprite_sheet_cultista = pygame.image.load("assets/imagens/Cultista-Sheet.png").convert_alpha()
TAMANHO_JOGO = (64, 64)

frames_cultista = [sprite_sheet_cultista.subsurface((i * 192, 0, 192, 192)) for i in range(6)]

frames_cultista_direita = []
frames_cultista_esquerda = []

for frame in frames_cultista:
    frame_redimensionado = pygame.transform.scale(frame, TAMANHO_JOGO)
    frames_cultista_direita.append(frame_redimensionado)
    frame_invertido = pygame.transform.flip(frame_redimensionado, True, False)
    frames_cultista_esquerda.append(frame_invertido)

ANIMACACOES = {
    "direita": {
        "andar": frames_cultista_direita[0:2],
        "atacar": frames_cultista_direita[2:6]
    },
    "esquerda": {
        "andar": frames_cultista_esquerda[0:2],
        "atacar": frames_cultista_esquerda[2:6]
    }
}

imagem_torre = pygame.image.load("assets/imagens/tower.png").convert_alpha()
imagem_torre = pygame.transform.scale(imagem_torre, (200, 200))


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
    def __init__(self, x_centro, y_centro, velocidade, vida, dano):
        self.vida = vida
        self.dano = dano
        self.ultimo_ataque = 0

        self.estado = "andar"
        self.olhando_para = "direita"
        self.index_frame = 0
        self.ultima_atualizacao_frame = 0
        self.velocidade_animacao = 150

        self.frames_atuais = ANIMACACOES[self.olhando_para][self.estado]
        self.imagem = self.frames_atuais[self.index_frame]
        self.rect = self.imagem.get_rect()

        angulo = random.uniform(0, 2 * math.pi)
        raio_spawn = max(config.largura, config.altura) // 2 + 50

        self.x = x_centro + raio_spawn * math.cos(angulo)
        self.y = y_centro + raio_spawn * math.sin(angulo)

        sentido_x = x_centro - self.x
        sentido_y = y_centro - self.y
        distancia = math.hypot(sentido_x, sentido_y)

        self.dx = (sentido_x / distancia) * velocidade
        self.dy = (sentido_y / distancia) * velocidade

        if self.dx < 0:
            self.olhando_para = "esquerda"
        else:
            self.olhando_para = "direita"

        self.rect.center = (int(self.x), int(self.y))

    def atualizar_animacao(self):
        self.frames_atuais = ANIMACACOES[self.olhando_para][self.estado]

        if self.index_frame >= len(self.frames_atuais):
            self.index_frame = 0

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultima_atualizacao_frame > self.velocidade_animacao:
            self.index_frame = (self.index_frame + 1) % len(self.frames_atuais)
            self.imagem = self.frames_atuais[self.index_frame]
            self.ultima_atualizacao_frame = tempo_atual

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))
        self.atualizar_animacao()


class InimigoCultista(Inimigo):
    def __init__(self, x_centro, y_centro):
        super().__init__(x_centro, y_centro, velocidade=2, vida=10, dano=5)