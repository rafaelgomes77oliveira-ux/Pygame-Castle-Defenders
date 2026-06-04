import pygame

pygame.init()

janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Meu primeiro jogo")

rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()