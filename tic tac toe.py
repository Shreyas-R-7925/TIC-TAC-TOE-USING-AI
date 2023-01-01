import sys
import pygame
import numpy as np
import random
import copy

WIDTH = 600
HEIGHT = 600
BG_COLOR = (0, 238, 0)
ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS
LINE_COLOR = (0, 139, 0)
LINE_WIDTH = 15
CIRC_COLOR = (220, 20, 60)
RADIUS = SQSIZE // 4
CIRC_WIDTH = 15
CROSS_WIDTH = 20
CROSS_COLOR = (75, 0, 130)
WIN_LINE = (36, 36, 36)
OFFSET = 50
FONT = (0,255,255)
HELP = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE                                   Press h to view the commands')
screen.fill(BG_COLOR)

font = pygame.font.Font('freesansbold.ttf', 32)
text_r = font.render('    r --> Start/Restart', True, FONT )
text_0 = font.render('        0 --> Easy level', True, FONT )
text_1 = font.render('        1 --> Hard level', True, FONT)
text_g = font.render('      g --> Player1 vs Player2', True, FONT)
text_h = font.render('        h --> Help', True, FONT)
text1 = text_h.get_rect()
text2 = text_0.get_rect()
text3 = text_1.get_rect()
text4 = text_g.get_rect()
text5 = text_r.get_rect()
text1.center = (WIDTH // 2.5, WIDTH // 4)
text2.center = (WIDTH // 2.5, WIDTH // 3)
text3.center = (WIDTH // 2.5, WIDTH // 2.35)
text4.center = (WIDTH // 2.5, WIDTH // 1.95)
text5.center = (WIDTH // 2.5, WIDTH // 1.65)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
        return 0 if there is no win yet or game is drawn at the terminal case
        return 1 if player 1 wins
        return 2 if player 2 wins
        '''
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:

                if show:
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, WIN_LINE, iPos, fPos, LINE_WIDTH)
                    if self.squares[0][col] == 1:
                        pygame.display.set_caption('PLAYER-X WINS                      Press R to restart and choose your game mode')
                    else:
                        pygame.display.set_caption('PLAYER-O WINS                      Press R to restart and choose your game mode')
                return self.squares[0][col]
        
        # horizontal wins
        for rows in range(ROWS):
            if self.squares[rows][0] == self.squares[rows][1] == self.squares[rows][2] != 0:

                if show:
                    iPos = (20, rows * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, rows * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, WIN_LINE, iPos, fPos, LINE_WIDTH)
                    if self.squares[rows][0] == 1:
                        pygame.display.set_caption('PLAYER-X WINS                      Press R to restart and choose your game mode')
                    else:
                        pygame.display.set_caption('PLAYER-O WINS                      Press R to restart and choose your game mode')

                return self.squares[rows][0]
        # desc diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:

            if show:
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, WIN_LINE, iPos, fPos, CROSS_WIDTH)
                if self.squares[1][1] == 1:
                    pygame.display.set_caption("PLAYER-X WINS                          Press R to restart and choose your game mode")
                else:
                    pygame.display.set_caption("PLAYER-O WINS                          Press R to restart and choose your game mode")
            return self.squares[1][1]  # common sqr
        
        # asc diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:

            if show:
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, WIN_LINE, iPos, fPos, CROSS_WIDTH)
                if self.squares[1][1] == 1:
                    pygame.display.set_caption("PLAYER-X WINS                          Press R to restart and choose your game mode")
                else:
                    pygame.display.set_caption("PLAYER-O WINS                          Press R to restart and choose your game mode")
            return self.squares[1][1]  # common sqr

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]  # (row, col)

    def minimax(self, board, maximizing):

        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100  # can use any number
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100  # can use any number
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of : {eval}')

        return move  # row, col

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # 1-cross(User) and 2-circle(AI)
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        screen.fill(BG_COLOR)
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1
        if self.player % 2 == 0:
            pygame.display.set_caption('                                                                Player O\'s turn')
        else:
            pygame.display.set_caption('                                                                Player X\'s turn')

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()  # restarting all the attributes to the default values


def main():
    # objects
    game = Game()
    board = game.board     
    ai = game.ai

    while True:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_g:  # g - game mode
                    game.change_gamemode()
                    pygame.display.set_caption('Tic Tac Toe :                                                User1 vs User2')
            
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    pygame.display.set_caption('TIC TAC TOE                                  Press h to view the commands')

                if event.key == pygame.K_0:
                    ai.level = 0  # 0 - random ai
                    pygame.display.set_caption('Tic Tac Toe :                                                     Level EASY')

                if event.key == pygame.K_1:
                    ai.level = 1  # 1 - hard ai
                    pygame.display.set_caption('Tic Tac Toe :                                                     Level HARD')

                if event.key == pygame.K_h:
                    screen.fill(HELP)
                    screen.blit(text_r, text1)
                    screen.blit(text_0, text2)
                    screen.blit(text_1, text3)
                    screen.blit(text_g, text4)
                    screen.blit(text_h, text5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                
                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update screen
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        if board.isfull() and board.final_state()==0:
            pygame.display.set_caption('Game ended in a DRAW!!               Press r to restart and choose game mode')

        pygame.display.update()

main()
