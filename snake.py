import pygame
from pygame.locals import *
import random
from enum import Enum
import requests
import base64
import json
import io
import sys

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

pygame.init()

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('HY452 Snake')

#define font
font = pygame.font.SysFont(None, 40)

#setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

#define game variables
cell_size = 10
move_delay = 50
update_snake = 1
food = [0, 0]
new_food = True
new_piece = [0, 0]
game_over = False
clicked = False
score = 0

#define snake variables
snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 2])
snake_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])
direction = Direction.UP #1 is up, 2 is down, 3 is left, 4 is right

#define colors
bg = (255, 200, 150)
body_inner = (255, 255, 0)
body_outer = (0, 0, 0)
food_col = (0, 250, 50)
head_col = (255, 140, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

def draw_background():
    screen.blit(background_image, (0, 0))

def draw_screen():
    screen.fill(bg)

def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0, 0))

def check_game_over(game_over):
    #first check is to see if the snake has eaten itself by checking if the head has clashed with the rest of the body
    head_count = 0
    for x in snake_pos:
        if snake_pos[0] == x and head_count > 0:
            game_over = True
        head_count += 1


    #second check is to see if the snake has gone out of bounds
    if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
        game_over = True   

    return game_over


def draw_game_over():
    over_text = "Game Over!"
    over_img = font.render(over_text, True, blue)
    pygame.draw.rect(screen, red, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))


#Remote background functionality test
# Fetch image from API & add into background
def fetch_image_from_api(image_id):
    api_url = f'https://api-id.execute-api.region.amazonaws.com/your-stage/image?id={image_id}'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        base64_data = response.json()['body']
        image_data = base64.b64decode(base64_data)
        return image_data
    else:
        raise Exception(f"Error fetching image: {response.status_code}")

# Load image from bytes into pygame
def load_image_from_bytes(image_data):
    image_file = BytesIO(image_data)
    return pygame.image.load(image_file)


run = True
last_move_final = True

#Load background image & resize
background_image = pygame.image.load('background_image.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

#Get remote background
#get 1st argument, if exists
if len(sys.argv) > 1:
    remote_bg = int(sys.argv[1])
    try:
        image_data = fetch_image_from_api(remote_bg)
        image = load_image_from_bytes(image_data)
    except Exception as e:
        print(f"Failed to fetch image: {e}")
        pygame.quit()
        quit()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


while run:

    #draw_screen()
    draw_background()
    draw_score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != Direction.DOWN:
                if last_move_final:
                    direction = Direction.UP
                    last_move_final = False
                else:
                    pygame.event.post(event)
            if event.key == pygame.K_RIGHT and direction != Direction.LEFT:
                if last_move_final:
                    direction = Direction.RIGHT
                    last_move_final = False
                else:
                    pygame.event.post(event)
            if event.key == pygame.K_DOWN and direction != Direction.UP:
                if last_move_final:
                    direction = Direction.DOWN
                    last_move_final = False
                else:
                    pygame.event.post(event)
            if event.key == pygame.K_LEFT and direction != Direction.RIGHT:
                if last_move_final:
                    direction  = Direction.LEFT
                    last_move_final = False
                else:
                    pygame.event.post(event)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            delay = move_delay / 5
        else:
            delay = move_delay

    #create food
    if new_food == True:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width / cell_size) - 1)
        food[1] = cell_size * random.randint(0, (screen_height / cell_size) - 1)
    
    #draw food
    pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))


    #check if food has been eaten
    if snake_pos[0] == food:
        new_food = True
        #create a new piece at the last point of the snake's tail
        new_piece = list(snake_pos[-1])
        #add an extra piece to the snake
        if direction == Direction.UP:
            new_piece[1] += cell_size
        #heading down
        if direction == Direction.DOWN:
            new_piece[1] -= cell_size
        #heading right
        if direction == Direction.RIGHT:
            new_piece[0] -= cell_size
        #heading left
        if direction == Direction.LEFT:
            new_piece[0] += cell_size
        
        #attach new piece to the end of the snake
        snake_pos.append(new_piece)

        #increase score
        score += 1



    if game_over == False:
        #update snake
        if update_snake > delay:
            update_snake = 1
            #first shift the positions of each snake piece back.
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            #now update the position of the head based on direction
            #heading up
            if direction == Direction.UP:
                snake_pos[0][0] = snake_pos[1][0]
                if snake_pos[1][1] - cell_size < 0:
                    snake_pos[0][1] = screen_height - cell_size
                else:
                    snake_pos[0][1] = snake_pos[1][1] - cell_size
            #heading down
            if direction == Direction.DOWN:
                snake_pos[0][0] = snake_pos[1][0]
                if snake_pos[1][1] + cell_size >= screen_height:
                    snake_pos[0][1] = 0
                else:
                    snake_pos[0][1] = snake_pos[1][1] + cell_size
            #heading right
            if direction == Direction.RIGHT:
                snake_pos[0][1] = snake_pos[1][1]
                if snake_pos[1][0] + cell_size >= screen_width:
                    snake_pos[0][0] = 0
                else:
                    snake_pos[0][0] = snake_pos[1][0] + cell_size
            #heading left
            if direction == Direction.LEFT:
                snake_pos[0][1] = snake_pos[1][1]
                if snake_pos[1][0] - cell_size < 0:
                    snake_pos[0][0] = screen_width - cell_size
                else:
                    snake_pos[0][0] = snake_pos[1][0] - cell_size
            game_over = check_game_over(game_over)
            last_move_final = True
    



    if game_over == True:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            #reset variables
            game_over = False
            update_snake = 1
            food = [0, 0]
            new_food = True
            new_piece = [0, 0]
            #define snake variables
            snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
            snake_pos.append([300,310])
            snake_pos.append([300,320])
            snake_pos.append([300,330])
            direction = Direction.UP
            score = 0

    head = 1
    for x in snake_pos:

        if head == 0:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, head_col, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

    pygame.display.update()

    update_snake += 1

pygame.quit()