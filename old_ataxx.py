<<<<<<< HEAD

import pygame as p

# Defino o estado do jogo quando começa
# Notação: 0 - espaço vazio  1 - peça vermelha  2 - peça azul  8 - parede
# A variável jogador irá manter track de quem joga no momento, se for True, é o jogador, se for False, é o PC
# O histórico manterá guardado as jogadas durante a partida.


class GameState():
    def __init__(self):

        self.board = [
            ["1", "0", "0", "0", "0", "0", "2"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "8", "0", "0", "0"],
            ["0", "0", "8", "0", "8", "0", "0"],
            ["0", "0", "0", "8", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["2", "0", "0", "0", "0", "0", "1"],
        ]

        self.historico = []

        self.jogador = True                  # True = Jogador Azul  / False = Jogador Vermelho

        self.moves = [(-1, 1), (0, 1), (1, 1), (-1, 0),
                      (1, 0), (-1, -1), (0, -1), (1, -1),
                      (-2, 2), (-2, 1), (-2, 0), (-2, -1),
                      (-2, -2), (-1, 2), (-1, -2),(0, 2),
                      (0, -2), (1, 2), (1, -2), (2, 2),
                      (2, 1), (2, 0), (2, -1), (2, -2)]

    def mudar_turno(self):
        # de cada vez que esta função é executada, o jogo muda de turno.
        self.jogador = not self.jogador

    ##########################################################################################

#Variáveis Globais
p.init()
WIDTH = 600
HEIGHT = 600
DIMENSION = 7
MAX_FPS = 15
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {}

# Ir buscar as imagens das peças do jogo
def loadImages():
    pieces = ["1", "2", "3"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            "images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Desenhar o actual tabuleiro na janela
def drawBoard(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = p.Color(66, 179, 132)
            p.draw.rect(screen, color, p.Rect(
            c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))
            if board[r][c] == "8":
                 p.draw.rect(screen, (128,128,128), (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))

# Colocar as peças no tabuleiro
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "0" and piece != "8":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Desenha uma marca na peça carregada
def drawSelected(screen, board, primeiroclick):
    i = int(primeiroclick[0])
    j = int(primeiroclick[1])
    print(i , j)
    if board[j][i] == '1' or board[j][i] == '2':
        screen.blit(IMAGES['3'], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.draw.rect(screen, p.Color(255,255,255), (j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))

# Desenhar o estado do tabuleiro ditado pelo ataxxengine.py
def drawGameState(screen, gs):
    drawBoard(screen, gs.board)
    drawPieces(screen, gs.board)

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Define o tamanho da janela
    clock = p.time.Clock()  # Faz o jogo correr no tempo
    screen.fill((0,0,0)) #background branco  # Fundo da janela preto
    gs = GameState()  # Carrega o estado do jogo para uma variável
#    print(gs.board)  # DEBUG: Dá print na consola do estado do jogo (TIRAR NO FIM)
    loadImages()  # Carrega as imagens

    # Executa a função de desenhar o tabuleiro no janela
    drawGameState(screen, gs)

    # O jogo funcionará até ser comandado o contrário (ex. sair do jogo)
    running = True

    # A taxa de atualização será de 15 frames per second
    clock.tick(MAX_FPS)
    p.display.flip()

    # Variáveis usadas para o evento de clickar no tabuleiro
    qdselecionado = ()
    primeiroclick = ()

    while running:

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                running = False

            # Guarda a localização do rato quando se carrega , formato click[x,y]
            elif e.type == p.MOUSEBUTTONDOWN:
                click = p.mouse.get_pos()

            # Transforma as coordenadas para o quadrado em específico
                col = click[1] // SQ_SIZE
                row = click[0] // SQ_SIZE
                qdselecionado = (row, col)

            # Verifica se é o primeiro clique ou o segundo
                if primeiroclick == ():
                    primeiroclick = qdselecionado
                    qdselecionado = ()

            # At this point, temos de ver se carregamos num quadrado com uma peça
                if gs.board[primeiroclick[0]][primeiroclick[1]] != '0' and gs.board[primeiroclick[0]][primeiroclick[1]] !='3' and gs.board[primeiroclick[0]][primeiroclick[1]] != '8' :
                    drawBoard(screen,gs.board)
                    drawSelected(screen,gs.board,primeiroclick)
                    drawPieces(screen,gs.board)

                #I'll work on this later ffs

            # Dá reset aos cliques se carregar no mesmo quadrado duas vezes
                if primeiroclick == qdselecionado:
                    primeiroclick = ()
                    qdselecionado = ()
                    print("Carregado 2 vezes no mesmo, cliques resetados")

                if primeiroclick != () and qdselecionado !=():
                    primeiroclick = ()
                    qdselecionado = ()

=======

import pygame as p

# Defino o estado do jogo quando começa
# Notação: 0 - espaço vazio  1 - peça vermelha  2 - peça azul  8 - parede
# A variável jogador irá manter track de quem joga no momento, se for True, é o jogador, se for False, é o PC
# O histórico manterá guardado as jogadas durante a partida.


class GameState():
    def __init__(self):

        self.board = [
            ["1", "0", "0", "0", "0", "0", "2"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "8", "0", "0", "0"],
            ["0", "0", "8", "0", "8", "0", "0"],
            ["0", "0", "0", "8", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["2", "0", "0", "0", "0", "0", "1"],
        ]

        self.historico = []

        self.jogador = True                  # True = Jogador Azul  / False = Jogador Vermelho

        self.moves = [(-1, 1), (0, 1), (1, 1), (-1, 0),
                      (1, 0), (-1, -1), (0, -1), (1, -1),
                      (-2, 2), (-2, 1), (-2, 0), (-2, -1),
                      (-2, -2), (-1, 2), (-1, -2),(0, 2),
                      (0, -2), (1, 2), (1, -2), (2, 2),
                      (2, 1), (2, 0), (2, -1), (2, -2)]

    def mudar_turno(self):
        # de cada vez que esta função é executada, o jogo muda de turno.
        self.jogador = not self.jogador

    ##########################################################################################

#Variáveis Globais
p.init()
WIDTH = 600
HEIGHT = 600
DIMENSION = 7
MAX_FPS = 15
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {}

# Ir buscar as imagens das peças do jogo
def loadImages():
    pieces = ["1", "2", "3"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            "images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Desenhar o actual tabuleiro na janela
def drawBoard(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = p.Color(66, 179, 132)
            p.draw.rect(screen, color, p.Rect(
            c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))
            if board[r][c] == "8":
                 p.draw.rect(screen, (128,128,128), (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))

# Colocar as peças no tabuleiro
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "0" and piece != "8":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Desenha uma marca na peça carregada
def drawSelected(screen, board, primeiroclick):
    i = int(primeiroclick[0])
    j = int(primeiroclick[1])
    print(i , j)
    if board[j][i] == '1' or board[j][i] == '2':
        # screen.blit(IMAGES['3'], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        # p.draw.rect(screen, p.Color(255,255,255), (j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))

# Desenhar o estado do tabuleiro ditado pelo ataxxengine.py
def drawGameState(screen, gs):
    drawBoard(screen, gs.board)
    drawPieces(screen, gs.board)

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Define o tamanho da janela
    clock = p.time.Clock()  # Faz o jogo correr no tempo
    screen.fill((0,0,0)) #background branco  # Fundo da janela preto
    gs = GameState()  # Carrega o estado do jogo para uma variável
#    print(gs.board)  # DEBUG: Dá print na consola do estado do jogo (TIRAR NO FIM)
    loadImages()  # Carrega as imagens

    # Executa a função de desenhar o tabuleiro no janela
    drawGameState(screen, gs)

    # O jogo funcionará até ser comandado o contrário (ex. sair do jogo)
    running = True

    # A taxa de atualização será de 15 frames per second
    clock.tick(MAX_FPS)
    p.display.flip()

    # Variáveis usadas para o evento de clickar no tabuleiro
    qdselecionado = ()
    primeiroclick = ()

    while running:

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                running = False

            # Guarda a localização do rato quando se carrega , formato click[x,y]
            elif e.type == p.MOUSEBUTTONDOWN:
                click = p.mouse.get_pos()

            # Transforma as coordenadas para o quadrado em específico
                col = click[1] // SQ_SIZE
                row = click[0] // SQ_SIZE
                qdselecionado = (row, col)

            # Verifica se é o primeiro clique ou o segundo
                if primeiroclick == ():
                    primeiroclick = qdselecionado
                    qdselecionado = ()

            # At this point, temos de ver se carregamos num quadrado com uma peça
                if gs.board[primeiroclick[0]][primeiroclick[1]] != '0' and gs.board[primeiroclick[0]][primeiroclick[1]] !='3' and gs.board[primeiroclick[0]][primeiroclick[1]] != '8' :
                    drawBoard(screen,gs.board)
                    drawSelected(screen,gs.board,primeiroclick)
                    drawPieces(screen,gs.board)

                #I'll work on this later ffs

            # Dá reset aos cliques se carregar no mesmo quadrado duas vezes
                if primeiroclick == qdselecionado:
                    primeiroclick = ()
                    qdselecionado = ()
                    print("Carregado 2 vezes no mesmo, cliques resetados")

                if primeiroclick != () and qdselecionado !=():
                    primeiroclick = ()
                    qdselecionado = ()

>>>>>>> c38c10f52403f2acf3ba2a525979d17851d9301b
main()