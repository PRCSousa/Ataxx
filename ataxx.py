
# Ataxx
# Project developed by Pedro Sousa and Inês Cardoso

from numpy import unsignedinteger
import pygame
import time
import copy
import random

pygame.init()
MAX_FPS = 15
SIZE = 600


class gamestate:
    N = unsignedinteger
    sq = unsignedinteger
    tabuleiro = []
    tipo = unsignedinteger
    ai1diff = unsignedinteger
    ai2diff = unsignedinteger
    rec = 0
    nMovs = 1
    vencedor = 0


class movimento:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    jog = 0
    tipo = 0


class totalmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    tipo = 0


class bestmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0


class minmaxmov():
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    min = 0
    max = 0


class save:
    game = []


def escolhe_tabul():
    print("Tabuleiros:")
    print("1) Original")
    print("2) Sem paredes")
    print("3) Circular")
    print("4) Coração")
    print("5) Alvo")
    print("6) Xadrez")
    print("7) Foxy")
    print("8) 5x5")
    print("9) 6x6")
    numtabul = input()
    tabuleiro = "tabuleiros/tab"+numtabul+".txt"
    return tabuleiro


def carrega_tabul(ficheiro):
    f = open(ficheiro)
    gamestate.N = int(f.readline())
    gamestate.sq = SIZE / gamestate.N
    tabuleiro = []
    for i in range(gamestate.N):
        tabuleiro.append(list(map(int, f.readline().split())))
    f.close()
    gamestate.tabuleiro = tabuleiro


def dificuldade():
    if gamestate.tipo == 1:
        return
    elif gamestate.tipo == 2:
        print("Dificuldade:")
        print("1) Fácil")
        print("2) Médio")
        print("3) Difícil")
        gamestate.ai2diff = input()
        return
    else:
        print("Algoritmo da AI 1:")
        print("1) Random")
        print("2) Greedy")
        print("3) Center Control")
        print("4) Minmax")
        gamestate.ai1diff = int(input())
        print("Algoritmo da AI 2:")
        print("1) Random")
        print("2) Greedy")
        print("3) Center Control")
        print("4) Minmax")
        gamestate.ai2diff = int(input())
        return


def copia():
    save.game = copy.deepcopy(gamestate.tabuleiro)


def restaura():
    gamestate.tabuleiro = save.game


def troca_jog(jog):
    if jog == 1:
        return 2
    else:
        return 1


def assinala_quad(x, y, screen):
    if movimento.jog == 1:
        color = pygame.Color(220, 20, 60)
    else:
        color = pygame.Color(106, 90, 205)
    pygame.draw.ellipse(
        screen, color, (y*gamestate.sq+3, x*gamestate.sq+3, 6, 6))
    pygame.draw.ellipse(screen, color, (y*gamestate.sq +
                        gamestate.sq-11, x*gamestate.sq+3, 6, 6))
    pygame.draw.ellipse(screen, color, (y*gamestate.sq+3,
                        x*gamestate.sq+gamestate.sq-11, 6, 6))
    pygame.draw.ellipse(screen, color, (y*gamestate.sq +
                        gamestate.sq-11, x*gamestate.sq+gamestate.sq-11, 6, 6))


def mostra_tabul(screen):
    for r in range(gamestate.N):
        for c in range(gamestate.N):
            color = pygame.Color(255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(
                c * gamestate.sq, r * gamestate.sq, gamestate.sq - 2, gamestate.sq - 2))
            if gamestate.tabuleiro[r][c] == 8:
                pygame.draw.rect(screen, (128, 128, 128),
                                 (c * gamestate.sq, r * gamestate.sq, gamestate.sq - 2, gamestate.sq - 2))
            if gamestate.tabuleiro[r][c] == 1:
                pygame.draw.ellipse(screen, (220, 20, 60), pygame.Rect(

                    c * gamestate.sq + (gamestate.sq / 4), r * gamestate.sq + (gamestate.sq / 4), gamestate.sq / 2, gamestate.sq / 2))
            elif gamestate.tabuleiro[r][c] == 2:
                pygame.draw.ellipse(screen, (106, 90, 205), pygame.Rect(
                    c * gamestate.sq + (gamestate.sq / 4), r * gamestate.sq + (gamestate.sq / 4), gamestate.sq / 2, gamestate.sq / 2))


def comer():
    dx = -1
    dy = -1
    for dx in range(dx, 2):
        for dy in range(dy, 2):
            try:
                if movimento.yf + dy == -1 and movimento.xf + dx == -1:
                    if gamestate.tabuleiro[0][0] == troca_jog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy +
                                            1][movimento.xf + dx+1] = movimento.jog
                elif movimento.yf + dy == -1:
                    if gamestate.tabuleiro[0][movimento.xf + dx] == troca_jog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy +
                                            1][movimento.xf + dx] = movimento.jog
                elif movimento.xf + dx == -1:
                    if gamestate.tabuleiro[movimento.yf + dy][0] == troca_jog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy][movimento.xf +
                                                               dx+1] = movimento.jog

                elif gamestate.tabuleiro[movimento.yf + dy][movimento.xf + dx] == troca_jog(movimento.jog):
                    gamestate.tabuleiro[movimento.yf +
                                        dy][movimento.xf + dx] = movimento.jog
            except IndexError:
                pass
        dy = -1


def executa_movimento():
    gamestate.tabuleiro[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        gamestate.tabuleiro[movimento.yi][movimento.xi] = 0
    comer()


def adjacente(dist, classe):
    return(
        abs(classe.xi - classe.xf) == dist and abs(classe.yi - classe.yf) <= dist or
        abs(classe.yi - classe.yf) == dist and abs(classe.xi - classe.xf) <= dist)


def dentro(x, y):
    return (x >= 0 and x <= gamestate.N-1 and y >= 0 and y <= gamestate.N-1)


def movimento_valido(classe):
    if abs(classe.yf - classe.yi) == 2 and abs(classe.xf - classe.xi) == 1 or abs(classe.xf - classe.xi) == 2 and abs(classe.yf - classe.yi) == 1:
        return False
    if not dentro(classe.xi, classe.yi) or not dentro(classe.xf, classe.yf):
        return False
    if gamestate.tabuleiro[classe.yi][classe.xi] == movimento.jog and gamestate.tabuleiro[classe.yf][classe.xf] == 0 and adjacente(1, classe):
        classe.tipo = 0
        return True
    if gamestate.tabuleiro[classe.yi][classe.xi] == movimento.jog and gamestate.tabuleiro[classe.yf][classe.xf] == 0 and adjacente(2, classe):
        classe.tipo = 1
        return True


def tipo_jogo():
    print("Jogo de Ataxx")
    print("Escolha o modo de jogo:")
    print("1 - Humano vs. Humano ")
    print("2 - Humano vs. Computador ")
    print("3 - Computador vs. Computador ")
    tipo = input()
    return tipo


def jogadas_validas_pos(jog, yi, xi, screen):
    if gamestate.tabuleiro[yi][xi] == jog:
        for k in range(gamestate.N):
            for l in range(gamestate.N):
                movimento.jog = jog
                movimento.yi = yi
                movimento.xi = xi
                movimento.yf = k
                movimento.xf = l
                if movimento_valido(movimento):
                    assinala_quad(k, l, screen)


def jogadas_validas_total(jog):
    nmovs = 0
    for yi in range(gamestate.N):
        for xi in range(gamestate.N):
            if gamestate.tabuleiro[yi][xi] == jog:
                for yf in range(gamestate.N):
                    for xf in range(gamestate.N):
                        movimento.jog = jog
                        totalmov.yi = yi
                        totalmov.xi = xi
                        totalmov.yf = yf
                        totalmov.xf = xf
                        if movimento_valido(totalmov):
                            nmovs += 1
    return nmovs


def conta_pecas(jog):
    pecas = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == jog:
                pecas += 1
    return pecas


def quad_vazios():
    nmovs = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == 0:
                nmovs += 1
    return nmovs


def fim_jogo():
    n = quad_vazios()
    if conta_pecas(1) == 0 or conta_pecas(2) == 0:
        if conta_pecas(1) == 0:
            gamestate.vencedor = 1
            return -1
        else:
            gamestate.vencedor = -1
            return -1
    if n == 0:
        if (conta_pecas(1) - conta_pecas(2) >= 0):
            gamestate.vencedor = -1
            return -1
        if (conta_pecas(1) - conta_pecas(2) < 0):
            gamestate.vencedor = 1
            return -1
        else:
            gamestate.vencedor = 0
            return -1
    else:
        return 0


def finaliza():
    if gamestate.vencedor != 0:
        if gamestate.vencedor == -1:
            print("Jogador vermelho ganha !")
        else:
            print("Jogador azul ganha !")
    else:
        print("Empate!")


def jogada_Humano(cl, px, py, screen):
    if cl == 0:
        movimento.xi = px
        movimento.yi = py
        assinala_quad(py, px, screen)
        jogadas_validas_pos(movimento.jog, py, px, screen)
    elif cl == 1:
        movimento.xf = px
        movimento.yf = py


def jogada_PC():
    bestav = -1000
    for yi in range(gamestate.N):
        for xi in range(gamestate.N):
            if gamestate.tabuleiro[yi][xi] == movimento.jog:
                for k in range(0, gamestate.N):
                    for l in range(0, gamestate.N):
                        movimento.yi = yi
                        movimento.xi = xi
                        movimento.yf = l
                        movimento.xf = k
                        if movimento_valido(movimento):
                            copia()
                            executa_movimento()
                            if gamestate.nMovs % 2 != 1:
                                av = avalia(gamestate.ai2diff)
                            else:
                                av = avalia(gamestate.ai1diff)
                            restaura()
                            if av >= bestav:
                                bestav = av
                                bestmov.yi = movimento.yi
                                bestmov.xi = movimento.xi
                                bestmov.yf = movimento.yf
                                bestmov.xf = movimento.xf
    movimento.yi = bestmov.yi
    movimento.xi = bestmov.xi
    movimento.yf = bestmov.yf
    movimento.xf = bestmov.xf
    if movimento_valido(movimento):
        executa_movimento()


def avalia(tipo):
    tipo = int(tipo)
    score = 0
    if tipo == 1:
        score = algo_random()
    elif tipo == 2:
        score = algo_greedy()
    elif tipo == 3:
        score = algo_centercontrol()
    elif tipo == 4:
        if gamestate.nMovs % 2 != 1:
            movimento.jog = 1
            minmaxmov.min = 1
            minmaxmov.max = 2
        else:
            movimento.jog = 2
            minmaxmov.min = 2
            minmaxmov.max = 1
        minmaxmov.yi = movimento.yi
        minmaxmov.xi = movimento.xi
        minmaxmov.yf = movimento.yf
        minmaxmov.xf = movimento.xf
        alfa = -100000
        beta = 100000
        score = algo_minmax(0, True, alfa, beta)
        movimento.yi = minmaxmov.yi
        movimento.xi = minmaxmov.xi
        movimento.yf = minmaxmov.yf
        movimento.xf = minmaxmov.xf
    elif tipo > 4:
        score = random.random()
    return score


def algo_random():
    return (random.randint(1, 10))


def algo_greedy():
    salt = random.random()
    return (conta_pecas(movimento.jog) - conta_pecas(troca_jog(movimento.jog))+salt)


def algo_centercontrol():
    salt = random.random()
    yc = abs(gamestate.N / 2 - movimento.yf)
    xc = abs(gamestate.N / 2 - movimento. xf)
    score = 100 - (yc + xc) + 2*conta_pecas(movimento.jog) + salt
    return score


def algo_minmax(depth, minimizer, alfa, beta):
    if depth == 3 or fim_jogo == -1:
        return (algo_greedy() * (-1))

    if minimizer:
        movimento.jog = minmaxmov.min
        value = +1000
        for yi in range(gamestate.N):
            for xi in range(gamestate.N):
                if gamestate.tabuleiro[yi][xi] == movimento.jog:
                    for k in range(0, gamestate.N):
                        for l in range(0, gamestate.N):
                            movimento.yi = yi
                            movimento.xi = xi
                            movimento.yf = l
                            movimento.xf = k
                            if movimento_valido(movimento):
                                temp = copy.deepcopy(gamestate.tabuleiro)
                                executa_movimento()
                                evaluation = algo_minmax(
                                    depth + 1, False, alfa, beta)
                                gamestate.tabuleiro = temp
                                value = min(value, evaluation)
                                beta = min(beta, evaluation)
                                if beta <= alfa:
                                    break
        movimento.jog = minmaxmov.max
        return value
    else:
        movimento.jog = minmaxmov.max
        value = -1000
        for yi in range(gamestate.N):
            for xi in range(gamestate.N):
                if gamestate.tabuleiro[yi][xi] == movimento.jog:
                    for k in range(0, gamestate.N):
                        for l in range(0, gamestate.N):
                            movimento.yi = yi
                            movimento.xi = xi
                            movimento.yf = l
                            movimento.xf = k
                            if movimento_valido(movimento):
                                temp = copy.deepcopy(gamestate.tabuleiro)
                                executa_movimento()
                                evaluation = algo_minmax(
                                    depth + 1, True, alfa, beta)
                                gamestate.tabuleiro = temp
                                value = max(value, evaluation)
                                alfa = max(alfa, evaluation)
                                if beta <= alfa:
                                    break
        movimento.jog = minmaxmov.min
        return value


def main():
    cl = 0
    fim = 0
    movimento.jog = 1
    gamestate.tipo = int(tipo_jogo())
    dificuldade()
    tabuleiro = escolhe_tabul()
    carrega_tabul(tabuleiro)
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    mostra_tabul(screen)
    clock.tick(30)
    pygame.display.flip()
    running = True

    while running:

        if jogadas_validas_total(movimento.jog) == 0:
            gamestate.nMovs += 1
            movimento.jog = troca_jog(movimento.jog)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                time.sleep(2)
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:

                click = pygame.mouse.get_pos()
                yi = int(click[1] // gamestate.sq)
                xi = int(click[0] // gamestate.sq)

                if gamestate.nMovs % 2 == 1:

                    if gamestate.tipo <= 2:
                        if cl == 0 and gamestate.tabuleiro[yi][xi] == movimento.jog:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            if movimento_valido(movimento):
                                executa_movimento()

                                gamestate.nMovs += 1
                                movimento.jog = 2

                            mostra_tabul(screen)
                else:

                    if gamestate.tipo == 1:
                        if cl == 0 and gamestate.tabuleiro[yi][xi] == movimento.jog:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            if movimento_valido(movimento):
                                executa_movimento()
                                gamestate.nMovs += 1
                                movimento.jog = 1
                            mostra_tabul(screen)
            try:
                pygame.display.flip()
            except pygame.error:
                pass

        if gamestate.nMovs % 2 != 1 and gamestate.tipo >= 2:
            jogada_PC()
            gamestate.nMovs += 1
            mostra_tabul(screen)
            movimento.jog = 1
            time.sleep(1)
            pygame.display.flip()
        if gamestate.tipo == 3:
            jogada_PC()
            gamestate.nMovs += 1
            mostra_tabul(screen)
            movimento.jog = 2
            time.sleep(1)
            pygame.display.flip()

        try:
            pygame.display.flip()
        except pygame.error:
            pass

        fim = fim_jogo()
        if fim == -1:
            print("\n")
            print("Jogador Vermelho:", conta_pecas(1))
            print("Jogador Azul:", conta_pecas(2))
            finaliza()
            print("\n")
            print("Trabalho realizado por:")
            print("Pedro Sousa")
            print("Inês Cardoso")
            time.sleep(1)
            pygame.quit()
            running = False


main()
