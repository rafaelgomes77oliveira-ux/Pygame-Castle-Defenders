import pygame
import math
from src import config
from src.entidades import Inimigo
from src import upgrades

RAIO_CONTATO_TORRE = 90
SEGUNDOS_POR_NIVEL = 20
INTERVALO_BOSS_MS = 45000
SPAWN_INICIAL_MS = 800
SPAWN_MINIMO_MS = 300
REDUCAO_SPAWN_POR_NIVEL_MS = 70


def calcular_intervalo_spawn(dificuldade):
    reducao = (dificuldade - 1) * REDUCAO_SPAWN_POR_NIVEL_MS
    return max(SPAWN_MINIMO_MS, SPAWN_INICIAL_MS - reducao)


def formatar_tempo(segundos_decorridos):
    minutos = segundos_decorridos // 60
    segundos = segundos_decorridos % 60
    return f"{minutos:02d}:{segundos:02d}"


def spawn_inimigo(lista_inimigos, dificuldade=1, boss=False):
    novo_inimigo = Inimigo(config.centro_x, config.centro_y, dificuldade, boss)
    lista_inimigos.append(novo_inimigo)


def verificar_colisao_inimigo(inimigo, torre):
    distancia = math.hypot(
        inimigo.rect.centerx - torre.rect.centerx,
        inimigo.rect.centery - torre.rect.centery
    )

    if distancia <= RAIO_CONTATO_TORRE:
        inimigo.dx = 0
        inimigo.dy = 0

        if inimigo.estado != "atacar":
            inimigo.estado = "atacar"
            inimigo.index_frame = 0

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - inimigo.ultimo_ataque >= 1000:
            torre.vida -= inimigo.dano
            inimigo.ultimo_ataque = tempo_atual


def verificar_dano_mouse(pos_mouse, raio_circulo, torre, lista_inimigos):
    inimigos_alcancados = []

    for inimigo in lista_inimigos:
        distancia = math.hypot(pos_mouse[0] - inimigo.rect.centerx, pos_mouse[1] - inimigo.rect.centery)
        if distancia < (raio_circulo + inimigo.rect.width // 2):
            inimigos_alcancados.append(inimigo)

    dano = upgrades.processar_ataque(torre, len(inimigos_alcancados) > 0)
    for inimigo in inimigos_alcancados:
        inimigo.vida -= dano