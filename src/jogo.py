import pygame
import sys
from src import config
from src.entidades import Torre, AnimacaoAtaque
from src.dados import carregar_moedas, salvar_moedas, carregar_nivel, salvar_nivel, salvar_upgrades
from src import funcoes
from src import upgrades
from src import sprites
from src import ui

def executar_jogo():
    pygame.init()

    fonte_titulo  = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 60)
    fonte_media   = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 36)
    fonte_pequena = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 24)

    texto_titulo = fonte_titulo.render("Castle Defenders", True, (255, 255, 255))
    rect_titulo  = texto_titulo.get_rect(center=(config.centro_x, config.centro_y - 120))

    lista_inimigos = []
    animacoes_ataque = []
    torre = Torre(config.centro_x, config.centro_y)
    torre.dinheiro = carregar_moedas()

    evento_spawn = pygame.USEREVENT + 1
    pygame.time.set_timer(evento_spawn, 0)

    estado_jogo = "menu"
    tempo_inicio_partida = 0
    tempo_inicio_pausa = 0
    dificuldade_atual = carregar_nivel()
    intervalo_spawn_atual = funcoes.calcular_intervalo_spawn(dificuldade_atual)
    proximo_boss_ms = 0
    tempo_aviso_nivel = 0

    rect_botao_replay = pygame.Rect(0, 0, 0, 0)
    rect_botao_novo_jogo_go = pygame.Rect(0, 0, 0, 0)
    rect_botao_upgrades = pygame.Rect(0, 0, 0, 0)
    rect_botao_voltar_upgrades = pygame.Rect(0, 0, 0, 0)
    rect_botao_novo_jogo = pygame.Rect(config.centro_x - 150, config.altura // 2 + 60, 300, 50)
    botoes_upgrades = {}

    rodando = True
    relogio = pygame.time.Clock()
    pygame.display.set_caption("Castle Defenders")

    while rodando:
        posicao_mouse = pygame.mouse.get_pos()
        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if estado_jogo == "menu":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    rect_play = sprites.botao_play.get_rect(topleft=(config.largura // 2 - 50, config.altura // 2 - 60 ))

                    if rect_play.collidepoint(posicao_mouse):
                        torre = Torre(config.centro_x, config.centro_y)
                        torre.dinheiro = carregar_moedas()
                        lista_inimigos.clear()
                        tempo_inicio_partida = pygame.time.get_ticks()
                        dificuldade_atual = carregar_nivel()
                        intervalo_spawn_atual = funcoes.calcular_intervalo_spawn(dificuldade_atual)
                        proximo_boss_ms = tempo_inicio_partida + funcoes.INTERVALO_BOSS_MS
                        tempo_aviso_nivel = 0
                        pygame.event.clear(evento_spawn)
                        pygame.time.set_timer(evento_spawn, intervalo_spawn_atual)
                        estado_jogo = "jogando"

                    elif rect_botao_novo_jogo.collidepoint(posicao_mouse):
                        salvar_moedas(0)
                        salvar_nivel(1)
                        salvar_upgrades({})

                        torre = Torre(config.centro_x, config.centro_y)
                        torre.dinheiro = 0
                        lista_inimigos.clear()
                        tempo_inicio_partida = pygame.time.get_ticks()
                        dificuldade_atual = 1
                        intervalo_spawn_atual = funcoes.calcular_intervalo_spawn(dificuldade_atual)
                        proximo_boss_ms = tempo_inicio_partida + funcoes.INTERVALO_BOSS_MS
                        tempo_aviso_nivel = 0
                        pygame.event.clear(evento_spawn)
                        pygame.time.set_timer(evento_spawn, intervalo_spawn_atual)
                        estado_jogo = "jogando"

            elif estado_jogo == "jogando":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_u:
                    tempo_inicio_pausa = pygame.time.get_ticks()
                    pygame.event.clear(evento_spawn)
                    pygame.time.set_timer(evento_spawn, 0)
                    estado_jogo = "upgrades"

                if evento.type == evento_spawn:
                    funcoes.spawn_inimigo(lista_inimigos, dificuldade_atual)

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if rect_botao_upgrades.collidepoint(posicao_mouse):
                        tempo_inicio_pausa = pygame.time.get_ticks()
                        estado_jogo = "upgrades"
                    else:
                        funcoes.verificar_dano_mouse(posicao_mouse, torre.raio_ataque, torre, lista_inimigos)
                        animacoes_ataque.append(AnimacaoAtaque(posicao_mouse[0], posicao_mouse[1], torre.raio_ataque))

            elif estado_jogo == "upgrades":
                if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_u):
                    tempo_pausado = pygame.time.get_ticks() - tempo_inicio_pausa
                    tempo_inicio_partida += tempo_pausado
                    proximo_boss_ms += tempo_pausado
                    pygame.event.clear(evento_spawn)
                    pygame.time.set_timer(evento_spawn, intervalo_spawn_atual)
                    estado_jogo = "jogando"

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if rect_botao_voltar_upgrades.collidepoint(posicao_mouse):
                        tempo_pausado = pygame.time.get_ticks() - tempo_inicio_pausa
                        tempo_inicio_partida += tempo_pausado
                        proximo_boss_ms += tempo_pausado
                        pygame.event.clear(evento_spawn)
                        pygame.time.set_timer(evento_spawn, intervalo_spawn_atual)
                        estado_jogo = "jogando"
                    else:
                        for id_upgrade, rect_botao in botoes_upgrades.items():
                            if rect_botao.collidepoint(posicao_mouse):
                                if upgrades.comprar_upgrade(torre, id_upgrade):
                                    salvar_moedas(torre.dinheiro)
                                    salvar_upgrades(torre.niveis_upgrades)
                                break

            elif estado_jogo == "game_over":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if rect_botao_replay.collidepoint(posicao_mouse):
                        torre = Torre(config.centro_x, config.centro_y)
                        torre.dinheiro = carregar_moedas()
                        lista_inimigos.clear()
                        tempo_inicio_partida = pygame.time.get_ticks()
                        dificuldade_atual = carregar_nivel()
                        intervalo_spawn_atual = funcoes.calcular_intervalo_spawn(dificuldade_atual)
                        proximo_boss_ms = tempo_inicio_partida + funcoes.INTERVALO_BOSS_MS
                        tempo_aviso_nivel = 0
                        pygame.event.clear(evento_spawn)
                        pygame.time.set_timer(evento_spawn, intervalo_spawn_atual)
                        estado_jogo = "jogando"
                    elif rect_botao_novo_jogo_go.collidepoint(posicao_mouse):
                        salvar_moedas(0)
                        salvar_nivel(1)
                        salvar_upgrades({})

                        torre = Torre(config.centro_x, config.centro_y)
                        torre.dinheiro = 0
                        lista_inimigos.clear()
                        tempo_inicio_partida = pygame.time.get_ticks()
                        dificuldade_atual = 1
                        intervalo_spawn_atual = funcoes.calcular_intervalo_spawn(dificuldade_atual)
                        proximo_boss_ms = tempo_inicio_partida + funcoes.INTERVALO_BOSS_MS
                        tempo_aviso_nivel = 0
                        pygame.event.clear(evento_spawn)
                        pygame.time.set_timer(evento_spawn, intervalo_spawn_atual)
                        estado_jogo = "jogando"

        if estado_jogo == "menu":
            config.tela.fill((0, 0, 0))
            config.tela.blit(texto_titulo, rect_titulo)
            config.tela.blit(sprites.botao_play, (config.largura // 2 - 50, config.altura // 2 - 60))

            cor_novo_jogo = (100, 100, 100) if rect_botao_novo_jogo.collidepoint(posicao_mouse) else (50, 50, 50)
            pygame.draw.rect(config.tela, cor_novo_jogo, rect_botao_novo_jogo, border_radius=8)
            pygame.draw.rect(config.tela, (255, 255, 255), rect_botao_novo_jogo, 2, border_radius=8)

            txt_nj = fonte_pequena.render("Novo Jogo", True, (255, 255, 255))
            config.tela.blit(txt_nj, txt_nj.get_rect(center=rect_botao_novo_jogo.center))

        elif estado_jogo == "jogando":
            segundos_decorridos = max(0, (tempo_atual - tempo_inicio_partida) // 1000)

            while proximo_boss_ms > 0 and tempo_atual >= proximo_boss_ms:
                funcoes.spawn_inimigo(lista_inimigos, dificuldade_atual, boss=True)
                proximo_boss_ms += funcoes.INTERVALO_BOSS_MS

            config.tela.blit(sprites.tela_fundo, (0, 0))

            for inimigo in lista_inimigos[:]:
                if inimigo.vida <= 0:
                    torre.dinheiro += inimigo.dinheiro
                    salvar_moedas(torre.dinheiro)

                    # REGRA: Quando um Boss é derrotado
                    if inimigo.eh_boss:
                        dificuldade_atual += 1
                        salvar_nivel(dificuldade_atual)
                        # Acelera o spawn dos inimigos comuns para a nova dificuldade
                        intervalo_spawn_atual = funcoes.calcular_intervalo_spawn(dificuldade_atual)
                        pygame.time.set_timer(evento_spawn, intervalo_spawn_atual)
                        tempo_aviso_nivel = tempo_atual + 3000
                        # Cura a torre em 40% da vida máxima
                        if (torre.vida + torre.vida_maxima * 0.4) > torre.vida_maxima:
                            torre.vida = torre.vida_maxima
                        else:
                            torre.vida += torre.vida_maxima * 0.4

                    lista_inimigos.remove(inimigo)
                    continue

                inimigo.update()
                config.tela.blit(inimigo.imagem, inimigo.rect)
                ui.desenhar_barra_vida_inimigo(inimigo)
                funcoes.verificar_colisao_inimigo(inimigo, torre)

            barra_x = config.centro_x - (torre.barra_vida_largura // 2)
            barra_y = torre.rect.top - 20
            largura_atual_barra = max(0, (torre.vida / torre.vida_maxima)) * torre.barra_vida_largura
            pygame.draw.rect(config.tela, (40, 40, 40),  (barra_x, barra_y, torre.barra_vida_largura, 12))
            pygame.draw.rect(config.tela, (255, 0, 0),   (barra_x, barra_y, largura_atual_barra, 12))

            config.tela.blit(torre.imagem_sombra, torre.rect_sombra)
            config.tela.blit(torre.imagem, torre.rect)
            if torre.niveis_upgrades.get("dano", 0) == 8:
                config.tela.blit(torre.X_besta, torre.rect_X_besta)

            for anim in animacoes_ataque[:]:
                anim.update()
                if anim.concluida:
                    animacoes_ataque.remove(anim)
                else:
                    config.tela.blit(anim.imagem, anim.rect)

            txt_tempo = fonte_pequena.render(f"Tempo: {funcoes.formatar_tempo(segundos_decorridos)}", True, (255, 255, 255))
            config.tela.blit(txt_tempo, (20, 60))
            txt_dificuldade = fonte_pequena.render(f"Nivel: {dificuldade_atual}", True, (255, 220, 50))
            config.tela.blit(txt_dificuldade, (20, 90))
            txt_moedas = fonte_pequena.render(f"Moedas: {torre.dinheiro}", True, (255, 220, 50))
            config.tela.blit(txt_moedas, (20, 120))

            combo_bonus_pct = int(torre.combo_atual * torre.bonus_combo_por_acerto * 100)
            txt_combo = fonte_pequena.render(
                f"Combo: x{torre.combo_atual} (+{combo_bonus_pct}%)", True, (255, 220, 50)
            )
            if torre.niveis_upgrades.get("Combo", 0) > 0:
                combo_bonus_pct = int(torre.combo_atual * torre.bonus_combo_por_acerto * 100)
                txt_combo = fonte_pequena.render(
                    f"Combo: x{torre.combo_atual} (+{combo_bonus_pct}%)", True, (255, 220, 50)
                )

                config.tela.blit(txt_combo, (20, 150))

            rect_botao_upgrades = ui.desenhar_botao_upgrades(fonte_pequena)

            if tempo_atual < tempo_aviso_nivel:
                ui.desenhar_aviso_nivel(dificuldade_atual, fonte_titulo)

            if torre.vida <= 0:
                pygame.time.set_timer(evento_spawn, 0)
                estado_jogo = "game_over"

        elif estado_jogo == "upgrades":
            config.tela.blit(sprites.tela_fundo, (0, 0))
            for inimigo in lista_inimigos:
                config.tela.blit(inimigo.imagem, inimigo.rect)
                ui.desenhar_barra_vida_inimigo(inimigo)             
            config.tela.blit(torre.imagem_sombra, torre.rect_sombra)
            config.tela.blit(torre.imagem, torre.rect)
            if torre.niveis_upgrades.get("dano", 0) == 8:
                config.tela.blit(torre.X_besta, torre.rect_X_besta)                         
            botoes_upgrades, rect_botao_voltar_upgrades = ui.desenhar_tela_upgrades(fonte_titulo, fonte_media, fonte_pequena, torre)

        elif estado_jogo == "game_over":
            config.tela.blit(sprites.tela_fundo, (0, 0))
            for inimigo in lista_inimigos:
                config.tela.blit(inimigo.imagem, inimigo.rect)
            config.tela.blit(torre.imagem, torre.rect)
            rect_botao_replay, rect_botao_novo_jogo_go = ui.desenhar_tela_game_over(fonte_titulo, fonte_media, fonte_pequena, torre.dinheiro)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()