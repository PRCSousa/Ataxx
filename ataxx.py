import pygame
import time
import copy

pygame.init()
SIZE = 600
NTABS = 6
N = 7
sq = SIZE / N
MAX_FPS = 15


class tabul:
    tabul = [
        [1, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 0],
        [0, 0, 8, 0, 8, 0, 0],
        [0, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
    ]


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


def copia():
    save.game = copy.deepcopy(tabul.tabul)


def restaura():
    tabul.tabul = save.game


def outroJog(jog):
    if jog == 1:
        return 2
    else:
        return 1


def assinala_quad(x, y, screen):
    if movimento.jog == 1:
        pygame.draw.ellipse(screen, (220, 20, 60), (y*sq+3, x*sq+3, 6, 6))
        pygame.draw.ellipse(screen, (220, 20, 60), (y*sq+sq-11, x*sq+3, 6, 6))
        pygame.draw.ellipse(screen, (220, 20, 60), (y*sq+3, x*sq+sq-11, 6, 6))
        pygame.draw.ellipse(screen, (220, 20, 60),
                            (y*sq+sq-11, x*sq+sq-11, 6, 6))

    else:
        pygame.draw.ellipse(screen, (106, 90, 205), (y*sq+3, x*sq+3, 6, 6))
        pygame.draw.ellipse(screen, (106, 90, 205), (y*sq+sq-11, x*sq+3, 6, 6))
        pygame.draw.ellipse(screen, (106, 90, 205), (y*sq+3, x*sq+sq-11, 6, 6))
        pygame.draw.ellipse(screen, (106, 90, 205),
                            (y*sq+sq-11, x*sq+sq-11, 6, 6))


def mostra_tabul(screen):
    for r in range(N):
        for c in range(N):
            color = pygame.Color(255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(
                c * sq, r * sq, sq - 2, sq - 2))
            if tabul.tabul[r][c] == 8:
                pygame.draw.rect(screen, (128, 128, 128),
                                 (c * sq, r * sq, sq - 2, sq - 2))
            if tabul.tabul[r][c] == 1:
                pygame.draw.ellipse(screen, (220, 20, 60), pygame.Rect(
                    c * sq + (sq / 4), r * sq + (sq / 4), sq / 2, sq / 2))
            elif tabul.tabul[r][c] == 2:
                pygame.draw.ellipse(screen, (106, 90, 205), pygame.Rect(
                    c * sq + (sq / 4), r * sq + (sq / 4), sq / 2, sq / 2))


def comer():
    dx = -1
    dy = -1
    for dx in range(dx, 2):
        for dy in range(dy, 2):
            try:
                if movimento.yf + dy == -1 and movimento.xf + dx == -1:
                    if tabul.tabul[0][0] == outroJog(movimento.jog):
                        tabul.tabul[movimento.yf + dy +
                                    1][movimento.xf + dx+1] = movimento.jog
                elif movimento.yf + dy == -1:
                    if tabul.tabul[0][movimento.xf + dx] == outroJog(movimento.jog):
                        tabul.tabul[movimento.yf + dy +
                                    1][movimento.xf + dx] = movimento.jog
                elif movimento.xf + dx == -1:
                    if tabul.tabul[movimento.yf + dy][0] == outroJog(movimento.jog):
                        tabul.tabul[movimento.yf + dy][movimento.xf +
                                                       dx+1] = movimento.jog

                elif tabul.tabul[movimento.yf + dy][movimento.xf + dx] == outroJog(movimento.jog):
                    tabul.tabul[movimento.yf +
                                dy][movimento.xf + dx] = movimento.jog
            except IndexError:
                pass
        dy = -1


def executa_movimento():
    tabul.tabul[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        tabul.tabul[movimento.yi][movimento.xi] = 0
    comer()


def avalia():
    return conta_pecas(movimento.jog) - conta_pecas(outroJog(movimento.jog))


def adjacente(dist):
    return(
        abs(movimento.xi - movimento.xf) == dist and abs(movimento.yi - movimento.yf) <= dist or
        abs(movimento.yi - movimento.yf) == dist and abs(movimento.xi - movimento.xf) <= dist)


def dentro(x, y):
    return (x >= 0 and x <= N-1 and y >= 0 and y <= N-1)


def movimento_valido():
    if not dentro(movimento.xi, movimento.yi) or not dentro(movimento.xf, movimento.yf):
        return False
    if tabul.tabul[movimento.yi][movimento.xi] == movimento.jog and tabul.tabul[movimento.yf][movimento.xf] == 0 and adjacente(1):
        movimento.tipo = 0
        return True
    if tabul.tabul[movimento.yi][movimento.xi] == movimento.jog and tabul.tabul[movimento.yf][movimento.xf] == 0 and adjacente(2):
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
    nmovs = 0
    if tabul.tabul[yi][xi] == jog:
        for k in range(N):
            for l in range(N):
                movimento.jog = jog
                movimento.yi = yi
                movimento.xi = xi
                movimento.yf = k
                movimento.xf = l
                if movimento_valido():
                    assinala_quad(k, l, screen)
                    nmovs += 1


def conta_pecas(jog):
    pecas = 0
    for i in range(N):
        for j in range(N):
            if tabul.tabul[i][j] == jog:
                pecas += 1
    return pecas


def jogadas_validas():
    nmovs = 0
    for i in range(N):
        for j in range(N):
            if tabul.tabul[i][j] == 0:
                nmovs += 1
    return nmovs


def fim_jogo():
    n = jogadas_validas()
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
    if cl == 0 and tabul.tabul[py][px] == movimento.jog:
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
    for yi in range(N):
        for xi in range(N):
            if tabul.tabul[yi][xi] == movimento.jog:
                for k in range(0, N):
                    for l in range(0, N):
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

                yi = int(click[1] // sq)
                xi = int(click[0] // sq)
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
