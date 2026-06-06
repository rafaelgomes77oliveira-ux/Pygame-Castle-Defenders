import pygame
import sys
import random
import math

pygame.init()
largura = 1920
altura = 1020
tela = pygame.display.set_mode((largura, altura))
centro_x = largura // 2
centro_y = altura // 2

velocidade_inimigo = 3
vida_torre = 100
inimigos = {
    "1" : ["Goblin", 10],
    "2" : ["Slime", 7]
}

class Torre:
    def __init__(self, x_centro, y_centro):
        self.imagem = pygame.image.load("tower.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (100, 100))
        self.rect = self.imagem.get_rect()
        self.rect.center = (x_centro, y_centro)

    def ataque(vida_torre, valor_dano):
        vida = vida_torre
        if vida <= valor_dano:
            fonte = pygame.font.Font(None, 80)
            texto = fonte.render("GAME OVER", True, (255, 0, 0))
            tela.blit(texto, (250, 250))
        else:
            vida -= valor_dano

class Inimigo:
    def __init__(self, x_centro, y_centro, velocidade, vida):
        self.imagem = pygame.image.load("enemy.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (30, 60))
        self.rect = self.imagem.get_rect()

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
        return self.rect.center

posicao_inimigo = Inimigo.update

torre = Torre(centro_x, centro_y)

class Trovao:
    def __init__(self, posicao_mouse, valor_dano):
        self.posicao_mouse = posicao_mouse
        self.valor_dano = valor_dano
    
    def update_vida_inimigo(valor_dano):
        for chave, valores in inimigos.items():
            vida_inimigos = (valores[1])  
        if vida_inimigos > valor_dano:
            valores[1] -= valor_dano
        elif vida_inimigos == 0:
            inimigos.popitem(chave)
                   

def spawn_inimigo():
    novo_inimigo = Inimigo(centro_x, centro_y, velocidade_inimigo)
    #lista_inimigos.append(novo_inimigo)

def verificar_colisao_inimigo(inimigo, torre):
    if inimigo.rect.colliderect(torre.rect):
        inimigo.dx = 0
        inimigo.dy = 0


def atacar_inimigos(posicao_mouse, posicao_inimigo, evento):
    if posicao_mouse == posicao_inimigo and evento.type == pygame.MOUSEBUTTONDOWN:
        Trovao.update_vida_inimigo(valor_dano=10)        

EVENTO_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_SPAWN, 800)

rodando = True
relogio = pygame.time.Clock()
pygame.display.set_caption("Castle Defenders")


#atualizar o while conforme alterações feitas
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == EVENTO_SPAWN:
            spawn_inimigo()

    tela.fill((0, 0, 0))

    for chave, inimigo in inimigos:
        inimigo.update()
        tela.blit(inimigo.imagem, inimigo.rect)
        verificar_colisao_inimigo(inimigo, torre)

    posicao_mouse = pygame.mouse.get_pos()
    pygame.draw.circle(tela, (255, 0, 0), posicao_mouse, 20)
    tela.blit(torre.imagem, torre.rect)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()