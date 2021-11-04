import time
import random
import pygame
from pygame import key
from pygame.constants import BLEND_ALPHA_SDL2, K_DOWN, K_RIGHT, K_UP, K_LEFT

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
snake_block = 10
snake_speed = 30
# food
food_block = 10
# pygame
clock = pygame.time.Clock()

def message(msg, color, font_style, disp):
    mesg = font_style.render(msg, True, color)
    disp.blit(mesg, [disp_width / 3, disp_height / 3])

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

    game_over = False
    game_close = False
    while not game_over:
        while game_close == True:
            disp.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", black, font_style, disp)
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
                game_over = True
            
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
        pygame.draw.rect(disp, black, [x1, y1, snake_block, snake_block])
        pygame.display.update()
        if x1 == food_x and y1 == food_y:
            print("HITHIT")
        clock.tick(snake_speed)

    pygame.quit()


if __name__ == "__main__":
    print("===Start Pygame [Snake Game]===")
    main()
    quit()