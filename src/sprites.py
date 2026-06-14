import pygame
from src import config

sprite_sheet_cultista = pygame.image.load("assets/imagens/Cultista-Sheet.png").convert_alpha()
TAMANHO_INIMIGO = (64, 64)
TAMANHO_BOSS = (128, 128)

frames_cultista = [sprite_sheet_cultista.subsurface((i * 192, 0, 192, 192)) for i in range(6)]

def criar_animacoes_cultista(tamanho):
    frames_cultista_direita = []
    frames_cultista_esquerda = []

    for frame in frames_cultista:
        frame_redimensionado = pygame.transform.scale(frame, tamanho)
        frames_cultista_direita.append(frame_redimensionado)
        frame_invertido = pygame.transform.flip(frame_redimensionado, True, False)
        frames_cultista_esquerda.append(frame_invertido)

    return {
        "direita": {
            "andar": frames_cultista_direita[0:2],
            "atacar": frames_cultista_direita[2:6]
        },
        "esquerda": {
            "andar": frames_cultista_esquerda[0:2],
            "atacar": frames_cultista_esquerda[2:6]
        }
    }

ANIMACACOES_INIMIGO = criar_animacoes_cultista(TAMANHO_INIMIGO)
ANIMACACOES_BOSS = criar_animacoes_cultista(TAMANHO_BOSS)

imagem_torre = pygame.image.load("assets/imagens/tower.png").convert_alpha()
imagem_torre = pygame.transform.scale(imagem_torre, (200, 200))

tela_fundo = pygame.image.load("assets/imagens/Background-prototipo.png").convert()
tela_fundo = pygame.transform.scale(tela_fundo, (config.largura, config.altura))

botao_play = pygame.image.load("assets/imagens/botao.png").convert_alpha()
botao_play = pygame.transform.scale(botao_play, (100, 50))
