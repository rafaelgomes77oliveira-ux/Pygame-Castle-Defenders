import pygame
from src import config
from src import upgrades


def desenhar_barra_vida_inimigo(inimigo):
    vida_atual = max(0, inimigo.vida)
    area_visivel = inimigo.imagem.get_bounding_rect(min_alpha=1)

    if area_visivel.width <= 0 or area_visivel.height <= 0:
        area_visivel = inimigo.imagem.get_rect()

    if inimigo.eh_boss:
        largura = 80
    else:
        largura = 40

    altura = 15 if inimigo.eh_boss else 5

    centro_x = inimigo.rect.left + area_visivel.centerx
    x = int(centro_x - largura // 2)
    y = int(inimigo.rect.top + area_visivel.top - altura - 4)

    proporcao = vida_atual / inimigo.vida_maxima
    cor_vida = (220, 40, 40) if inimigo.eh_boss else (80, 220, 90)

    pygame.draw.rect(config.tela, (35, 35, 35), (x, y, largura, altura))
    pygame.draw.rect(config.tela, cor_vida, (x, y, int(largura * proporcao), altura))


def desenhar_botao_upgrades(fonte_pequena):
    rect = pygame.Rect(config.largura - 290, 20, 260, 46)
    mouse = pygame.mouse.get_pos()
    cor = (100, 100, 100) if rect.collidepoint(mouse) else (50, 50, 50)
    pygame.draw.rect(config.tela, cor, rect, border_radius=5)
    pygame.draw.rect(config.tela, (255, 255, 255), rect, 2, border_radius=5)

    txt = fonte_pequena.render("Upgrades", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=rect.center)
    config.tela.blit(txt, txt_rect)
    return rect


def desenhar_tela_upgrades(fonte_titulo, fonte_media, fonte_pequena, torre):
    overlay = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    config.tela.blit(overlay, (0, 0))

    txt_titulo = fonte_titulo.render("UPGRADES", True, (255, 220, 50))
    config.tela.blit(txt_titulo, txt_titulo.get_rect(center=(config.centro_x, 100)))

    botoes_upgrades = {}
    y_offset = 250
    mouse = pygame.mouse.get_pos()

    for upg in upgrades.UPGRADES_TORRE:
        id_upg = upg["id"]
        nivel_atual = torre.niveis_upgrades.get(id_upg, 0)
        max_nivel = upg["nivel_maximo"]
        custo = upgrades.calcular_custo(upg, nivel_atual)

        info_texto = f"{upg['nome']} (Nivel {nivel_atual}/{max_nivel})"
        txt_info = fonte_media.render(info_texto, True, (255, 255, 255))
        config.tela.blit(txt_info, (config.centro_x - 450, y_offset))

        rect_comprar = pygame.Rect(config.centro_x + 150, y_offset - 5, 280, 50)

        if nivel_atual >= max_nivel:
            texto_botao = "MAX"
            cor_botao = (80, 80, 80)
        else:
            texto_botao = f"Comprar: {custo}"
            if torre.dinheiro >= custo:
                cor_botao = (80, 160, 80) if rect_comprar.collidepoint(mouse) else (40, 120, 40)
            else:
                cor_botao = (160, 80, 80) if rect_comprar.collidepoint(mouse) else (120, 40, 40)

        pygame.draw.rect(config.tela, cor_botao, rect_comprar, border_radius=8)
        pygame.draw.rect(config.tela, (255, 255, 255), rect_comprar, 2, border_radius=8)

        txt_b = fonte_pequena.render(texto_botao, True, (255, 255, 255))
        config.tela.blit(txt_b, txt_b.get_rect(center=rect_comprar.center))

        botoes_upgrades[id_upg] = rect_comprar
        y_offset += 120

    rect_voltar = pygame.Rect(config.centro_x - 120, config.altura - 150, 240, 60)
    cor_voltar = (100, 100, 100) if rect_voltar.collidepoint(mouse) else (60, 60, 60)
    pygame.draw.rect(config.tela, cor_voltar, rect_voltar, border_radius=8)
    pygame.draw.rect(config.tela, (255, 255, 255), rect_voltar, 2, border_radius=8)

    txt_v = fonte_pequena.render("Voltar", True, (255, 255, 255))
    config.tela.blit(txt_v, txt_v.get_rect(center=rect_voltar.center))

    return botoes_upgrades, rect_voltar


def desenhar_aviso_nivel(nivel, fonte_titulo):
    txt = fonte_titulo.render(f"NIVEL {nivel}", True, (255, 50, 50))
    config.tela.blit(txt, txt.get_rect(center=(config.centro_x, config.centro_y - 200)))


def desenhar_tela_game_over(fonte_titulo, fonte_media, fonte_pequena, moedas_retidas):
    overlay = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    config.tela.blit(overlay, (0, 0))

    txt_over = fonte_titulo.render("GAME OVER", True, (220, 50, 50))
    config.tela.blit(txt_over, txt_over.get_rect(center=(config.centro_x, config.centro_y - 130)))

    txt_moedas = fonte_media.render(f"Moedas Salvas: {moedas_retidas}", True, (255, 220, 50))
    config.tela.blit(txt_moedas, txt_moedas.get_rect(center=(config.centro_x, config.centro_y - 60)))

    rect_replay = pygame.Rect(0, 0, 280, 52)
    rect_replay.center = (config.centro_x, config.centro_y + 60)
    mouse = pygame.mouse.get_pos()
    cor_botao = (80, 160, 80) if rect_replay.collidepoint(mouse) else (50, 120, 50)
    pygame.draw.rect(config.tela, cor_botao, rect_replay, border_radius=8)
    pygame.draw.rect(config.tela, (255, 255, 255), rect_replay, 2, border_radius=8)

    txt_rep = fonte_pequena.render("Jogar De Novo", True, (255, 255, 255))
    config.tela.blit(txt_rep, txt_rep.get_rect(center=rect_replay.center))
    rect_novo_jogo_go = pygame.Rect(0, 0, 280, 52)
    rect_novo_jogo_go.center = (config.centro_x, config.centro_y + 130)
    cor_botao_nj = (100, 100, 100) if rect_novo_jogo_go.collidepoint(mouse) else (50, 50, 50)
    pygame.draw.rect(config.tela, cor_botao_nj, rect_novo_jogo_go, border_radius=8)
    pygame.draw.rect(config.tela, (255, 255, 255), rect_novo_jogo_go, 2, border_radius=8)

    txt_nj = fonte_pequena.render("Novo Jogo", True, (255, 255, 255))
    config.tela.blit(txt_nj, txt_nj.get_rect(center=rect_novo_jogo_go.center))

    return rect_replay, rect_novo_jogo_go