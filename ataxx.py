import random
from turtle import Screen
import numpy
import math
import pygame
import copy

pygame.init()
SIZE = 600
NTABS = 6
N = 7
sq = SIZE / N
MAX_FPS = 15
tabul = [
            [1, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 8, 0, 0, 0],
            [0, 0, 8, 0, 8, 0, 0],
            [0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 1],
        ]
tabcopia = []

class movimento:
    movimentoxi = 0
    movimentoyi = 0
    movimentoyf = 0
    movimentojog = 0
    movimentoxf = 0
    movimentotipo = 0


def copia():
    for i in range(N):
        for j in range(N):
            tabcopia[j][i] = tabul[j][i]


def restaura():
    for i in range(0, N):
        for j in range(0, N):
            tabul[j][i] = tabcopia[j][i]


def outroJog(jog):
    if jog == 1:
        return 2
    else:
        return 1


def assinala_quad(x, y, atip,screen):
    print("foda-se")
    col = (192,192,192)
    if atip == 1:
        col = (173,255,47)
        pygame.draw.ellipse(screen,(220, 20, 60),(y*sq+3,x*sq+3,6,6))
        pygame.draw.ellipse(screen,(220, 20, 60),(y*sq+sq-9,x*sq+3,6,6))
        pygame.draw.ellipse(screen,(220, 20, 60),(y*sq+3,x*sq+sq-9,6,6))
        pygame.draw.ellipse(screen,(220, 20, 60),(y*sq+sq-9,x*sq+sq-9,6,6))

    elif atip == 2:
        col = (199,21,133)
        pygame.draw.ellipse(screen,(220, 20, 60),(x+4,y+5,10, 10))
        pygame.draw.ellipse(screen,(220, 20, 60),(x*sq+5,y*sq+5,4,4))
        pygame.draw.ellipse(screen,(220, 20, 60),(x*sq+5,y*sq+5,4,4))
        pygame.draw.ellipse(screen,(220, 20, 60),(x*sq+5,y*sq+5,4,4))

    

        # Aqui é suposto desenhar os quadrados de movimento


def mostra_tabul(screen, tabul):
    for r in range(N):
        for c in range(N):
            color = pygame.Color(255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(
                c * sq, r * sq, sq - 2, sq - 2))
            if tabul[r][c] == 8:
                pygame.draw.rect(screen, (128, 128, 128),
                                 (c * sq, r * sq, sq - 2, sq - 2))
            if tabul[r][c] == 1:
                pygame.draw.ellipse(screen, (220, 20, 60), pygame.Rect(
                    c * sq + (sq / 4), r * sq + (sq / 4), sq / 2, sq / 2))
            elif tabul[r][c] == 2:
                pygame.draw.ellipse(screen, (106, 90, 205), pygame.Rect(
                    c * sq + (sq / 4), r * sq + (sq / 4), sq / 2, sq / 2))


def tipo_jogo():
    print("Jogo de Ataxx")
    print("Escolha o modo de jogo:")
    print("1 - Humano vs. Humano ")
    print("2 - Humano vs. Computador ")
    print("3 - Computador vs. Computador ")
    tipo = input()
    return tipo


def jogada_Humano(jog, xi, yi,screen):
    cl = 0
    if cl == 0 and tabul[yi][xi]==jog:
        cl = 1
        movimento.movimentoxi = xi
        movimento.movimentoyi = yi
        assinala_quad(yi, xi,1,screen)



def main():
    nMovs = 2
    jog = 0
    tipo = int(tipo_jogo())
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    mostra_tabul(screen, tabul)
    clock.tick(MAX_FPS)
    pygame.display.flip()
    running = True
    while running:
        nMovs += 1
        jog = outroJog(jog)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()

                yi = int(click[1] // sq)
                xi = int(click[0] // sq)
                if nMovs % 2 == 1:
                    if tipo <= 2:
                        jogada_Humano(jog, xi, yi,screen)
                    # else:
                    #     jogada_PC(jog, nMovs)
                else:
                    if tipo == 1 or tipo == 3:
                        jogada_Humano(jog, xi, yi,screen)
                    # else:
                    #     jogada_PC(jog, nMovs)          
        pygame.display.flip()


main()
