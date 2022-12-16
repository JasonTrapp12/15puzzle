import math
import os.path
import random
import time
import numpy
import pygame
import queue

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Endstate(object):

    def __init__(self, screen, num_moves, curr_time):
        self.active_state = True
        self.restart = None
        self.leaderboard = None
        self.end_state(screen, num_moves, curr_time)

    def end_state(self, screen, num_moves, curr_time):
        screen.fill(WHITE)
        # display time
        time_f = pygame.font.SysFont("monospace", 60)
        time_t = time_f.render(str(curr_time) + " seconds", True, BLACK)
        screen.blit(time_t, (120, 100))

        # completed message
        complete = pygame.font.SysFont("monospace", 39)
        text = complete.render("Puzzle completed in " + str(num_moves) + " moves", True, BLACK)
        screen.blit(text, (20, 300))

        # restart button
        restart_t = pygame.font.SysFont("monospace", 20)
        restart_text = restart_t.render("Restart", True, BLACK)
        screen.blit(restart_text, (198, 412))
        self.restart = pygame.Rect(180, 400, 120, 50)
        pygame.draw.rect(screen, BLACK, self.restart, 2)

        # leaderboard button
        leaderboard_t = pygame.font.SysFont("monospace", 20)
        leaderboard_text = leaderboard_t.render("Leaderboard", True, BLACK)
        screen.blit(leaderboard_text, (350, 412))
        self.leaderboard = pygame.Rect(332, 400, 170, 50)
        pygame.draw.rect(screen, BLACK, self.leaderboard, 2)

        pygame.display.update()

