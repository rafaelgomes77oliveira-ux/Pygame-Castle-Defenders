import pygame

class Inimigo:
    def __init__(self, nome, vida, dano, x, y):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.x = x
        self.y = y

    def mostrar_status(self):
        print(f"{self.nome} | Vida: {self.vida} | Dano: {self.dano}")

    def receber_dano(self, dano):
        self.vida -= dano

        if self.vida <= 0:
            print(f"{self.nome} foi derrotado!")

   