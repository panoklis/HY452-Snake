import pygame
from pygame.locals import *
from menu import *
from enum import Enum
import time
import random
from server import ScoreServer
import yaml


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game():
    def __init__(self):
        pygame.init()

        configs = yaml.safe_load(open('../config.yaml'))
        
        self.DISPLAY_W, self.DISPLAY_H = 600, 800
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        pygame.display.set_caption('HY452 Snake')

        #setup a rectangle for "Play Again" Option
        self.again_rect = Rect(self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2, 160, 50)

        #define game variables
        self.cell_size = 10
        self.game_speed = 5
        self.update_snake = time.time()
        self.food = [0, 0]
        self.new_food = True
        self.new_piece = [0, 0]
        self.game_over = True
        self.pause = False
        self.clicked = False
        self.score = 0
        self.highscore = 0
        self.post_interval = 5
        self.gameover_interval = 2
        self.server_url = configs['server_url']
        self.player_name = configs['player_name']
        self.password = configs['password']
        self.server = ScoreServer(self.server_url)

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ENTER_KEY, self.BACK_KEY, self.PAUSE_KEY, self.W_KEY, self.A_KEY, self.S_KEY, self.D_KEY, self.M_KEY = False, False, False, False, False, False, False, False, False, False, False, False
        #load font from ttf
        self.font_name = '../assets/fonts/Super Moods.ttf'
        self.def_font = pygame.font.Font(self.font_name, 20)    

        #define snake variables
        self.snake_pos = [[int(self.DISPLAY_W / 2), int(self.DISPLAY_H / 2)]]
        self.snake_pos.append([int(self.DISPLAY_W / 2), int(self.DISPLAY_H / 2) + self.cell_size])
        self.snake_pos.append([int(self.DISPLAY_W / 2), int(self.DISPLAY_H / 2) + self.cell_size * 2])
        self.snake_pos.append([int(self.DISPLAY_W / 2), int(self.DISPLAY_H / 2) + self.cell_size * 3])
        self.direction = Direction.UP #1 is up, 2 is down, 3 is left, 4 is right

        #define colors
        self.BG = (255, 200, 150)
        self.BODY_INNER = (255, 255, 0)
        self.BODY_OUTER = (0, 0, 0)
        self.FOOD_COL = (0, 250, 50)
        self.HEAD_COL = (255, 140, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        #text/outline colors
        self.LIGHT_YELLOW = pygame.Color(255, 255, 102)
        self.DARK_BROWN = pygame.Color(102, 51, 0)

        self.BRIGHT_ORANGE = pygame.Color(255, 153, 51)
        self.DEEP_FOREST_GREEN = pygame.Color(0, 102, 0)

        self.SKY_BLUE = pygame.Color(135, 206, 250)
        self.DARK_BLUE = pygame.Color(0, 0, 139)

        self.PASTEL_PINK = pygame.Color(255, 182, 193)
        self.DARK_PURPLE = pygame.Color(102, 0, 102)

        self.BRIGHT_RED = pygame.Color(255, 69, 0)
        self.BLACK = pygame.Color(0, 0, 0)
        
        #initialize menu objects
        self.main_menu = MainMenu(self)
        self.highscores = HighScores(self)
        self.settings = Settings(self)
        self.customize = Customize(self)
        self.custom_background = CustomBackground(self)
        self.custom_soundtrack = CustomSoundtrack(self)
        self.register = Register(self)
        self.login = Login(self)
        self.user_profile = UserProfile(self)
        self.curr_menu = self.main_menu

        # Load background music
        pygame.mixer.music.load("../assets/sounds/background_music.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play the music (-1 means loop indefinitely)
        self.music_playing = True

        #Load background image
        self.background_image = pygame.image.load('../assets/images/backgrounds/background_image.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.background_override = False

        #Animated background
        self.animated_background = False
        self.animation_frames = []
        self.animation_frame = 0
        self.animation_total_frames = 0

        print("Game Initialized")

    def draw_background(self,background_image):
        self.display.blit(background_image, (0, 0))

    def draw_screen(self):
        self.display.fill(self.BG)

    def draw_score(self):
        score_txt = 'Score: ' + str(self.score)
        score_img = self.def_font.render(score_txt, True, self.BLUE)
        self.display.blit(score_img, (2, 2))

    def check_game_over(self):
        #first check is to see if the snake has eaten itself by checking if the head has clashed with the rest of the body
        head_count = 0
        for x in self.snake_pos:
            if self.snake_pos[0] == x and head_count > 0:
                self.game_over = True
            head_count += 1


        #second check is to see if the snake has gone out of bounds
        if self.snake_pos[0][0] < 0 or self.snake_pos[0][0] > self.DISPLAY_W or self.snake_pos[0][1] < 0 or self.snake_pos[0][1] > self.DISPLAY_H:
            self.game_over = True   

        return self.game_over


    def draw_game_over(self):
        over_text = "Game Over!"
        score_text = "Score: " + str(self.score)
        self.draw_text(over_text, 60, self.DISPLAY_W // 2 - 160, self.DISPLAY_H // 2 - 60, self.BLUE)
        self.draw_text(score_text, 80, self.DISPLAY_W // 2 - 160, self.DISPLAY_H // 2 - 10, self.BLUE)

    def game_loop(self):
        if not self.playing:
            return
        last_move_final = True
        current_time = time.time()
        score_changed = False

        #Draw the game screen

        #background_image = pygame.image.load(self.server.get_background())
        #background_image = pygame.transform.scale(background_image, (self.DISPLAY_W, self.DISPLAY_H))
        
        self.game_over = False
        self.pause = False

        anim_time = time.time()

        while self.playing:
            if self.animated_background and time.time() - anim_time > 0.1:
                anim_time = time.time()
                self.animation_frame = (self.animation_frame + 1) % self.animation_total_frames
                self.background_image = self.animation_frames[self.animation_frame]
            self.draw_background(self.background_image)
            if time.time() - current_time > self.post_interval and score_changed:
                current_time = time.time()
                score_changed = False
                self.server.post_score(self.score, self.player_name)
                
            if score_changed:
                if self.score > self.highscore:
                    self.highscore = self.score
                score_changed = False
            self.check_events()
            if not self.playing:
                break
            
            if (self.UP_KEY or self.W_KEY) and self.direction != Direction.DOWN:
                if last_move_final:
                    self.direction = Direction.UP
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.UP_KEY = True
                    self.W_KEY = True
            if (self.RIGHT_KEY or self.D_KEY) and self.direction != Direction.LEFT:
                if last_move_final:
                    self.direction = Direction.RIGHT
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.RIGHT_KEY = True
                    self.D_KEY = True
            if (self.DOWN_KEY or self.S_KEY) and self.direction != Direction.UP:
                if last_move_final:
                    self.direction = Direction.DOWN
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.DOWN_KEY = True
                    self.S_KEY = True
            if (self.LEFT_KEY or self.A_KEY) and self.direction != Direction.RIGHT:
                if last_move_final:
                    self.direction  = Direction.LEFT
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.LEFT_KEY = True
                    self.A_KEY = True
            if self.ENTER_KEY:
                #pass
                self.ENTER_KEY = False
            if self.BACK_KEY:
                #pass
                self.BACK_KEY = False
            if self.PAUSE_KEY:
                self.pause = not self.pause
                self.PAUSE_KEY = False
                    
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                speed = self.game_speed * 5
            else:
                speed = self.game_speed
            
            #create food
            if self.new_food == True:
                self.new_food = False
                self.food[0] = self.cell_size * random.randint(0, int(self.DISPLAY_W / self.cell_size) - 1)
                self.food[1] = self.cell_size * random.randint(0, int(self.DISPLAY_H / self.cell_size) - 1)

            #draw food
            pygame.draw.rect(self.display, self.BLUE, (self.food[0], self.food[1], self.cell_size, self.cell_size))


            #check if food has been eaten
            if self.snake_pos[0] == self.food:
                self.new_food = True
                #create a new piece at the last point of the snake's tail
                self.new_piece = list(self.snake_pos[-1])
                #add an extra piece to the snake
                if self.direction == Direction.UP:
                    self.new_piece[1] += self.cell_size
                #heading down
                if self.direction == Direction.DOWN:
                    self.new_piece[1] -= self.cell_size
                #heading right
                if self.direction == Direction.RIGHT:
                    self.new_piece[0] -= self.cell_size
                #heading left
                if self.direction == Direction.LEFT:
                    self.new_piece[0] += self.cell_size

                #attach new piece to the end of the snake
                self.snake_pos.append(self.new_piece)

                #increase score
                self.score += 1
                score_changed = True


            if self.game_over == False and self.pause == False:
                #update snake
                if time.time() - self.update_snake > 0.5 / speed:
                    self.update_snake = time.time()
                    #first shift the positions of each snake piece back.
                    self.snake_pos = self.snake_pos[-1:] + self.snake_pos[:-1]
                    #now update the position of the head based on direction
                    #heading up
                    if self.direction == Direction.UP:
                        self.snake_pos[0][0] = self.snake_pos[1][0]
                        if self.snake_pos[1][1] - self.cell_size < 0:
                            self.snake_pos[0][1] = self.DISPLAY_H - self.cell_size
                        else:
                            self.snake_pos[0][1] = self.snake_pos[1][1] - self.cell_size
                    #heading down
                    if self.direction == Direction.DOWN:
                        self.snake_pos[0][0] = self.snake_pos[1][0]
                        if self.snake_pos[1][1] + self.cell_size >= self.DISPLAY_H:
                            self.snake_pos[0][1] = 0
                        else:
                            self.snake_pos[0][1] = self.snake_pos[1][1] + self.cell_size
                    #heading right
                    if self.direction == Direction.RIGHT:
                        self.snake_pos[0][1] = self.snake_pos[1][1]
                        if self.snake_pos[1][0] + self.cell_size >= self.DISPLAY_W:
                            self.snake_pos[0][0] = 0
                        else:
                            self.snake_pos[0][0] = self.snake_pos[1][0] + self.cell_size
                    #heading left
                    if self.direction == Direction.LEFT:
                        self.snake_pos[0][1] = self.snake_pos[1][1]
                        if self.snake_pos[1][0] - self.cell_size < 0:
                            self.snake_pos[0][0] = self.DISPLAY_W - self.cell_size
                        else:
                            self.snake_pos[0][0] = self.snake_pos[1][0] - self.cell_size
                    self.game_over = self.check_game_over()
                    if self.game_over:
                        endgame_time = time.time()
                    last_move_final = True

            head = 1
            for x in self.snake_pos:
            
                if head == 0:
                    pygame.draw.rect(self.display, self.BODY_OUTER, (x[0], x[1], self.cell_size, self.cell_size))
                    pygame.draw.rect(self.display, self.BODY_INNER, (x[0] + 1, x[1] + 1, self.cell_size - 2, self.cell_size - 2))
                if head == 1:
                    pygame.draw.rect(self.display, self.BODY_OUTER, (x[0], x[1], self.cell_size, self.cell_size))
                    pygame.draw.rect(self.display, self.RED, (x[0] + 1, x[1] + 1, self.cell_size - 2, self.cell_size - 2))
                    head = 0

            self.draw_score()

            #Endgame/Pausegame logic

            if self.game_over == True:
                self.draw_game_over()
                #print(f'endgame_time: {endgame_time} current_time: {time.time()}')
                if time.time() - endgame_time > self.gameover_interval:
                    #reset game variables
                    print("Game Over")
                    self.server.post_score(self.score, self.player_name)
                    self.reset_game()
                    self.playing = False

            if self.pause:
                self.playing = False
                #self.draw_text('Paused', 40, self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2 - 60, self.BLUE)
                #self.draw_text('Press P to unpause', 20, self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2 - 20, self.BLUE)


            self.window.blit(self.display, (0, 0))
            pygame.display.update()

    def reset_game(self):
        self.game_over = True
        self.pause = False
        self.update_snake = 1
        self.food = [0, 0]
        self.new_food = True
        self.new_piece = [0, 0]
        #define snake variables
        self.snake_pos = [[int(self.DISPLAY_W / 2), int(self.DISPLAY_H / 2)]]
        self.snake_pos.append([300,310])
        self.snake_pos.append([300,320])
        self.snake_pos.append([300,330])
        self.direction = Direction.UP
        self.score = 0

    def check_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                #self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    self.PAUSE_KEY = True
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.ENTER_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_w:
                    self.W_KEY = True
                if event.key == pygame.K_a:
                    self.A_KEY = True
                if event.key == pygame.K_s:
                    self.S_KEY = True
                if event.key == pygame.K_d:
                    self.D_KEY = True
                if event.key == pygame.K_m:
                    self.M_KEY = True
            events.append(event)
        return events

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ENTER_KEY, self.BACK_KEY, self.PAUSE_KEY, self.W_KEY, self.A_KEY, self.S_KEY, self.D_KEY, self.M_KEY = False, False, False, False, False, False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_text_outline(self, text, size, x, y, color, outline_color, offset):
        font = pygame.font.Font(self.font_name, size)
        #Outline
        text_surface = font.render(text, True, outline_color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x-offset, y)
        self.display.blit(text_surface, text_rect)
        text_rect.topleft = (x+offset, y)
        self.display.blit(text_surface, text_rect)
        text_rect.topleft = (x, y-offset)
        self.display.blit(text_surface, text_rect)
        text_rect.topleft = (x, y+offset)
        self.display.blit(text_surface, text_rect)
        
        text_rect.topleft = (x-offset, y-offset)
        self.display.blit(text_surface, text_rect)
        text_rect.topleft = (x-offset, y+offset)
        self.display.blit(text_surface, text_rect)
        text_rect.topleft = (x+offset, y-offset)
        self.display.blit(text_surface, text_rect)
        text_rect.topleft = (x+offset, y+offset)
        self.display.blit(text_surface, text_rect)

        #Text
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.display.blit(text_surface, text_rect)



