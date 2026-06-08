import pygame
import sys
from src import config
from src.entidades import Torre
from src.dados import carregar_pontos, salvar_pontos
from src import funcoes

def executar_jogo():
    pygame.init()

    def resetar_jogo():
        global torre, dicionario_inimigos, pontos_sessao
        torre = Torre(config.centro_x, config.centro_y)
        dicionario_inimigos = {}
        pontos_sessao = 0

    pontos = carregar_pontos()
    pontos_sessao = 0

    tela_fundo = pygame.image.load("assets/imagens/Background-prototipo.png").convert()
    tela_fundo = pygame.transform.scale(tela_fundo, (config.largura, config.altura))
    botao_play = pygame.image.load("assets/imagens/botao.png").convert_alpha()
    botao_play = pygame.transform.scale(botao_play, (100, 50))

    fonte_titulo  = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 60)
    fonte_media   = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 36)
    fonte_pequena = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 24)

    texto_titulo = fonte_titulo.render("Castle Defenders", True, (255, 255, 255))
    rect_titulo  = texto_titulo.get_rect(center=(config.centro_x, config.centro_y - 120))

    dicionario_inimigos = {}
    raio_ataque_mouse   = 20

    torre = Torre(config.centro_x, config.centro_y)

    evento_spawn = pygame.USEREVENT + 1
    pygame.time.set_timer(evento_spawn, 800)

    estado_jogo = "menu"

    rodando = True
    relogio  = pygame.time.Clock()
    pygame.display.set_caption("Castle Defenders")

    while rodando:
        posicao_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if estado_jogo == "menu":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    rect_botao = botao_play.get_rect(topleft=(config.largura // 2 - 50, config.altura // 2 - 25))
                    if rect_botao.collidepoint(posicao_mouse):
                        estado_jogo = "jogando"

            elif estado_jogo == "jogando":
                if evento.type == evento_spawn:
                    funcoes.spawn_inimigo(dicionario_inimigos)
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    funcoes.verificar_dano_mouse(posicao_mouse, raio_ataque_mouse, 10, dicionario_inimigos)

            elif estado_jogo == "game_over":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if rect_botao_replay.collidepoint(posicao_mouse):
                        resetar_jogo()
                        estado_jogo = "jogando"

        if estado_jogo == "menu":
            config.tela.fill((0, 0, 0))
            config.tela.blit(texto_titulo, rect_titulo)
            config.tela.blit(botao_play, (config.largura // 2 - 50, config.altura // 2 - 25))

        elif estado_jogo == "jogando":
            config.tela.blit(tela_fundo, (0, 0))

            for inimigo in list(dicionario_inimigos.keys()):
                if dicionario_inimigos[inimigo] <= 0:
                    pontos_sessao += 1
                    if pontos_sessao > pontos:
                        pontos = pontos_sessao
                        salvar_pontos(pontos)

                    del dicionario_inimigos[inimigo]
                    continue

                inimigo.update()
                config.tela.blit(inimigo.imagem, inimigo.rect)
                funcoes.verificar_colisao_inimigo(inimigo, torre)

            barra_x = config.centro_x - (torre.barra_vida_largura // 2)
            barra_y = torre.rect.top - 20
            largura_atual_barra = (torre.vida / torre.vida_maxima) * torre.barra_vida_largura
            pygame.draw.rect(config.tela, (40, 40, 40),  (barra_x, barra_y, torre.barra_vida_largura, 12))
            pygame.draw.rect(config.tela, (255, 0, 0),   (barra_x, barra_y, largura_atual_barra, 12))

            config.tela.blit(torre.imagem, torre.rect)
            pygame.draw.circle(config.tela, (255, 0, 0), posicao_mouse, raio_ataque_mouse)

            txt_pts = fonte_media.render(f"{pontos_sessao}", True, (255, 255, 255))
            config.tela.blit(txt_pts, (20, 20))

            if torre.vida <= 0:
                estado_jogo = "game_over"

        elif estado_jogo == "game_over":
            config.tela.blit(tela_fundo, (0, 0))
            for inimigo in dicionario_inimigos:
                config.tela.blit(inimigo.imagem, inimigo.rect)
            config.tela.blit(torre.imagem, torre.rect)

            rect_botao_replay = funcoes.desenhar_tela_game_over(
                fonte_titulo, fonte_media, fonte_pequena, pontos_sessao, pontos
            )

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()