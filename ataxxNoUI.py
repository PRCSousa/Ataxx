# Importamos as librarias:
# Time: This lib is used to create time intervals in the code
# Random: This lib generates pseudo-random values to enhance the PC human-like behaviour

import copy
import numpy
import random

# Window Size
SIZE = 600

# Class that saves the gamestate, like the size of the board (N), the square size (dynamic to the window size), and the board setup


class gamestate:
    N = 1
    sq = SIZE / N
    tabuleiro = []
    nMovs = 1
    vencedor = 0


# This class saves the movement data (initial and final x and y's, the player moving, the game type and the winner)


class movimento:
    xi = 0
    yi = 0
    yf = 0
    xf = 0
    jog = 0
    tipo = 0
    vencedor = 0

# This class is a temporary data saver, which saves the best move possible by the computer


class bestmov:
    xi = 0
    yi = 0
    yf = 0
    xf = 0

# This class solely saves the game before the computer move, so it can restore it after every try


class save:
    game = []

# Function to read the chosen board by the player


def escolhetabul():
    print("Tabuleiros:")
    print("1) Original")
    print("2) Sem paredes")
    print("3) Circular")
    print("4) Coração")
    print("5) Alvo")
    print("6) Xadrez")
    print("7) Foxy")
    numtabul = input()
    tabuleiro = "tabuleiros/tab"+numtabul+".txt"
    return tabuleiro

# Function to, after the player has chosen the board, loads it into the gamestate class


def letabul(ficheiro):
    f = open(ficheiro)
    gamestate.N = int(f.readline())
    gamestate.sq = SIZE / gamestate.N
    tabuleiro = []
    for i in range(gamestate.N):
        tabuleiro.append(list(map(int, f.readline().split())))
    f.close()
    gamestate.tabuleiro = tabuleiro

# The next 2 functions save the gamestate and restores it when called, respectively


def copia():
    save.game = copy.deepcopy(gamestate.tabuleiro)


def restaura():
    gamestate.tabuleiro = save.game

# This function changes the player turn


def outroJog(jog):
    if jog == 1:
        return 2
    else:
        return 1


# This function deals with taking of the opponent pieces, after a movement is done, any adjacent pieces are swapped
# Note: Every if in the try...except is to stop taking from across the board because tabuleiro[-1] = tabuleiro[N]


def comer():
    dx = -1
    dy = -1
    for dx in range(dx, 2):
        for dy in range(dy, 2):
            try:
                if movimento.yf + dy == -1 and movimento.xf + dx == -1:
                    if gamestate.tabuleiro[0][0] == outroJog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy +
                                            1][movimento.xf + dx+1] = movimento.jog
                elif movimento.yf + dy == -1:
                    if gamestate.tabuleiro[0][movimento.xf + dx] == outroJog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy +
                                            1][movimento.xf + dx] = movimento.jog
                elif movimento.xf + dx == -1:
                    if gamestate.tabuleiro[movimento.yf + dy][0] == outroJog(movimento.jog):
                        gamestate.tabuleiro[movimento.yf + dy][movimento.xf +
                                                               dx+1] = movimento.jog

                elif gamestate.tabuleiro[movimento.yf + dy][movimento.xf + dx] == outroJog(movimento.jog):
                    gamestate.tabuleiro[movimento.yf +
                                        dy][movimento.xf + dx] = movimento.jog
            except IndexError:
                pass
        dy = -1

# This function simply executes the movement, if the movement type is jumping,
# it also removes the piece from its old location, and then checks for piece taking


def executa_movimento():
    gamestate.tabuleiro[movimento.yf][movimento.xf] = movimento.jog
    if movimento.tipo == 1:
        gamestate.tabuleiro[movimento.yi][movimento.xi] = 0
    comer()

# Evaluation function, the computer decides it move by the heuristic placed here


def avalia():
    salt = random.random()
    return (conta_pecas(movimento.jog) - conta_pecas(outroJog(movimento.jog))+salt)

# Checks if the movement choice is either a jump or a multiplication


def adjacente(dist):
    return(
        abs(movimento.xi - movimento.xf) == dist and abs(movimento.yi - movimento.yf) <= dist or
        abs(movimento.yi - movimento.yf) == dist and abs(movimento.xi - movimento.xf) <= dist)

# Checks if the move is inside the board limits


def dentro(x, y):
    return (x >= 0 and x <= gamestate.N-1 and y >= 0 and y <= gamestate.N-1)

# Using the last 2 functions, this one checks if the move is totally valid
# Note: the first if removes the L like movement


def movimento_valido():
    if abs(movimento.yf - movimento.yi) == 2 and abs(movimento.xf - movimento.xi) == 1 or abs(movimento.xf - movimento.xi) == 2 and abs(movimento.yf - movimento.yi) == 1:
        return False
    if not dentro(movimento.xi, movimento.yi) or not dentro(movimento.xf, movimento.yf):
        return False
    if gamestate.tabuleiro[movimento.yi][movimento.xi] == movimento.jog and gamestate.tabuleiro[movimento.yf][movimento.xf] == 0 and adjacente(1):
        movimento.tipo = 0
        return True
    if gamestate.tabuleiro[movimento.yi][movimento.xi] == movimento.jog and gamestate.tabuleiro[movimento.yf][movimento.xf] == 0 and adjacente(2):
        movimento.tipo = 1
        return True

# Checks the amount of valid moves a player has


def jogadas_validas_total(jog):
    nmovs = 0
    for y in range(gamestate.N):
        for x in range(gamestate.N):
            if gamestate.tabuleiro[y][x] == jog:
                for k in range(gamestate.N):
                    for l in range(gamestate.N):
                        movimento.jog = jog
                        movimento.yi = y
                        movimento.xi = x
                        movimento.yf = k
                        movimento.xf = l
                        if movimento_valido():
                            nmovs += 1
    return nmovs

# Function that counts the amount of pieces the called player has


def conta_pecas(jog):
    pecas = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == jog:
                pecas += 1
    return pecas

# Function that returns the amount of empty squares


def quad_validos():
    nmovs = 0
    for i in range(gamestate.N):
        for j in range(gamestate.N):
            if gamestate.tabuleiro[i][j] == 0:
                nmovs += 1
    return nmovs

# Checks if the game has reached its end conditions, depending on which one it is,
# it set the winner as one of the players or as a draw


def fim_jogo():
    n = quad_validos()
    if conta_pecas(1) == 0 or conta_pecas(2) == 0:
        if conta_pecas(1) == 0:
            gamestate.vencedor = 2
            return -1
        else:
            gamestate.vencedor = 1
            return -1
    if n == 0:
        if (conta_pecas(1) - conta_pecas(2) > 0):
            gamestate.vencedor = 1
            return -1
        if (conta_pecas(1) - conta_pecas(2) < 0):
            gamestate.vencedor = 2
            return -1
        else:
            gamestate.vencedor = 0
            return -1
    else:
        return 0

# If one of the ending conditions has been reached, it prints who won


def finaliza():
    if gamestate.vencedor != 0:
        if gamestate.vencedor == 1:
            resultados.vermelho += 1
        else:
            resultados.azul += 1
    else:
        resultados.empate += 1


# Manages the computer made movements:
# For each piece it has, it tries every possivle move, by doing it, evaluating it, and restoring the game to before the move
# for each evaluation, it saves the movement with the best evaluation score and then, after every move has been played
# it does said best move


def jogada_PC():
    # Currently Not working
    # if jogadas_validas_total(movimento.jog) == 0:
    #     gamestate.nMovs += 1
    #     return
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

# Main function, executes:
# The type and board selection functions;
# Generates the window and the board
#  Begins the loop that sets the game playing


def game():
    cl = 0
    fim = 0
    movimento.jog = 1
    letabul(tabuleiro)
    running = True

    # While the game plays, it checks for events:
    # If the X is pressed, the game exits
    # If a click is made, it begins a chain of events explained next

    while running:

        # Computer's turn

        if gamestate.nMovs % 2:
            jogada_PC()
            gamestate.nMovs += 1
            movimento.jog = outroJog(movimento.jog)
        else:
            jogada_PC()
            gamestate.nMovs += 1
            movimento.jog = outroJog(movimento.jog)

        # It constatnly checks if the game has reached any end condition, and if it has, it finalizes it

        fim = fim_jogo()
        if fim == -1:
            resultados.diff.append(conta_pecas(1) - conta_pecas(2))
            finaliza()
            running = False


class resultados:
    vermelho = 0
    azul = 0
    empate = 0
    jogadas = []
    diff = []
    media = 0

def calculos():
    resultados.media = numpy.median(resultados.diff)




tabuleiro = escolhetabul()

total = int(input("Quantos testes quer realizar?: "))

for i in range(total):
    game()

calculos()

print("Vitórias do Vermelho: ",    resultados.vermelho)
print("Vitórias do Azul: ",        resultados.azul)
print("Empates: ",                 resultados.empate)
print("Diferença de peças média: ",resultados.media)
