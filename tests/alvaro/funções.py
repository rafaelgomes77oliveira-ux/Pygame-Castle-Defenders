import pygame 
import sys

tela = pygame.display.set_mode((1920, 1020))

#função para mostrar um círculo seguindo o cursor do mouse, para a torre dar dano
def função_cursor(tela):
    tela.fill((0, 0, 0))
    posição_mouse = pygame.mouse.get_pos()
    pygame.draw.circle(tela, (255, 0, 0), posição_mouse, 20)
    pygame.display.flip()
    print(posição_mouse)

pygame.quit()
sys.exit()