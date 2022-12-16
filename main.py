import math
import os.path
import time
import pygame
import queue

from leaderboard import Leaderboard
from endstate import Endstate
from board import Board

EMPTY = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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
    screen = pygame.display.set_mode((700, 600))
    board = Board()
    board.random_board()
    while not board.is_solvable():
        board = Board()
        board.random_board()
    pygame.init()
    pygame.display.set_caption("15 Puzzle")
    cells = []
    for x in range(0, 4):
        for y in range(0, 4):
            cell = pygame.Rect(y * 150 + 100, x * 150, 150, 150)
            cells.append(cell)
    screen.fill(WHITE)
    board.draw_board(screen)
    pygame.display.update()
    start = 0.00
    curr_time = 0.00
    move_count = 0
    state = "game"
    while 1:
        if state == "game":
            if start != 0:
                curr_time = time.time() - start
            curr_time = round(curr_time, 2)
            font = pygame.font.SysFont("monospace", 20)
            cover = pygame.Rect(10, 10, 80, 40)
            pygame.draw.rect(screen, WHITE, cover)
            time_text = font.render("Timer:", True, BLACK)
            screen.blit(time_text, (20, 10))
            timer = font.render(str(curr_time), True, BLACK)
            screen.blit(timer, (20, 30))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start == 0:
                        start = time.time()
                    if not board.is_complete():
                        if event.button == 1:
                            for i in range(0, 16):
                                if cells[i].collidepoint(event.pos):
                                    move_count += board.make_move(math.floor(i / 4), i % 4)
                                    if board.is_complete():
                                        save(curr_time, move_count)
                                        state = "end"
                                    else:
                                        board.draw_board(screen)
                                        pygame.display.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        leader = Leaderboard(screen)
                        leader.leaderboard_screen(screen)
                    elif event.key == pygame.K_ESCAPE:
                        state = "end"
        if state == "end":
            end = Endstate(screen, move_count, curr_time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if end.restart.collidepoint(event.pos):
                        main()
                    if end.leaderboard.collidepoint(event.pos):
                        state = "leader"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
        if state == "leader":
            leader = Leaderboard(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if leader.back.collidepoint(event.pos):
                        state = "end"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


main()
