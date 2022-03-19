import pygame as p

# Defino o estado do jogo quando começa
# Notação: 0 - espaço vazio  1 - peça vermelha  2 - peça azul  3 - parede
# A variável jogador irá manter track de quem joga no momento, se for True, é o jogador, se for False, é o PC
# O histórico manterá guardado as jogadas durante a partida.


class GameState():
    def __init__(self):

        self.board = [
            ["1", "0", "0", "0", "0", "0", "2"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "3", "0", "0", "0"],
            ["0", "0", "3", "0", "3", "0", "0"],
            ["0", "0", "0", "3", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["2", "0", "0", "0", "0", "0", "1"],
        ]

        self.jogador = True

        self.historico = []


p.init()  # Inicio um tabuleiro e defino o tamanho da janela, quantidade de quadrados, FPS
WIDTH = 600
HEIGHT = 600
DIMENSION = 7
MAX_FPS = 15
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {}

# Ir buscar as imagens das peças do jogo


def loadImages():
    pieces = ["1", "2"]
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
            if board[r][c] == "3":
                p.draw.rect(screen, p.Color("gray"), p.Rect(
                    c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))

# Colocar as peças no tabuleiro


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "0" and piece != "3":
                screen.blit(IMAGES[piece], p.Rect(
                    c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Desenhar o estado do tabuleiro ditado pelo ataxxengine.py


def drawGameState(screen, gs):
    drawBoard(screen, gs.board)
    drawPieces(screen, gs.board)


# Função que trata do movimento das peças
def moverpeca():
    2


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Define o tamanho da janela
    clock = p.time.Clock()  # Faz o jogo correr no tempo
    screen.fill(p.Color("black"))  # Fundo da janela preto
    gs = GameState()  # Carrega o estado do jogo para uma variável
    print(gs.board)  # DEBUG: Dá print na consola do estado do jogo (TIRAR NO FIM)
    loadImages()  # Carrega as imagens
    # Executa a função de desenhar o tabuleiro no janela
    drawGameState(screen, gs)

    # O jogo funcionará até ser comandado o contrário (ex. sair do jogo)
    running = True

    # Variáveis usadas para o evento de clickar no tabuleiro
    qdselecionado = ()
    qdsclickados = []
    primeiroclick = ()
    segundoclick = ()

    while running:

        # Desliga o jogo quando se carrega no X
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        # Guarda a localização do rato quando se carrega , formato click[x,y]
            elif e.type == p.MOUSEBUTTONDOWN:
                click = p.mouse.get_pos()

                # Transforma as coordenadas (números grandes e burros) para algo o quadrado que selecionei
                col = click[0] // SQ_SIZE
                row = click[1] // SQ_SIZE

                # Verifica se é o primeiro clique ou o segundo
                if qdselecionado is None and gs.board[qdselecionado(1)][qdselecionado(2)]:
                    primeiroclick = qdselecionado

                # Já há uma peça no quadrado que clicamos aseguir, não há movimento e damos reset aos cliques
                elif primeiroclick is not None and gs.board[qdselecionado(1)][qdselecionado(2)] is not None:
                    primeiroclick = None

                elif primeiroclick is not None and gs.board[qdselecionado(1)][qdselecionado(2)] is None:
                    moverpeca()

                # Dá reset aos cliques se carregar no mesmo quadrado duas vezes
                if qdselecionado == (row, col):
                    qdselecionado = ()
                    qdsclickados = []
                else:
                    qdselecionado = (row, col)

                # Diz que o quadrado que selecionei foi (X,Y) (vai de 1 a 8)
                qdselecionado = (row, col)

        # A taxa de atualização será de 15 frames per second
        clock.tick(MAX_FPS)
        p.display.flip()


main()
