import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Leaderboard(object):

    def __init__(self, screen):
        self.active_state = True
        self.back = None
        self.best_times = self.get_best_times("15puzzlescores.txt")
        self.leaderboard_screen(screen)

    def get_best_times(self, filename):
        times = [0.00, 0.00, 0.00]
        with open(filename) as f:
            for i in range(0, 3):
                # adds the time from the file
                timer = f.readline()
                if not timer:
                    break
                else:
                    times[i] = (timer.split()[1])
        f.close()
        for l in range(0, 3):
            if times[l] is None:
                times[l] = 0.00
        return times

    def leaderboard_screen(self, screen):
        screen.fill(WHITE)
        # draw leaderboard
        # vertical lines
        pygame.draw.line(screen, BLACK, (140, 45), (140, 445), 2)
        pygame.draw.line(screen, BLACK, (560, 45), (560, 445), 2)
        pygame.draw.line(screen, BLACK, (224, 145), (224, 445), 2)
        # horizontal lines
        for i in range(0, 5):
            pygame.draw.line(screen, BLACK, (140, 45 + 100 * i), (560, 45 + 100 * i), 2)

        # title
        font = pygame.font.SysFont("monospace", 50)
        title = font.render("Fastest Times", True, BLACK)
        screen.blit(title, (155, 70))

        # numbers 1-5 with times
        for l in range(0, 3):
            num = font.render("#" + str(l + 1), True, BLACK)
            screen.blit(num, (155, 175 + l * 100))
            time_text = font.render(str(self.best_times[l]), True, BLACK)
            screen.blit(time_text, (290, 175 + l * 100))

        # back button
        self.back = pygame.Rect(250, 500, 200, 50)
        arrow = pygame.image.load('backarrow.png')
        arrow = pygame.transform.scale(arrow, (200, 50))
        screen.blit(arrow, (250, 500))
        pygame.display.update()
