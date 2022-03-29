import pygame
import time
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
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    jog = 0
    tipo = 0
    vencedor = 0


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

def comer():
    dx = -1
    dy = -1
    for dx in range(dx, 2):
        for dy in range(dy, 2):
            try:
                if movimento.yf + dy == -1 and movimento.xf + dx == -1:
                    if tabul[0][0] == outroJog(movimento.jog):
                        tabul[movimento.yf + dy +
                              1][movimento.xf + dx+1] = movimento.jog
                elif movimento.yf + dy == -1:
                    if tabul[0][movimento.xf + dx] == outroJog(movimento.jog):
                        tabul[movimento.yf + dy +
                              1][movimento.xf + dx] = movimento.jog
                elif movimento.xf + dx == -1:
                    if tabul[movimento.yf + dy][0] == outroJog(movimento.jog):
                        tabul[movimento.yf + dy][movimento.xf +
                                                 dx+1] = movimento.jog

                elif tabul[movimento.yf + dy][movimento.xf + dx] == outroJog(movimento.jog):
                    tabul[movimento.yf + dy][movimento.xf + dx] = movimento.jog
            except IndexError:
                pass
        dy = -1


def executa_movimento():
    tabul[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        tabul[movimento.yi][movimento.xi] = 0
    comer()


def adjacente(dist):
    return(
        abs(movimento.xi - movimento.xf) == dist and abs(movimento.yi - movimento.yf) <= dist or
        abs(movimento.yi - movimento.yf) == dist and abs(movimento.xi -
                                                         movimento.xf) <= dist
    )


def dentro(x, y):
    return (x >= 0 and x <= N-1 and y >= 0 and y <= N-1)


def movimento_valido():
    if not dentro(movimento.xi, movimento.yi) or not dentro(movimento.xf, movimento.yf):
        return False
    if tabul[movimento.yi][movimento.xi] == movimento.jog and tabul[movimento.yf][movimento.xf] == 0 and adjacente(1):
        movimento.tipo = 0
        return True
    if tabul[movimento.yi][movimento.xi] == movimento.jog and tabul[movimento.yf][movimento.xf] == 0 and adjacente(2):
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
    if tabul[yi][xi] == jog:
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
             if tabul[i][j] == jog:
                 pecas +=1
    return pecas

def jogadas_validas():
    nmovs = 0
    for i in range(N):
        for j in range(N):
            if tabul[i][j] == 0:
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
    print("Jogador", movimento.vencedor, "ganha !")


def jogada_Humano(cl, px, py, screen):
    if cl == 0 and tabul[py][px] == movimento.jog:
        movimento.xi = px
        movimento.yi = py
        assinala_quad(py, px, screen)
        jogadas_validas_pos(movimento.jog, py, px, screen)
    elif cl == 1:
        movimento.xf = px
        movimento.yf = py
        assinala_quad(movimento.xf, movimento.yf, screen)


def main():
    cl = 0
    nMovs = 1
    fim = 0
    movimento.jog = 1
    tipo = int(tipo_jogo())
    screen = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    mostra_tabul(screen, tabul)
    clock.tick(30)
    pygame.display.flip()
    running = True
    while running:
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
                        if cl == 0:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                            print("JOGADOR 1 ESCOLHEU PEÇA")
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            print("JOGADOR 1 ESCOLHEU MOVIMENTO")
                            if movimento_valido():
                                executa_movimento()
                                nMovs += 1
                                movimento.jog = outroJog(movimento.jog)
                            mostra_tabul(screen, tabul)

                    # else:
                    #     jogada_PC(jog, nMovs)

                else:
                    if tipo == 1 or tipo == 3:
                        if cl == 0:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 1
                            print("JOGADOR 2 ESCOLHEU PEÇA")
                        elif cl == 1:
                            jogada_Humano(cl, xi, yi, screen)
                            cl = 0
                            print("JOGADOR 2 ESCOLHEU MOVIMENTO")
                            if movimento_valido():
                                executa_movimento()
                                nMovs += 1
                                movimento.jog = outroJog(movimento.jog)
                            mostra_tabul(screen, tabul)

                    # else:
                    #     jogada_PC(jog, nMovs)
                    # ...
                    #

        pygame.display.flip()
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


'''
