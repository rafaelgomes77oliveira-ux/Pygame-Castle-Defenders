import pygame
import sys
import math
import config
from entidades import Torre, InimigoCultista

def carregar_pontos():
    with open("data/pontos.txt", "r") as arq:
        return int(arq.read().strip())

def salvar_pontos(quantidade):
    with open("data/pontos.txt", "w") as arq:
        arq.write(str(quantidade))

pontos = carregar_pontos()

tela_fundo = pygame.image.load("assets/imagens/background.png").convert()
tela_fundo = pygame.transform.scale(tela_fundo, (config.largura, config.altura))
botao_play = pygame.image.load("assets/imagens/botao.png").convert_alpha()
botao_play = pygame.transform.scale(botao_play, (100, 50))
fonte_titulo = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 60)
texto_titulo = fonte_titulo.render("Castle Defenders", True, (255, 255, 255))
rect_titulo = texto_titulo.get_rect(center=(config.centro_x, config.centro_y - 120))

dicionario_inimigos = {}
raio_ataque_mouse = 20

torre = Torre(config.centro_x, config.centro_y)


def spawn_inimigo():
    novo_inimigo = InimigoCultista(config.centro_x, config.centro_y)
    dicionario_inimigos[novo_inimigo] = novo_inimigo.vida


def verificar_colisao_inimigo(inimigo, torre):
    if inimigo.rect.colliderect(torre.rect):
        inimigo.dx = 0
        inimigo.dy = 0
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - inimigo.ultimo_ataque >= 1000:
            torre.vida -= inimigo.dano
            inimigo.ultimo_ataque = tempo_atual


def verificar_dano_mouse(pos_mouse, raio_circulo, dano_causado):
    for inimigo in list(dicionario_inimigos.keys()):
        distancia = math.hypot(pos_mouse[0] - inimigo.rect.centerx, pos_mouse[1] - inimigo.rect.centery)

        if distancia < (raio_circulo + inimigo.rect.width // 2):
            dicionario_inimigos[inimigo] -= dano_causado


evento_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(evento_spawn, 800)

rodando = True
play = True
relogio = pygame.time.Clock()
pygame.display.set_caption("Castle Defenders")

while rodando:
    posicao_mouse = pygame.mouse.get_pos()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if play:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if botao_play.get_rect(topleft=(config.largura // 2 - 50, config.altura // 2 - 25)).collidepoint(
                            posicao_mouse):
                        play = False

        else:
            if evento.type == evento_spawn:
                spawn_inimigo()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    verificar_dano_mouse(posicao_mouse, raio_ataque_mouse, dano_causado=10)

    if play:
        config.tela.fill((0, 0, 0))
        config.tela.blit(texto_titulo, rect_titulo)
        config.tela.blit(botao_play, (config.largura // 2 - 50, config.altura // 2 - 25))
    else:
        config.tela.blit(tela_fundo, (0, 0))

        for inimigo in list(dicionario_inimigos.keys()):
            if dicionario_inimigos[inimigo] <= 0:
                pontos += 1
                salvar_pontos(pontos)
                del dicionario_inimigos[inimigo]
                continue

            inimigo.update()
            config.tela.blit(inimigo.imagem, inimigo.rect)
            verificar_colisao_inimigo(inimigo, torre)

        barra_x = config.centro_x - (torre.barra_vida_largura // 2)
        barra_y = torre.rect.top - 20
        largura_atual_barra = (torre.vida / torre.vida_maxima) * torre.barra_vida_largura
        pygame.draw.rect(config.tela, (40, 40, 40), (barra_x, barra_y, torre.barra_vida_largura, 12))
        pygame.draw.rect(config.tela, (255, 0, 0), (barra_x, barra_y, largura_atual_barra, 12))

        config.tela.blit(torre.imagem, torre.rect)
        pygame.draw.circle(config.tela, (255, 0, 0), posicao_mouse, raio_ataque_mouse)
        texto_pontos = pygame.font.Font("assets/fontes/PixelOperator8-Bold.ttf", 36).render(f"{pontos}", True, (255, 255, 255))
        config.tela.blit(texto_pontos, (20, 20))

        if torre.vida <= 0:
            print("A torre foi destruída! Fim de jogo.")
            rodando = False

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()