#funções para o jogo, sem a definição de variaveis por enquanto!


import pygame 
import sys
import random
import math

tela = pygame.display.set_mode((1920, 1020))

#função para mostrar um círculo seguindo o cursor do mouse, para a torre dar dano
#tela.fill deve ser a primeira coisa a ser chamada dentro do loop para evitar que o círculo deixe um rastro na tela e nao apague nada
tela.fill((0, 0, 0))
def função_cursor(tela):
    posição_mouse = pygame.mouse.get_pos()
    pygame.draw.circle(tela, (255, 0, 0), posição_mouse, 20)
    pygame.display.flip()
    print(posição_mouse)

def spawn_inimigo():
    angulo = random.uniform(0, 2 * math.pi)
    
    raio_spawn = max(largura, altura) // 2 + 50
    
    x = centro_x + raio_spawn * math.cos(angulo)
    y = centro_y + raio_spawn * math.sin(angulo)
    
    sentido_x = centro_x - x
    sentido_y = centro_y - y
    
    distancia = math.hypot(sentido_x, sentido_y)
    
    dx = (sentido_x / distancia) * velocidade_inimigo
    dy = (sentido_y / distancia) * velocidade_inimigo
    
    lista_inimigos.append({'x': x, 'y': y, 'dx': dx, 'dy': dy})

pygame.quit()
sys.exit()