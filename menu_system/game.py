import pygame
from pygame.locals import *
from menu import *
from enum import Enum
import time
import random
from server import ScoreServer


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game():
    def __init__(self):
        pygame.init()
        
        self.DISPLAY_W, self.DISPLAY_H = 600, 800
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        pygame.display.set_caption('HY452 Snake')

        #setup a rectangle for "Play Again" Option
        self.again_rect = Rect(self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2, 160, 50)

        #define game variables
        self.cell_size = 10
        self.move_delay = 50
        self.update_snake = 1
        self.food = [0, 0]
        self.new_food = True
        self.new_piece = [0, 0]
        self.game_over = True
        self.pause = False
        self.clicked = False
        self.score = 0
        self.highscore = 0
        self.post_interval = 5
        self.gameover_interval = 3
        self.server_url = 'https://wl2uxwpe15.execute-api.us-east-1.amazonaws.com/test'
        self.server = ScoreServer(self.server_url)

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ENTER_KEY, self.BACK_KEY, self.PAUSE_KEY = False, False, False, False, False, False, False
        self.font_name = pygame.font.get_default_font()
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
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        self.main_menu = MainMenu(self)
        #self.options = OptionsMenu(self)
        #self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
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
        self.draw_text(over_text, 40, self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2 - 60, self.BLUE)
        self.draw_text(score_text, 40, self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2 - 20, self.BLUE)

    def game_loop(self):
        if not self.playing:
            return
        last_move_final = True
        current_time = time.time()
        score_changed = False

        #Draw the game screen
        background_image = pygame.image.load('background_image.jpg')
        background_image = pygame.transform.scale(background_image, (self.DISPLAY_W, self.DISPLAY_H))

        #background_image = pygame.image.load(self.server.get_background())
        #background_image = pygame.transform.scale(background_image, (self.DISPLAY_W, self.DISPLAY_H))

        self.game_over = False
        self.pause = False

        while self.playing:
            self.draw_background(background_image)
            if time.time() - current_time > self.post_interval and score_changed:
                current_time = time.time()
                score_changed = False
                self.server.post_score('gamiolis', self.score)
                
            if score_changed:
                if self.score > self.highscore:
                    self.highscore = self.score
                score_changed = False
            self.check_events()
            if not self.playing:
                break
            
            if self.UP_KEY and self.direction != Direction.DOWN:
                if last_move_final:
                    self.direction = Direction.UP
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.UP_KEY = True
            if self.RIGHT_KEY and self.direction != Direction.LEFT:
                if last_move_final:
                    self.direction = Direction.RIGHT
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.RIGHT_KEY = True
            if self.DOWN_KEY and self.direction != Direction.UP:
                if last_move_final:
                    self.direction = Direction.DOWN
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.DOWN_KEY = True
            if self.LEFT_KEY and self.direction != Direction.RIGHT:
                if last_move_final:
                    self.direction  = Direction.LEFT
                    self.reset_keys()
                    last_move_final = False
                else:
                    self.reset_keys()
                    self.LEFT_KEY = True
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
                delay = self.move_delay / 5
            else:
                delay = self.move_delay
            
            #create food
            if self.new_food == True:
                self.new_food = False
                self.food[0] = self.cell_size * random.randint(0, int(self.DISPLAY_W / self.cell_size) - 1)
                self.food[1] = self.cell_size * random.randint(0, int(self.DISPLAY_H / self.cell_size) - 1)

            #draw food
            pygame.draw.rect(self.display, self.FOOD_COL, (self.food[0], self.food[1], self.cell_size, self.cell_size))


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
                if self.update_snake > delay:
                    self.update_snake = 1
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
                    pygame.draw.rect(self.display, self.HEAD_COL, (x[0] + 1, x[1] + 1, self.cell_size - 2, self.cell_size - 2))
                    head = 0

            self.draw_score()

            #Endgame/Pausegame logic

            if self.game_over == True:
                self.draw_game_over()
                #print(f'endgame_time: {endgame_time} current_time: {time.time()}')
                if time.time() - endgame_time > self.gameover_interval:
                    #reset game variables
                    print("Game Over")
                    self.reset_game()
                    self.playing = False

            if self.pause:
                self.playing = False
                #self.draw_text('Paused', 40, self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2 - 60, self.BLUE)
                #self.draw_text('Press P to unpause', 20, self.DISPLAY_W // 2 - 80, self.DISPLAY_H // 2 - 20, self.BLUE)


            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.update_snake += 1    

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                #self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    self.PAUSE_KEY = True
                if event.key == pygame.K_RETURN:
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

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ENTER_KEY, self.BACK_KEY, self.PAUSE_KEY = False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.display.blit(text_surface, text_rect)





