import math
import os.path
import random
import time
import numpy
import pygame
import queue

from leaderboard import Leaderboard

EMPTY = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Board:
    board = numpy.empty((4, 4), int)

    def random_board(self):
        numbers = list(range(16))
        random.shuffle(numbers)
        index = 0
        for i in range(0, 4):
            for j in range(0, 4):
                self.board[i, j] = numbers[index]
                index += 1

    def make_move(self, x, y):
        if x - 1 > -1 and self.board[x - 1, y] == EMPTY:
            self.board[x - 1, y] = self.board[x, y]
        elif x + 1 < 4 and self.board[x + 1, y] == EMPTY:
            self.board[x + 1, y] = self.board[x, y]
        elif y - 1 > -1 and self.board[x, y - 1] == EMPTY:
            self.board[x, y - 1] = self.board[x, y]
        elif y + 1 < 4 and self.board[x, y + 1] == EMPTY:
            self.board[x, y + 1] = self.board[x, y]
        else:
            return 0
        self.board[x, y] = EMPTY
        return 1

    def find_empty(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.board[i, j] == EMPTY:
                    return i, j

    def is_complete(self):
        for i in range(1, 16):
            if self.board[math.floor((i - 1) / 4), (i - 1) % 4] != i:
                return False
        return True

    def to_list(self):
        lst = []
        for x in range(0, 4):
            for y in range(0, 4):
                lst.append(self.board[x, y])
        return lst

    def is_solvable(self):
        boardlist = self.to_list()
        inversions = 0
        row = 0
        blank_row = 0
        for i in range(0, 16):
            if i % 4 == 0:
                row += 1
            if boardlist[i] == 0:
                blank_row = row
            for j in range(i + 1, 16):
                if boardlist[i] > boardlist[j] > 0:
                    inversions += 1
        # if its on an odd row
        if blank_row % 2 == 0:
            # even number of inversions means its solvable, odd unsolvable
            return inversions % 2 == 0
        # even row
        else:
            # odd number of inversions means its solvable, even unsolvable
            return inversions % 2 != 0

    def find_possible_moves(self):
        moves = []
        x, y = self.find_empty()
        if x - 1 >= 0:
            board = Board()
            b = copy_board(self.board)
            b[x, y] = b[x - 1, y]
            b[x - 1, y] = EMPTY
            board.board = b
            moves.append(board)
        if x + 1 < 4:
            board = Board()
            b = copy_board(self.board)
            b[x, y] = b[x + 1, y]
            b[x + 1, y] = EMPTY
            board.board = b
            moves.append(board)
        if y - 1 >= 0:
            board = Board()
            b = copy_board(self.board)
            b[x, y] = b[x, y - 1]
            b[x, y - 1] = EMPTY
            board.board = b
            moves.append(board)
        if y + 1 < 4:
            board = Board()
            b = copy_board(self.board)
            b[x, y] = b[x, y + 1]
            b[x, y + 1] = EMPTY
            board.board = b
            moves.append(board)
        return moves


def copy_board(board):
    dupe = numpy.zeros((4, 4))
    for i in range(0, 4):
        for j in range(0, 4):
            dupe[i, j] = board[i, j]
    return dupe


def draw_board(board, screen):
    screen.fill(WHITE)
    for i in range(0, 5):
        # vertical lines
        pygame.draw.line(screen, BLACK, ((i * 150) + 100, 0), ((i * 150) + 100, 600), 2)
        # horizontal lines
        pygame.draw.line(screen, BLACK, (100, i * 150), (700, i * 150), 2)
    for x in range(0, 4):
        for y in range(0, 4):
            font = pygame.font.SysFont("monospace", 60)
            if board[y, x] != 0:
                num = font.render(str(board[y, x]), True, BLACK)
                screen.blit(num, ((x * 150) + 150, (y * 150) + 50))


def end_state(screen, num_moves, curr):
    screen.fill(WHITE)
    time_f = pygame.font.SysFont("monospace", 60)
    time_t = time_f.render(str(curr) + " seconds", True, BLACK)
    screen.blit(time_t, (120, 100))
    complete = pygame.font.SysFont("monospace", 39)
    text = complete.render("Puzzle completed in " + str(num_moves) + " moves", True, BLACK)
    screen.blit(text, (20, 300))
    restart_t = pygame.font.SysFont("monospace", 20)
    restart_text = restart_t.render("Restart", True, BLACK)
    screen.blit(restart_text, (303, 412))
    restart = pygame.Rect(285, 400, 120, 50)
    pygame.draw.rect(screen, BLACK, restart, 2)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart.collidepoint(event.pos):
                    main()
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def hash_board(board):
    return board.data.tobytes()


def num_wrong_tiles(board):
    count = 0
    for i in range(1, 16):
        if board[math.floor((i - 1) / 4), (i - 1) % 4] != i:
            count += 1
    return count


def solver(board, screen):
    q = queue.Queue()
    q.put(board)
    visited = []
    while not q.empty():
        curr = q.get()
        print(str(curr))
        visited.append(hash_board(curr.board))
        if curr.is_complete():
            print("solved")
            break
        for move in board.find_possible_moves():
            if hash_board(move.board) in visited:
                continue
            draw_board(move.board, screen)
            q.put(move)


def save(timer, move_count):
    if os.path.exists("15puzzlescores.txt"):
        with open("15puzzlescores.txt", "r+") as f:
            contents = f.readlines()
            if len(contents) == 0:
                contents.insert(0, "Time: " + str(timer) + " Moves: " + str(move_count) + "\n")
                f.truncate(0)
                f.seek(0)
                f.writelines(contents)
                f.close()
                return
            for line in contents:
                entry_time = line.split()[1]
                if timer < float(entry_time):
                    contents.insert(contents.index(line), "Time: " + str(timer) + " Moves: " + str(move_count) + "\n")
                    f.truncate(0)
                    f.seek(0)
                    f.writelines(contents)
                    f.close()
                    return
                elif contents.index(line) == len(contents) - 1:
                    contents.insert(len(contents) + 1, "Time: " + str(timer) + " Moves: " + str(move_count) + "\n")
                    f.truncate(0)
                    f.seek(0)
                    f.writelines(contents)
                    f.close()
                    return

    else:
        f = open("15puzzlescores.txt", "x")
        f.close()
        save(timer, move_count)


def main():
    board = Board()
    board.random_board()
    while not board.is_solvable():
        board = Board()
        board.random_board()
    pygame.init()
    pygame.display.set_caption("15 Puzzle")
    screen = pygame.display.set_mode((700, 600))
    cells = []
    for x in range(0, 4):
        for y in range(0, 4):
            cell = pygame.Rect(y * 150 + 100, x * 150, 150, 150)
            cells.append(cell)
    screen.fill(WHITE)
    draw_board(board.board, screen)
    pygame.display.update()
    start = time.time()
    move_count = 0
    while 1:
        curr = time.time() - start
        curr = round(curr, 2)
        cover = pygame.Rect(8, 8, 80, 20)
        pygame.draw.rect(screen, WHITE, cover)
        font = pygame.font.SysFont("monospace", 20)
        timer = font.render(str(curr), True, BLACK)
        screen.blit(timer, (20, 10))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not board.is_complete():
                    if event.button == 1:
                        for i in range(0, 16):
                            if cells[i].collidepoint(event.pos):
                                move_count += board.make_move(math.floor(i / 4), i % 4)
                                if board.is_complete():
                                    save(curr, move_count)
                                    end_state(screen, move_count, curr)
                                else:
                                    draw_board(board.board, screen)
                                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    leader = Leaderboard()
                    leader.leaderboard_screen(screen)
                elif event.key == pygame.K_ESCAPE:
                    end_state(screen, move_count, curr)


main()