import pygame
from server import *

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cur_offset = - 40
        self.x_offset = -240
        self.cursor_rect = pygame.Rect(self.mid_w + self.cur_offset + self.x_offset, self.mid_h-70, 20, 20)
        self.cursor_icon = pygame.image.load('snake-icon.png')
        self.cursor_icon = pygame.transform.scale(self.cursor_icon, (40, 40))

    def draw_cursor(self):
        #self.game.draw_text('=>', 25, self.cursor_rect.x, self.cursor_rect.y, self.game.WHITE)
        self.game.display.blit(self.cursor_icon, (self.cursor_rect.x, self.cursor_rect.y))

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h
        self.highscoresx, self.highscoresy = self.mid_w, self.mid_h
        self.creditsx, self.creditsy = self.mid_w, self.mid_h
        self.quitx, self.quity = self.mid_w, self.mid_h
        self.cursor_rect.midtop = (self.cursor_rect.x, self.cursor_rect.y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('HY452 Snake Game', 40, self.mid_w + self.x_offset - 20, self.mid_h - 390, self.game.WHITE)
            self.game.draw_text('Main Menu', 60, self.mid_w + self.x_offset, self.mid_h - 220, self.game.WHITE)
            if self.game.game_over:
                self.game.draw_text("Start Game", 90, self.startx + self.x_offset, self.starty-100, self.game.WHITE)
            else:
                self.game.draw_text("Resume", 90, self.startx + self.x_offset, self.starty-100, self.game.WHITE)
            self.game.draw_text("Highscores", 90, self.highscoresx + self.x_offset, self.highscoresy, self.game.WHITE)
            self.game.draw_text("Credits", 90, self.creditsx + self.x_offset, self.creditsy+100, self.game.WHITE)
            self.game.draw_text("Quit", 90, self.quitx + self.x_offset, self.quity+200, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.highscoresx + self.cur_offset + self.x_offset, self.highscoresy+20)
                self.state = 'Highscores'
            elif self.state == 'Highscores':
                self.cursor_rect.midtop = (self.creditsx + self.cur_offset + self.x_offset, self.creditsy+120)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.cur_offset + self.x_offset, self.quity+220)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.cur_offset + self.x_offset, self.starty-80)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.cur_offset + self.x_offset, self.quity+220)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.cur_offset + self.x_offset, self.creditsy+120)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.highscoresx + self.cur_offset + self.x_offset, self.highscoresy+20)
                self.state = 'Highscores'
            elif self.state == 'Highscores':
                self.cursor_rect.midtop = (self.startx + self.cur_offset + self.x_offset, self.starty-80)
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