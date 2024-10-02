import pygame
from server import *
import time
import threading
from PIL import Image

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cur_offset = - 40
        self.x_offset = -240
        self.cursor_rect = pygame.Rect(self.mid_w + self.cur_offset + self.x_offset, self.mid_h-70, 20, 20)
        self.cursor_icon = pygame.image.load('../assets/images/icons/snake-icon-transparent-hardline-pink-purple.png').convert_alpha()
        self.cursor_icon = pygame.transform.scale(self.cursor_icon, (40, 40))

        #Text colors
        #self.text_col = self.game.WHITE
        #self.outline_col = self.game.BLACK

        #self.text_col = self.game.LIGHT_YELLOW
        #self.outline_col = self.game.DARK_BROWN

        #self.text_col = self.game.BRIGHT_ORANGE
        #self.outline_col = self.game.DEEP_FOREST_GREEN

        #self.text_col = self.game.SKY_BLUE
        #self.outline_col = self.game.DARK_BLUE

        self.text_col = self.game.PASTEL_PINK
        self.outline_col = self.game.DARK_PURPLE

        #self.text_col = self.game.BRIGHT_RED
        #self.outline_col = self.game.BLACK

    def draw_cursor(self):
        #self.game.draw_text('=>', 25, self.cursor_rect.x, self.cursor_rect.y, self.game.WHITE)
        self.game.display.blit(self.cursor_icon, (self.cursor_rect.x, self.cursor_rect.y))

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def popup_servererror(self):
        #draw rect in display
        pygame.draw.rect(self.game.display, self.game.BLACK, pygame.Rect(146, 296, 308, 208))
        pygame.draw.rect(self.game.display, self.game.RED, pygame.Rect(150, 300, 300, 200))
        pygame.draw.rect(self.game.display, self.game.DARK_BLUE, pygame.Rect(263, 410, 60, 50))
        self.game.draw_text_outline('Server Error', 40, 170, 320, self.game.WHITE, self.game.BLACK, 2)
        self.game.draw_text_outline('OK', 40, 270, 420, self.game.WHITE, self.game.BLACK, 2)

    def popup_serversuccess(self):
        #draw rect in display
        pygame.draw.rect(self.game.display, self.game.BLACK, pygame.Rect(146, 296, 308, 208))
        pygame.draw.rect(self.game.display, self.game.GREEN, pygame.Rect(150, 300, 300, 200))
        pygame.draw.rect(self.game.display, self.game.DARK_BLUE, pygame.Rect(263, 410, 60, 50))
        self.game.draw_text_outline('Success', 40, 225, 320, self.game.WHITE, self.game.BLACK, 2)
        self.game.draw_text_outline('OK', 40, 270, 420, self.game.WHITE, self.game.BLACK, 2)

    # Animated background tricks
    def load_gif_frames(self,filename):
        #import frames from gif
        gif = Image.open(filename)
        frames = []
        base_frame = gif.convert('RGBA')

        try:
            while True:
                # Composite the current frame on top of the base frame
                current_frame = gif.convert('RGBA')
                base_frame.paste(current_frame, (0, 0), current_frame)

                # Save a copy of the current composited frame
                frames.append(base_frame.copy())

                # Move to the next frame
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass  # End of GIF

        #Convert frames to pygame images
        frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode) for frame in frames]
        return frames
    
    def check_universal(self):
        if self.game.M_KEY:
            if self.game.music_playing:
                self.game.music_playing = False
                pygame.mixer.music.pause()
            else:
                self.game.music_playing = True
                pygame.mixer.music.unpause()

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
        self.bg_frames = self.load_gif_frames('../assets/images/backgrounds/cabin_forest_background_600_800.gif')
        self.bg_frames_len = len(self.bg_frames)
        self.frame_index = 0
        #Scale animation frames here
        #for i in range(self.bg_frames_len):
        #    self.bg_frames[i] = pygame.transform.scale(self.bg_frames[i], (self.game.DISPLAY_H, self.game.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        last_anim_time = time.time()
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            
            #self.game.display.fill(self.game.BLACK)
            #Animated background tricks
            if time.time() - last_anim_time > 0.02:
                last_anim_time = time.time()
                self.frame_index = (self.frame_index + 1) % self.bg_frames_len
                #Set animation frame position here
                self.game.display.blit(self.bg_frames[self.frame_index], (0, 0))

            self.game.draw_text_outline('HY452 Snake Game', 40, self.mid_w + self.x_offset - 20, self.mid_h - 390, self.text_col, self.outline_col, 2)
            self.game.draw_text_outline('Main Menu', 60, self.mid_w + self.x_offset, self.mid_h - 220, self.text_col, self.outline_col, 2)
            if self.game.game_over:
                self.game.draw_text_outline("Start Game", 90, self.startx + self.x_offset, self.starty-100, self.text_col, self.outline_col, 2)
            else:
                self.game.draw_text_outline("Resume", 90, self.startx + self.x_offset, self.starty-100, self.text_col, self.outline_col, 2)
            self.game.draw_text_outline("Highscores", 90, self.highscoresx + self.x_offset, self.highscoresy, self.text_col, self.outline_col, 2)
            self.game.draw_text_outline("Settings", 90, self.settingsx + self.x_offset, self.settingsy+100, self.text_col, self.outline_col, 2)
            self.game.draw_text_outline("Quit", 90, self.quitx + self.x_offset, self.quity+200, self.text_col, self.outline_col, 2)
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
        self.check_universal()
        self.move_cursor()
        if self.game.ENTER_KEY or self.game.RIGHT_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Highscores':
                self.game.curr_menu = self.game.highscores
            elif self.state == 'Settings':
                self.game.curr_menu = self.game.settings
            elif self.state == 'Quit':
                self.game.running = False
            self.run_display = False


            
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
                self.page_symbol = '<< >>'
            elif self.page == 1 and self.page < self.total_pages:
                self.page_symbol = '   >>'
            elif self.page > 1 and self.page == self.total_pages:
                self.page_symbol = '<<   '
            else:
                self.page_symbol = '     '
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Leaderboard (last: ' + time.strftime('%H:%M:%S', time.localtime(self.leaderboard_get_time)) + ')   ' + self.page_symbol, 30, 20, 10, self.game.WHITE)
            self.game.draw_text('Position', 20, 20, 50, self.game.WHITE)
            self.game.draw_text('Player', 20, 170, 50, self.game.WHITE)
            self.game.draw_text('Score', 20, 380, 50, self.game.WHITE)
            y_offset = 85
            position = 1
            for name, score in sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True):
                #print(f'{position} :: User: {name} Score: {score}')
                if position >= (self.page - 1) * self.page_size + 1 and position <= self.page * self.page_size:
                    if name == self.game.player_name:
                        self.game.draw_text(f'{position}', 20, 20, y_offset, self.game.RED)
                        self.game.draw_text(f'{name}', 20, 170, y_offset, self.game.RED)
                        self.game.draw_text(f'{score}', 20, 380, y_offset, self.game.RED)
                    else:
                        self.game.draw_text(f'{position}', 20, 20, y_offset, self.game.WHITE)
                        self.game.draw_text(f'{name}', 20, 170, y_offset, self.game.WHITE)
                        self.game.draw_text(f'{score}', 20, 380, y_offset, self.game.WHITE)
                    y_offset += 30
                position += 1
            
            self.blit_screen()

    def check_input(self):
        self.check_universal()
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

class Settings(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Customize" #first option
        self.labelx, self.labely = 185, 115
        self.startx, self.starty = 225, 275
        self.y_offset = 50
        self.cur_x_offset = - 60
        self.cursor_rect = pygame.Rect(self.startx + self.cur_x_offset, self.starty, 40, 40)
        self.cursor_icon = pygame.image.load('../assets/images/icons/snake-icon-transparent-hardline-yellow-brown.png').convert_alpha()
        self.cursor_icon = pygame.transform.scale(self.cursor_icon, (40, 40))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            self.game.display.fill(self.game.DARK_BLUE)
            self.game.draw_text_outline('Settings', 60, self.labelx, self.labely, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.game.draw_text_outline('Customize', 40, self.startx, self.starty, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.game.draw_text_outline('Server', 40, self.startx, self.starty + self.y_offset, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.game.draw_text_outline('User Profile', 40, self.startx, self.starty + self.y_offset*2, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.game.draw_text_outline('Register', 40, self.startx, self.starty + self.y_offset*3, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.game.draw_text_outline('Login', 40, self.startx, self.starty + self.y_offset*4, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.draw_cursor()
            self.blit_screen()

    def draw_cursor(self):
        self.game.display.blit(self.cursor_icon, (self.cursor_rect.x, self.cursor_rect.y))

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Customize':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y + self.y_offset)
                self.state = 'Server'
            elif self.state == 'Server':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y + self.y_offset)
                self.state = 'User Profile'
            elif self.state == 'User Profile':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y + self.y_offset)
                self.state = 'Register'
            elif self.state == 'Register':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y + self.y_offset)
                self.state = 'Login'
            elif self.state == 'Login':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)
                self.state = 'Customize'
        elif self.game.UP_KEY:
            if self.state == 'Customize':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y + self.y_offset*4)
                self.state = 'Login'
            elif self.state == 'Login':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y - self.y_offset)
                self.state = 'Register'
            elif self.state == 'Register':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y - self.y_offset)
                self.state = 'User Profile'
            elif self.state == 'User Profile':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.cursor_rect.y - self.y_offset)
                self.state = 'Server'
            elif self.state == 'Server':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)
                self.state = 'Customize'

    def check_input(self):
        self.check_universal()
        self.move_cursor()
        if self.game.BACK_KEY or self.game.LEFT_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.ENTER_KEY or self.game.RIGHT_KEY:
            if self.state == 'Customize':
                self.game.curr_menu = self.game.customize
                self.run_display = False
            elif self.state == 'Server':
                #self.game.curr_menu = self.game.server_menu
                pass
            elif self.state == 'User Profile':
                #self.game.curr_menu = self.game.user_profile
                pass
            elif self.state == 'Register':
                #self.game.curr_menu = self.game.register
                pass

class Customize(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Custom Soundtrack" #first option
        self.labelx, self.labely = 160, 125
        self.startx, self.starty = 160, 300
        self.y_offset = 50
        self.cur_x_offset = - 60
        self.cursor_rect = pygame.Rect(self.startx + self.cur_x_offset, self.starty, 40, 40)
        self.cursor_icon = pygame.image.load('../assets/images/icons/snake-icon-transparent-hardline-yellow-brown.png').convert_alpha()
        self.cursor_icon = pygame.transform.scale(self.cursor_icon, (40, 40))

        self.server_success = False
        self.server_error = False

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            self.game.display.fill(self.game.DARK_BLUE)
            #Debugging
            #self.game.draw_text_outline('label   x,y: ' + str(self.labelx) + ',' + str(self.labely), 20, 0, 0, self.game.WHITE, self.game.BLACK, 1)
            #self.game.draw_text_outline('options x,y: ' + str(self.startx) + ',' + str(self.starty), 20, 0,20, self.game.WHITE, self.game.BLACK, 1)
            self.game.draw_text_outline('Customize', 60, self.labelx, self.labely, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.game.draw_text_outline('Custom Soundtrack', 40, self.startx, self.starty, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.game.draw_text_outline('Custom Background', 40, self.startx, self.starty + self.y_offset, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            self.draw_cursor()
            self.blit_screen()

    
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Custom Soundtrack':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty + self.y_offset)
                self.state = 'Custom Background'
            elif self.state == 'Custom Background':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)
                self.state = 'Custom Soundtrack'
        elif self.game.UP_KEY:
            if self.state == 'Custom Soundtrack':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty + self.y_offset)
                self.state = 'Custom Background'
            elif self.state == 'Custom Background':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)
                self.state = 'Custom Soundtrack'
    
    def draw_cursor(self):
        self.game.display.blit(self.cursor_icon, (self.cursor_rect.x, self.cursor_rect.y))

    def check_input(self):
        self.check_universal()
        self.move_cursor()
        if self.game.BACK_KEY or self.game.LEFT_KEY:
            self.game.curr_menu = self.game.settings
            self.run_display = False
        if self.game.ENTER_KEY or self.game.RIGHT_KEY:
            if self.state == 'Custom Soundtrack':
                #self.game.curr_menu = self.game.custom_soundtrack
                #self.run_display = False
                pass
            elif self.state == 'Custom Background':
                self.game.curr_menu = self.game.custom_background
                self.run_display = False
        #Debugging
        #if self.game.W_KEY:
        #    if self.state == 'Custom Soundtrack':
        #        self.labely -= 5
        #    if self.state == 'Custom Background':
        #        self.starty -= 5
        #if self.game.S_KEY:
        #    if self.state == 'Custom Soundtrack':
        #        self.labely += 5
        #    if self.state == 'Custom Background':
        #        self.starty += 5
        #if self.game.A_KEY:
        #    if self.state == 'Custom Soundtrack':
        #        self.labelx -= 5
        #    if self.state == 'Custom Background':
        #        self.startx -= 5
        #if self.game.D_KEY:
        #    if self.state == 'Custom Soundtrack':
        #        self.labelx += 5
        #    if self.state == 'Custom Background':
        #        self.startx += 5

class CustomBackground(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 0 #first option
        self.startx, self.starty = 70, 110
        self.y_offset = 50
        self.cur_x_offset = - 50
        self.labelx, self.labely = 20, 40
        self.cursor_rect = pygame.Rect(self.startx + self.cur_x_offset, self.starty, 40, 40)
        self.cursor_icon = pygame.image.load('../assets/images/icons/snake-icon-transparent-hardline-yellow-brown.png').convert_alpha()
        self.cursor_icon = pygame.transform.scale(self.cursor_icon, (40, 40))

        self.server_success = False
        self.server_error = False

        self.got_backgrounds = True
        self.page = 1
        self.page_size = 14

        self.backgrounds = self.game.server.get_backgrounds()
        self.total_entries = len(self.backgrounds)
        self.total_pages = (self.total_entries -1) // self.page_size + 1
        self.page_symbol = ''

    def display_menu(self):
        self.got_backgrounds = False
        self.run_display = True
        self.update_backgrounds()
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            if (not self.server_success) and (not self.server_error):
                self.check_input()
            elif self.server_success and self.game.ENTER_KEY:
                self.server_success = False
                self.run_display = False
            elif self.server_error and self.game.ENTER_KEY:
                self.server_error = False
            self.game.display.fill(self.game.DARK_BLUE)
            pygame.draw.line(self.game.display, self.game.LIGHT_YELLOW, (20, 90), (580, 90), 3)
            if self.got_backgrounds:
                self.draw_cursor()
                if self.page > 1 and self.page < self.total_pages:
                    self.page_symbol = '<< >>'
                elif self.page == 1 and self.page < self.total_pages:
                    self.page_symbol = '   >>'
                elif self.page > 1 and self.page == self.total_pages:
                    self.page_symbol = '<<   '
                else:
                    self.page_symbol = ''
                self.game.draw_text_outline('Server Backgrounds' + '    ' + self.page_symbol, 40, self.labelx, self.labely, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
                #print backgrounds from server
                i = 0
                for bg in self.backgrounds:
                    if i >= (self.page - 1) * self.page_size and i < self.page * self.page_size:
                        if i == self.state % self.page_size:
                            self.game.draw_text_outline(bg, 30, self.startx, self.starty + self.y_offset * (i % self.page_size), self.game.RED, self.game.DARK_BROWN, 2)
                        else:
                            self.game.draw_text_outline(bg, 30, self.startx, self.starty + self.y_offset * (i % self.page_size), self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
                    i += 1
            else:
                self.game.draw_text_outline('Getting Backgrounds from server...', 30, self.labelx, self.labely+10, self.game.LIGHT_YELLOW, self.game.DARK_BROWN, 2)
            if self.server_success:
                self.popup_serversuccess()
            if self.server_error:
                self.popup_servererror()
            self.blit_screen()

    
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state >= (self.page - 1) * self.page_size and self.state < (self.page_size * self.page) - 1 and self.state < self.total_entries - 1:
                self.state += 1
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty + self.y_offset * (self.state % self.page_size))
        elif self.game.UP_KEY:
            if self.state > (self.page - 1) * self.page_size and self.state <= (self.page_size * self.page) - 1:
                self.state -= 1
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty + self.y_offset * (self.state % self.page_size))
    
    def draw_cursor(self):
        self.game.display.blit(self.cursor_icon, (self.cursor_rect.x, self.cursor_rect.y))

    def check_input(self):
        self.check_universal()
        self.move_cursor()
        if self.game.BACK_KEY or self.game.LEFT_KEY:
            self.game.curr_menu = self.game.customize
            self.run_display = False
        if self.game.ENTER_KEY:
            i = 0
            for bg in self.backgrounds:
                if i == self.state: 
                    # bg is of the form 'backgrounds/your-background.gif'
                    # we need to remove the 'backgrounds/' part
                    bg = bg.split('/')[1]
                    background = self.game.server.get_background(bg)
                    if self.game.server.last_request_status == False:
                        self.server_error = True
                        break
                    #find out if image is gif or not
                    if bg[-3:] == 'gif':
                        #load gif frames
                        frames = self.load_gif_frames(background)
                        self.game.animated_background = True
                        self.game.animation_frames = frames
                        self.game.animation_total_frames = len(frames)
                        for i in range(self.game.animation_total_frames):
                            self.game.animation_frames[i] = pygame.transform.scale(self.game.animation_frames[i], (self.game.DISPLAY_W, self.game.DISPLAY_H))
                    else:
                        self.game.animated_background = False
                        self.game.background_image = pygame.image.load(background).convert_alpha()
                        self.game.background_image = pygame.transform.scale(self.game.background_image, (self.game.DISPLAY_W, self.game.DISPLAY_H))

                    self.game.background_override = True
                    self.game.curr_menu = self.game.main_menu
                    #self.run_display = False
                    self.server_success = True
                    break
                i += 1
        if self.game.RIGHT_KEY:
            if self.page < self.total_pages:
                self.page += 1
                self.state = (self.page - 1) * self.page_size
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)
        if self.game.LEFT_KEY:
            if self.page > 1:
                self.page -= 1
                self.state = (self.page - 1) * self.page_size
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)

    def update_backgrounds(self):
        thread = threading.Thread(target=self._update_backgrounds_thread)
        thread.start()
    def _update_backgrounds_thread(self):
        self.backgrounds = self.game.server.get_backgrounds()
        if self.game.server.last_request_status == False:
            self.server_error = True
            return
        self.total_entries = len(self.backgrounds)
        self.total_pages = (self.total_entries -1) // self.page_size + 1
        self.got_backgrounds = True
        print(self.backgrounds)
""" 

class Submenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Customize" #first option
        self.startx, self.starty = 200, 200
        self.y_offset = 80
        self.cur_x_offset = - 60
        self.cursor_rect = pygame.Rect(self.startx + self.cur_x_offset, self.starty, 40, 40)
        self.cursor_icon = pygame.image.load('../assets/images/icons/snake-icon-transparent-hardline-yellow-brown.png').convert_alpha()
        self.cursor_icon = pygame.transform.scale(self.cursor_icon, (40, 40))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.running == False:
                return
            self.check_input()
            #visual representation of submenu
            self.draw_cursor()
            self.blit_screen()

    
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Top Option':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty + self.y_offset)
                self.state = 'Bottom Option'
            elif self.state == 'Bottom Option':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)
                self.state = 'Top Option'
        elif self.game.UP_KEY:
            if self.state == 'Top Option':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty + self.y_offset)
                self.state = 'Bottom Option'
            elif self.state == 'Bottom Option':
                self.cursor_rect.topleft = (self.startx + self.cur_x_offset, self.starty)
                self.state = 'Top Option'
    
    def draw_cursor(self):
        self.game.display.blit(self.cursor_icon, (self.cursor_rect.x, self.cursor_rect.y))

    def check_input(self):
        self.check_universal()
        self.move_cursor()
        if self.game.BACK_KEY
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.ENTER_KEY:
            self.game.curr_menu = self.game.whatevermenu
            self.run_display = False
        if self.game.LEFT_KEY:
            pass
            #Do some left key stuff
        if self.game.RIGHT_KEY:
            pass
            #Do some right key stuff
        if self.game.UP_KEY:
            pass
            #Do some up key stuff
            #Change state to lower menu option
        if self.game.DOWN_KEY:
            pass
            #Do some down key stuff
            #Change state to higher menu option

"""
