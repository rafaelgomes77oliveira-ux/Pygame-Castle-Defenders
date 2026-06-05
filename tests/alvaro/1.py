import pygame
import sys

pygame.init()
#resolução da tela
largura = 1920
altura = 1020
tela = pygame.display.set_mode((largura, altura))

rodando = True


pygame.display.set_caption("Castle Defenders")

#fechar o jogo
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False


pygame.quit()
sys.exit()