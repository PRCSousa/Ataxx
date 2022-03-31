import pygame
import time
import copy
import random

SIZE = 600


class tabul:
    N = 1
    sq = SIZE / N
    tabuleiro = []


pygame.init()
MAX_FPS = 15


class movimento:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    jog = 0
    tipo = 0
    vencedor = 0


class bestmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0


class save:
    game = []


def letabul(ficheiro):
    f = open(ficheiro)
    tabul.N = int(f.readline())
    tabul.sq = SIZE / tabul.N
    tabuleiro = []
    for i in range(tabul.N):
        tabuleiro.append(list(map(int, f.readline().split())))
    f.close()
    tabul.tabuleiro = tabuleiro


def escolhetabul():
    print("Tabuleiros:")
    print("1) 7x7 Original")
    print("2) 10x10 Sem paredes")
    print("3) 9x9 Circular")
    print("4) 13x13 Coração")
    print("5) 10x10 Alvo")
    numtabul = input()
    tabuleiro = "tabuleiros/tab"+numtabul+".txt"
    return tabuleiro


def copia():
    save.game = copy.deepcopy(tabul.tabuleiro)


def restaura():
    tabul.tabuleiro = save.game


def outroJog(jog):
    if jog == 1:
        return 2
    else:
        return 1


def assinala_quad(x, y, screen):
    if movimento.jog == 1:
        pygame.draw.ellipse(screen, (220, 20, 60),
                            (y*tabul.sq+3, x*tabul.sq+3, 6, 6))
        pygame.draw.ellipse(screen, (220, 20, 60),
                            (y*tabul.sq+tabul.sq-11, x*tabul.sq+3, 6, 6))
        pygame.draw.ellipse(screen, (220, 20, 60),
                            (y*tabul.sq+3, x*tabul.sq+tabul.sq-11, 6, 6))
        pygame.draw.ellipse(screen, (220, 20, 60),
                            (y*tabul.sq+tabul.sq-11, x*tabul.sq+tabul.sq-11, 6, 6))

    else:
        pygame.draw.ellipse(screen, (106, 90, 205),
                            (y*tabul.sq+3, x*tabul.sq+3, 6, 6))
        pygame.draw.ellipse(screen, (106, 90, 205),
                            (y*tabul.sq+tabul.sq-11, x*tabul.sq+3, 6, 6))
        pygame.draw.ellipse(screen, (106, 90, 205),
                            (y*tabul.sq+3, x*tabul.sq+tabul.sq-11, 6, 6))
        pygame.draw.ellipse(screen, (106, 90, 205),
                            (y*tabul.sq+tabul.sq-11, x*tabul.sq+tabul.sq-11, 6, 6))


def mostra_tabul(screen):
    for r in range(tabul.N):
        for c in range(tabul.N):
            color = pygame.Color(255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(
                c * tabul.sq, r * tabul.sq, tabul.sq - 2, tabul.sq - 2))
            if tabul.tabuleiro[r][c] == 8:
                pygame.draw.rect(screen, (128, 128, 128),
                                 (c * tabul.sq, r * tabul.sq, tabul.sq - 2, tabul.sq - 2))
            if tabul.tabuleiro[r][c] == 1:
                pygame.draw.ellipse(screen, (220, 20, 60), pygame.Rect(
                    c * tabul.sq + (tabul.sq / 4), r * tabul.sq + (tabul.sq / 4), tabul.sq / 2, tabul.sq / 2))
            elif tabul.tabuleiro[r][c] == 2:
                pygame.draw.ellipse(screen, (106, 90, 205), pygame.Rect(
                    c * tabul.sq + (tabul.sq / 4), r * tabul.sq + (tabul.sq / 4), tabul.sq / 2, tabul.sq / 2))


def comer():
    dx = -1
    dy = -1
    for dx in range(dx, 2):
        for dy in range(dy, 2):
            try:
                if movimento.yf + dy == -1 and movimento.xf + dx == -1:
                    if tabul.tabuleiro[0][0] == outroJog(movimento.jog):
                        tabul.tabuleiro[movimento.yf + dy +
                                        1][movimento.xf + dx+1] = movimento.jog
                elif movimento.yf + dy == -1:
                    if tabul.tabuleiro[0][movimento.xf + dx] == outroJog(movimento.jog):
                        tabul.tabuleiro[movimento.yf + dy +
                                        1][movimento.xf + dx] = movimento.jog
                elif movimento.xf + dx == -1:
                    if tabul.tabuleiro[movimento.yf + dy][0] == outroJog(movimento.jog):
                        tabul.tabuleiro[movimento.yf + dy][movimento.xf +
                                                           dx+1] = movimento.jog

                elif tabul.tabuleiro[movimento.yf + dy][movimento.xf + dx] == outroJog(movimento.jog):
                    tabul.tabuleiro[movimento.yf +
                                    dy][movimento.xf + dx] = movimento.jog
            except IndexError:
                pass
        dy = -1


def executa_movimento():
    tabul.tabuleiro[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        tabul.tabuleiro[movimento.yi][movimento.xi] = 0
    comer()


def avalia():
    salt = random.random()
    return (conta_pecas(movimento.jog) - conta_pecas(outroJog(movimento.jog))+salt)


def adjacente(dist):
    return(
        abs(movimento.xi - movimento.xf) == dist and abs(movimento.yi - movimento.yf) <= dist or
        abs(movimento.yi - movimento.yf) == dist and abs(movimento.xi - movimento.xf) <= dist)


def dentro(x, y):
    return (x >= 0 and x <= tabul.N-1 and y >= 0 and y <= tabul.N-1)


def movimento_valido():
    if abs(movimento.yf - movimento.yi) == 2 and abs(movimento.xf - movimento.xi) == 1 or abs(movimento.xf - movimento.xi) == 2 and abs(movimento.yf - movimento.yi) == 1:
       return False
    if not dentro(movimento.xi, movimento.yi) or not dentro(movimento.xf, movimento.yf):
        return False
    if tabul.tabuleiro[movimento.yi][movimento.xi] == movimento.jog and tabul.tabuleiro[movimento.yf][movimento.xf] == 0 and adjacente(1):
        movimento.tipo = 0
        return True
    if tabul.tabuleiro[movimento.yi][movimento.xi] == movimento.jog and tabul.tabuleiro[movimento.yf][movimento.xf] == 0 and adjacente(2):
        movimento.tipo = 1
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
    if tabul.tabuleiro[yi][xi] == jog:
        for k in range(tabul.N):
            for l in range(tabul.N):
                movimento.jog = jog
                movimento.yi = yi
                movimento.xi = xi
                movimento.yf = k
                movimento.xf = l
                if movimento_valido():
                    assinala_quad(k, l, screen)

# def jogadas_validas_total(jog):
#     nmovs = 0
#     for y in range(tabul.N):
#         for x in range(tabul.N):
#             if tabul.tabuleiro[y][x] == jog:
#                 for k in range(tabul.N):
#                     for l in range(tabul.N):
#                         movimento.jog = jog
#                         movimento.yi = y
#                         movimento.xi = x
#                         movimento.yf = k
#                         movimento.xf = l
#                         if movimento_valido():
#                             nmovs += 1
#     return nmovs


def conta_pecas(jog):
    pecas = 0
    for i in range(tabul.N):
        for j in range(tabul.N):
            if tabul.tabuleiro[i][j] == jog:
                pecas += 1
    return pecas


def quad_validos():
    nmovs = 0
    for i in range(tabul.N):
        for j in range(tabul.N):
            if tabul.tabuleiro[i][j] == 0:
                nmovs += 1
    return nmovs


def fim_jogo():
    n = quad_validos()
    if conta_pecas(1) == 0 or conta_pecas(2) == 0:
        if conta_pecas(1) == 0:
            movimento.vencedor = 2
            return -1
        else:
            movimento.vencedor = 1
            return -1
    if n == 0:
        if (conta_pecas(1) - conta_pecas(2) >= 0):
            movimento.vencedor = 1
            return -1
        if (conta_pecas(1) - conta_pecas(2) < 0):
            movimento.vencedor = 2
            return -1
        else:
            movimento.vencedor = 0
            return -1
    else:
        return 0


def finaliza(tipo, fim):
    if movimento.vencedor != 0:
        print("Jogador", movimento.vencedor, "ganha !")
    else:
        print("Empate!")


def jogada_Humano(cl, px, py, screen):
    if cl == 0 and tabul.tabuleiro[py][px] == movimento.jog:
        movimento.xi = px
        movimento.yi = py
        assinala_quad(py, px, screen)
        jogadas_validas_pos(movimento.jog, py, px, screen)
    elif cl == 1:
        movimento.xf = px
        movimento.yf = py
        assinala_quad(movimento.xf, movimento.yf, screen)


def jogada_PC():
    bestav = -1000
    for yi in range(tabul.N):
        for xi in range(tabul.N):
            if tabul.tabuleiro[yi][xi] == movimento.jog:
                for k in range(0, tabul.N):
                    for l in range(0, tabul.N):
                        movimento.yi = yi
                        movimento.xi = xi
                        movimento.yf = l
                        movimento.xf = k
                        if movimento_valido():
                            copia()
                            executa_movimento()
                            av = avalia()
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
    if movimento_valido():
        executa_movimento()


def main():
    cl = 0
    nMovs = 1
    fim = 0
    movimento.jog = 1
    tipo = int(tipo_jogo())
    tabuleiro = escolhetabul()
    letabul(tabuleiro)
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    mostra_tabul(screen)
    clock.tick(30)
    pygame.display.flip()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                time.sleep(2)
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()

                yi = int(click[1] // tabul.sq)
                xi = int(click[0] // tabul.sq)
                if nMovs % 2 == 1:
                    if tipo <= 2:
                        if cl == 0:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            if movimento_valido():
                                executa_movimento()
                                nMovs += 1
                                movimento.jog = outroJog(movimento.jog)
                            mostra_tabul(screen)

                    else:
                        jogada_PC()
                        nMovs += 1
                        mostra_tabul(screen)
                        movimento.jog = outroJog(movimento.jog)

                else:
                    if tipo == 1:
                        if cl == 0:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            if movimento_valido():
                                executa_movimento()
                                nMovs += 1
                                movimento.jog = outroJog(movimento.jog)
                            mostra_tabul(screen)

                    else:
                        jogada_PC()
                        nMovs += 1
                        mostra_tabul(screen)
                        movimento.jog = outroJog(movimento.jog)

        try:
            pygame.display.flip()
        except pygame.error:
            pass
        fim = fim_jogo()
        if fim == -1:
            print("Jogador 1:", conta_pecas(1))
            print("Jogador 2:", conta_pecas(2))
            finaliza(tipo, fim)
            time.sleep(5)
            pygame.quit()
            running = False


main()

'''
Dev Notes:

25/03
A seleção das peças já está a funcionar, se achares estranho o facto de
carregares nas peças azuis e selecionarem em vermelho, dw porque isso resolve-se
quando a função jogada_PC for feita (I hope)

Tenho de ter em atenção em como vou dar handle aos cliques do rato, posso fazer
encadeamento de funções ATÉ ter de dar input a mais um mouse click, a função
que recebe esse mouse click tem de ser feita dentro do if do evento do
MOUSEBUTTONDOWN


28/03
O jogo base já funciona!
As peças comem-se umas as outras e seguem todas as regras de movimento
como esperado.
O verificador da win condition não está a funcionar direito, tenho de fazer
de raíz by myself.
Tomorrow is gonna be a good day.

29/03
O jogo já verifica se alguem ficou sem peças,ou , no caso do tabuleiro ter sido
completamente preenchido, quem tem mais peças.
Ainda falta o caso de se um jogador ficar sem jogadas válidas, dá skip ao seu turno.
De resto, só falta implementar as jogadas do computador, it shouldn't be that hard right?

A jogada do computador está burra, idk what is going on, must be tested.


30/03

Humano x PC e PC x PC funcionam.
Ainda não tenho isto. "Ainda falta o caso de se um jogador ficar sem jogadas válidas, dá skip ao seu turno."


'''
