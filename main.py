import time
import random
import pygame
from pygame import key
from pygame.constants import BLEND_ALPHA_SDL2, K_DOWN, K_RIGHT, K_UP, K_LEFT
from pygame.font import SysFont

# Color variables
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
# display
disp_width = 800
disp_height = 600
font_size = 30
# Snake
snake_block = 20
snake_speed = 15 
# food
food_block = 20
# pygame
clock = pygame.time.Clock()

def disp_score(score, disp, font_style):
    value = font_style.render("Score: " + str(score), True, black)
    disp.blit(value, [0, 0])

def message(msg, color, font_style, disp):
    mesg = font_style.render(msg, True, color)
    disp.blit(mesg, [disp_width / 6, disp_height / 3])

def our_snake(snake_block, snake_list, disp):
    for x in snake_list:
        pygame.draw.rect(disp, black, [x[0], x[1], snake_block, snake_block])

def main():
    pygame.init()

    disp = pygame.display.set_mode(([disp_width, disp_height]))
    pygame.display.set_caption("Snake game")

    x1 = disp_width / 2
    y1 = disp_height / 2
    x1_change = 0
    y1_change = 0
    food_x = round(random.randrange(0, disp_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, disp_height- snake_block) / 10.0) * 10.0

    font_style = pygame.font.SysFont(None, font_size)
    font_style_score = pygame.font.SysFont(None, font_size)

    snake_list = []
    Length_of_snake = 1

    game_over = False
    game_close = False
    while not game_over:
        while game_close == True:
            disp.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", black, font_style, disp)
            disp_score(Length_of_snake - 1, disp, font_style_score)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif key == pygame.K_RIGHT:
                    x1_change = snake_block 
                    y1_change = 0
                elif key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block 
        
        if x1 >= disp_width or x1 < 0 or y1 >= disp_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        disp.fill(white)
        pygame.draw.rect(disp, blue, [food_x, food_y, food_block, food_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)
        if len(snake_list) > Length_of_snake:
            del snake_list[0]
        
        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True
        our_snake(snake_block, snake_list, disp)
        disp_score(Length_of_snake - 1, disp, font_style_score)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, disp_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, disp_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()


if __name__ == "__main__":
    print("===Start Pygame [Snake Game]===")
    main()
    quit()