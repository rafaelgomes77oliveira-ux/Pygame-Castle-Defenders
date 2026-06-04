import pygame
import sys

pygame.init()

#resolução da tela
largura = 1000
altura = 800
tela = pygame.display.set_mode((largura, altura))

pygame.display.set_caption("Castle Defenders")

#abrir o jogo
rodando = True
#fechar o jogo
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False





pygame.quit()
sys.exit()