import pygame
import random
import math
from src import config
from src import upgrades
from src import sprites
from src.dados import carregar_upgrades


class Torre:
    def __init__(self, x_centro, y_centro):
        self.imagem = sprites.imagem_torre
        self.rect = self.imagem.get_rect()
        self.rect.center = (x_centro, y_centro)
        self.vida = 100
        self.vida_maxima = 100
        self.barra_vida_largura = 100
        self.ratio_vida = self.barra_vida_largura / self.vida_maxima
        self.dano_ataque = 10
        self.raio_ataque = 20
        self.dinheiro = 0
        self.bonus_combo_por_acerto = 0.0  
        self.combo_atual = 0

        self.niveis_upgrades = carregar_upgrades()
        for u in upgrades.UPGRADES_TORRE:
            if u["id"] not in self.niveis_upgrades:
                self.niveis_upgrades[u["id"]] = 0

            nivel = self.niveis_upgrades[u["id"]]
            if nivel > 0:
                atributo = u["atributo"]
                valor_base = getattr(self, atributo)
                setattr(self, atributo, valor_base + (u["incremento"] * nivel))

        self.vida = self.vida_maxima
        self.atualizar_sprite()
    def atualizar_sprite(self):
        if self.niveis_upgrades.get("vida", 0) >= 5:
            self.imagem = sprites.imagem_torre2
        else:
            self.imagem = sprites.imagem_torre


class Inimigo:
    def __init__(self, x_centro, y_centro, dificuldade=1, eh_boss=False):
        self.eh_boss = eh_boss
        bonus = max(0, dificuldade - 1)
        if self.eh_boss:
            velocidade = 1.2 + min(bonus * 0.01, 1.2)
            vida = int(80 * (1 + bonus * 0.6))
            dano = int(15 * (1 + bonus * 0.4))
            self.pontos = 5 + bonus
            self.dinheiro = int(35 * (1 + bonus * 0.2))
            self.animacoes = sprites.ANIMACACOES_BOSS
        else:
            velocidade = 2 + min(bonus * 0.15, 2)
            vida = int(10 * (1 + bonus * 0.5))
            dano = int(5 * (1 + bonus * 0.3))
            self.pontos = 1
            self.dinheiro = int(5 * (1 + bonus * 0.2))
            self.animacoes = sprites.ANIMACACOES_INIMIGO

        self.vida = vida
        self.vida_maxima = vida
        self.dano = dano
        self.ultimo_ataque = 0

        self.estado = "andar"
        self.olhando_para = "direita"
        self.index_frame = 0
        self.ultima_atualizacao_frame = 0
        self.velocidade_animacao = 150

        self.frames_atuais = self.animacoes[self.olhando_para][self.estado]
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
        self.frames_atuais = self.animacoes[self.olhando_para][self.estado]

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

class InimigoCoxinha(Inimigo):
    def __init__(self, x_centro, y_centro, dificuldade=1, eh_boss=False):
        super().__init__(x_centro, y_centro, dificuldade, eh_boss)

        if self.eh_boss:
            self.animacoes = sprites.ANIMACOES_COXINHA_BOSS
            self.dano_explosao = 80 + (dificuldade * 15)
        else:
            self.animacoes = sprites.ANIMACOES_COXINHA
            self.dano_explosao = 30 + (dificuldade * 5)

        self.estado = "andar"
        self.frames_atuais = self.animacoes[self.olhando_para][self.estado]
        self.imagem = self.frames_atuais[0]
        self.explode = True

    def atualizar_animacao(self):
        self.frames_atuais = self.animacoes[self.olhando_para][self.estado]

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - getattr(self, 'ultimo_update_animacao', 0) > getattr(self, 'delay_animacao', 100):
            self.ultimo_update_animacao = tempo_atual
            self.index_frame += 1

            if self.index_frame >= len(self.frames_atuais):
                if self.estado == "explodir":
                    self.index_frame = len(self.frames_atuais) - 1
                else:
                    self.index_frame = 0

            self.imagem = self.frames_atuais[self.index_frame]