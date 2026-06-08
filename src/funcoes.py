import pygame
import math
import config
from entidades import InimigoCultista

RAIO_CONTATO_TORRE = 90

def spawn_inimigo(dicionario_inimigos):
    novo_inimigo = InimigoCultista(config.centro_x, config.centro_y)
    dicionario_inimigos[novo_inimigo] = novo_inimigo.vida


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


def verificar_dano_mouse(pos_mouse, raio_circulo, dano_causado, dicionario_inimigos):
    for inimigo in list(dicionario_inimigos.keys()):
        distancia = math.hypot(pos_mouse[0] - inimigo.rect.centerx, pos_mouse[1] - inimigo.rect.centery)
        if distancia < (raio_circulo + inimigo.rect.width // 2):
            dicionario_inimigos[inimigo] -= dano_causado


def desenhar_tela_game_over(fonte_titulo, fonte_media, fonte_pequena, pontos_sessao, pontos):
    overlay = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    config.tela.blit(overlay, (0, 0))

    txt_over = fonte_titulo.render("GAME OVER", True, (220, 50, 50))
    config.tela.blit(txt_over, txt_over.get_rect(center=(config.centro_x, config.centro_y - 130)))

    txt_pontos = fonte_media.render(f"Inimigos abatidos: {pontos_sessao}", True, (255, 255, 255))
    config.tela.blit(txt_pontos, txt_pontos.get_rect(center=(config.centro_x, config.centro_y - 60)))

    txt_recorde = fonte_pequena.render(f"Recorde: {pontos}", True, (255, 220, 50))
    config.tela.blit(txt_recorde, txt_recorde.get_rect(center=(config.centro_x, config.centro_y - 20)))

    rect_replay = pygame.Rect(0, 0, 220, 52)
    rect_replay.center = (config.centro_x, config.centro_y + 60)
    mouse = pygame.mouse.get_pos()
    cor_botao = (80, 160, 80) if rect_replay.collidepoint(mouse) else (50, 120, 50)
    pygame.draw.rect(config.tela, cor_botao, rect_replay, border_radius=8)
    pygame.draw.rect(config.tela, (255, 255, 255), rect_replay, 2, border_radius=8)
    txt_replay = fonte_media.render("REPLAY", True, (255, 255, 255))
    config.tela.blit(txt_replay, txt_replay.get_rect(center=rect_replay.center))

    return rect_replay