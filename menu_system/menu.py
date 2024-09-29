import pygame
from server import *

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('=>', 15, self.cursor_rect.x, self.cursor_rect.y, self.game.WHITE)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.highscoresx, self.highscoresy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.quitx, self.quity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2 - 80, self.game.DISPLAY_H / 2 - 20, self.game.WHITE)
            if self.game.game_over:
                self.game.draw_text("Start Game", 20, self.startx - 80, self.starty, self.game.WHITE)
            else:
                self.game.draw_text("Resume", 20, self.startx - 80, self.starty, self.game.WHITE)
            self.game.draw_text("Highscores", 20, self.highscoresx - 80, self.highscoresy, self.game.WHITE)
            self.game.draw_text("Credits", 20, self.creditsx - 80, self.creditsy, self.game.WHITE)
            self.game.draw_text("Quit", 20, self.quitx - 80, self.quity, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.highscoresx + self.offset, self.highscoresy)
                self.state = 'Highscores'
            elif self.state == 'Highscores':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.highscoresx + self.offset, self.highscoresy)
                self.state = 'Highscores'
            elif self.state == 'Highscores':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Highscores':
                #self.game.curr_menu = self.game.highscores
                leaderboard = self.game.server.get_leaderboard()
                #print leaderboard sorted by score
                position = 1
                for name, score in sorted(leaderboard.items(), key=lambda x: x[1], reverse=True):
                    print(f'{position} :: User: {name} Score: {score}')
                    position += 1
            
            elif self.state == 'Credits':
                #self.game.curr_menu = self.game.credits
                pass
            elif self.state == 'Quit':
                self.game.running = False
            self.run_display = False