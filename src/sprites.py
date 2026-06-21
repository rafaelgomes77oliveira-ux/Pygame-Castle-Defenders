import pygame
from src import config

sprite_sheet_cultista = pygame.image.load("assets/imagens/cultista-sheet.png").convert_alpha()
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

imagem_torre = pygame.image.load("assets/imagens/torre.png").convert_alpha()
imagem_torre = pygame.transform.scale(imagem_torre, (200, 200))

imagem_torre2 = pygame.image.load("assets/imagens/torre2.png").convert_alpha()
imagem_torre2 = pygame.transform.scale(imagem_torre2, (200, 200))

X_besta = pygame.image.load("assets/imagens/x-besta.png").convert_alpha()
X_besta = pygame.transform.scale(X_besta, (200, 200))

imagem_sombra_torre = pygame.image.load("assets/imagens/sombra.png").convert_alpha()
imagem_sombra_torre = pygame.transform.scale(imagem_sombra_torre, (200, 200))

tela_fundo = pygame.image.load("assets/imagens/background.png").convert()
tela_fundo = pygame.transform.scale(tela_fundo, (config.largura, config.altura))

botao_play = pygame.image.load("assets/imagens/botao.png").convert_alpha()
botao_play = pygame.transform.scale(botao_play, (100, 100))

sprite_sheet_coxinha = pygame.image.load("assets/imagens/coxinha-sheet.png").convert_alpha()

LARGURA_FRAME_COXINHA = 32
ALTURA_FRAME_COXINHA = 32

frames_coxinha_brutos = [sprite_sheet_coxinha.subsurface((i * LARGURA_FRAME_COXINHA, 0, LARGURA_FRAME_COXINHA, ALTURA_FRAME_COXINHA)) for i in range(8)]

def criar_animacoes_coxinha(tamanho):
    frames_direita = []
    frames_esquerda = []

    for frame in frames_coxinha_brutos:
        frame_redimensionado = pygame.transform.scale(frame, tamanho)
        frames_direita.append(frame_redimensionado)

        frame_invertido = pygame.transform.flip(frame_redimensionado, True, False)
        frames_esquerda.append(frame_invertido)

    return {
        "esquerda": {
            "andar": frames_direita[0:4],
            "explodir": frames_direita[4:8]
        },
        "direita": {
            "andar": frames_esquerda[0:4],
            "explodir": frames_esquerda[4:8]
        }
    }

ANIMACOES_COXINHA = criar_animacoes_coxinha(TAMANHO_INIMIGO)
ANIMACOES_COXINHA_BOSS = criar_animacoes_coxinha(TAMANHO_BOSS)

sprite_sheet_cursor = pygame.image.load("assets/imagens/cursor-sheet.png").convert_alpha()
largura_cursor = sprite_sheet_cursor.get_width() // 4
altura_cursor = sprite_sheet_cursor.get_height()

frames_cursor_brutos = [
    sprite_sheet_cursor.subsurface((i * largura_cursor, 0, largura_cursor, altura_cursor))
    for i in range(4)
]
