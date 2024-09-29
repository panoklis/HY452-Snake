import pygame
from server import *
import time
import threading

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cur_offset = - 40
        self.x_offset = -240
        self.cursor_rect = pygame.Rect(self.mid_w + self.cur_offset + self.x_offset, self.mid_h-70, 20, 20)
        self.cursor_icon = pygame.image.load('snake-icon-transparent-hardline.png').convert_alpha()
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
        self.settingsx, self.settingsy = self.mid_w, self.mid_h
        self.quitx, self.quity = self.mid_w, self.mid_h
        self.cursor_rect.midtop = (self.cursor_rect.x, self.cursor_rect.y)

        #Animated background tricks
        self.bg_frames = self.load_frames('extracted_frames/frame_', 42)
        self.bg_frames_len = len(self.bg_frames)
        self.frame_index = -1
        for i in range(self.bg_frames_len):
            self.bg_frames[i] = pygame.transform.scale(self.bg_frames[i], (self.game.DISPLAY_H, self.game.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        anim_delay = 0
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            
            #self.game.display.fill(self.game.BLACK)
            #Animated background tricks
            if anim_delay == 1:
                anim_delay = 0
                self.frame_index = (self.frame_index + 1) % self.bg_frames_len
            else:
                anim_delay += 1
            self.game.display.blit(self.bg_frames[self.frame_index], (-100, 0))

            self.game.draw_text('HY452 Snake Game', 40, self.mid_w + self.x_offset - 20, self.mid_h - 390, self.game.WHITE)
            self.game.draw_text('Main Menu', 60, self.mid_w + self.x_offset, self.mid_h - 220, self.game.WHITE)
            if self.game.game_over:
                self.game.draw_text("Start Game", 90, self.startx + self.x_offset, self.starty-100, self.game.WHITE)
            else:
                self.game.draw_text("Resume", 90, self.startx + self.x_offset, self.starty-100, self.game.WHITE)
            self.game.draw_text("Highscores", 90, self.highscoresx + self.x_offset, self.highscoresy, self.game.WHITE)
            self.game.draw_text("Settings", 90, self.settingsx + self.x_offset, self.settingsy+100, self.game.WHITE)
            self.game.draw_text("Quit", 90, self.quitx + self.x_offset, self.quity+200, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.highscoresx + self.cur_offset + self.x_offset, self.highscoresy+20)
                self.state = 'Highscores'
            elif self.state == 'Highscores':
                self.cursor_rect.midtop = (self.settingsx + self.cur_offset + self.x_offset, self.settingsy+120)
                self.state = 'Settings'
            elif self.state == 'Settings':
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
                self.cursor_rect.midtop = (self.settingsx + self.cur_offset + self.x_offset, self.settingsy+120)
                self.state = 'Settings'
            elif self.state == 'Settings':
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
                self.game.curr_menu = self.game.highscores
            elif self.state == 'Settings':
                #self.game.curr_menu = self.game.settings
                pass
            elif self.state == 'Quit':
                self.game.running = False
            self.run_display = False
    
    # Animated background tricks
    def load_frames(self,filename, amount):
        frames = []
        for i in range(amount):
                frame_image = pygame.image.load(f'{filename}{i}.png')
                frames.append(frame_image)
        return frames


            
class HighScores(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.leaderboard = self.game.server.get_leaderboard()
        self.leaderboard_get_time = time.time()
        #current leaderboard page
        self.page = 1
        #number of entries per page
        self.page_size = 24
        self.total_entries = len(self.leaderboard)
        self.total_pages = (self.total_entries -1) // self.page_size + 1
        self.interval = 5
        self.page_symbol = '[     ]'


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            if time.time() - self.leaderboard_get_time > self.interval:
                self.update_leaderboard()
                self.leaderboard_get_time = time.time()
            #print leaderboard sorted by score
            if self.page > 1 and self.page < self.total_pages:
                self.page_symbol = '[<< >>]'
            elif self.page == 1 and self.page < self.total_pages:
                self.page_symbol = '[   >>]'
            elif self.page > 1 and self.page == self.total_pages:
                self.page_symbol = '[<<   ]'
            else:
                self.page_symbol = '[     ]'
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Leaderboard (last: ' + time.strftime('%H:%M:%S', time.localtime(self.leaderboard_get_time)) + ')   ' + self.page_symbol, 30, 20, 10, self.game.WHITE)
            self.game.draw_text('Position', 20, 20, 50, self.game.WHITE)
            self.game.draw_text('Player', 20, 150, 50, self.game.WHITE)
            self.game.draw_text('Score', 20, 310, 50, self.game.WHITE)
            y_offset = 85
            position = 1
            for name, score in sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True):
                #print(f'{position} :: User: {name} Score: {score}')
                if position >= (self.page - 1) * self.page_size + 1 and position <= self.page * self.page_size:
                    if name == self.game.player_name:
                        self.game.draw_text(f'{position}', 20, 20, y_offset, self.game.RED)
                        self.game.draw_text(f'{name}', 20, 150, y_offset, self.game.RED)
                        self.game.draw_text(f'{score}', 20, 310, y_offset, self.game.RED)
                    else:
                        self.game.draw_text(f'{position}', 20, 20, y_offset, self.game.WHITE)
                        self.game.draw_text(f'{name}', 20, 150, y_offset, self.game.WHITE)
                        self.game.draw_text(f'{score}', 20, 310, y_offset, self.game.WHITE)
                    y_offset += 30
                position += 1
            
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ENTER_KEY:
            self.game.curr_menu = self.game.main_menu
            self.page = 1
            self.run_display = False
        if self.game.LEFT_KEY and self.page > 1:
            self.page -= 1
        if self.game.RIGHT_KEY and self.page < self.total_pages:
            self.page += 1
    def update_leaderboard(self):
        thread = threading.Thread(target=self._update_leaderboard_thread)
        thread.start()

    def _update_leaderboard_thread(self):
        self.leaderboard = self.game.server.get_leaderboard()
        self.total_entries = len(self.leaderboard)
        self.total_pages = (self.total_entries -1) // self.page_size + 1