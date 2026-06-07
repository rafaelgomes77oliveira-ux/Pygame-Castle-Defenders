import pygame
import sys
import random
import math

pygame.init()
largura = 1920
altura = 1020
tela = pygame.display.set_mode((largura, altura))
tela_fundo = pygame.image.load(r"C:\Users\silva\Pygame-Castle-Defenders\tests\joao\background.png").convert()
tela_fundo = pygame.transform.scale(tela_fundo, (largura, altura))
centro_x = largura // 2
centro_y = altura // 2

botao_play_teste = pygame.image.load("tests/joao/botao.png").convert_alpha()
botao_play_teste = pygame.transform.scale(botao_play_teste, (100, 50))

imagem_torre = pygame.image.load("tests/joao/tower.png").convert_alpha()
imagem_torre = pygame.transform.scale(imagem_torre, (150, 150))

imagem_inimigo = pygame.image.load("tests/joao/enemy.png").convert_alpha()
imagem_inimigo = pygame.transform.scale(imagem_inimigo, (30, 60))

dicionario_inimigos = {}
velocidade_inimigo = 3
raio_ataque_mouse = 20 

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
    def __init__(self, x_centro, y_centro, velocidade):
        self.imagem = imagem_inimigo 
        self.rect = self.imagem.get_rect()
        self.vida = 10
        self.dano = 5
        self.ultimo_ataque = 0

        angulo = random.uniform(0, 2 * math.pi)
        raio_spawn = max(largura, altura) // 2 + 50

        self.x = x_centro + raio_spawn * math.cos(angulo)
        self.y = y_centro + raio_spawn * math.sin(angulo)

        sentido_x = x_centro - self.x
        sentido_y = y_centro - self.y
        distancia = math.hypot(sentido_x, sentido_y)

        self.dx = (sentido_x / distancia) * velocidade
        self.dy = (sentido_y / distancia) * velocidade

        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))

torre = Torre(centro_x, centro_y)

def spawn_inimigo():
    novo_inimigo = Inimigo(centro_x, centro_y, velocidade_inimigo)
    dicionario_inimigos[novo_inimigo] = novo_inimigo.vida

def verificar_colisao_inimigo(inimigo, torre):
    if inimigo.rect.colliderect(torre.rect):
        inimigo.dx = 0
        inimigo.dy = 0
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - inimigo.ultimo_ataque >= 1000:
            torre.vida -= inimigo.dano
            print(f"Vida da Torre: {torre.vida}")
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
                    if botao_play_teste.get_rect(topleft=(largura // 2 - 50, altura // 2 - 25)).collidepoint(posicao_mouse):
                        play = False
        
        else:
            if evento.type == evento_spawn:
                spawn_inimigo()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    verificar_dano_mouse(posicao_mouse, raio_ataque_mouse, dano_causado=5)

    if play:
        tela.fill((0, 0, 0)) 
        tela.blit(botao_play_teste, (largura // 2 - 50, altura // 2 - 25))
    else:
        tela.blit(tela_fundo, (0, 0))

        for inimigo in list(dicionario_inimigos.keys()):
            if dicionario_inimigos[inimigo] <= 0:
                del dicionario_inimigos[inimigo]
                continue

            inimigo.update()
            tela.blit(inimigo.imagem, inimigo.rect)
            verificar_colisao_inimigo(inimigo, torre)

        pygame.draw.rect(tela, (255, 0, 0), (centro_x - 50, centro_y - 75, torre.vida/torre.ratio_vida, 10))
        tela.blit(torre.imagem, torre.rect)
        pygame.draw.circle(tela, (255, 0, 0), posicao_mouse, raio_ataque_mouse)

        if torre.vida <= 0:
            print("A torre foi destruída! Fim de jogo.")
            rodando = False

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()