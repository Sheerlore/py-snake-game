import random
import pygame

# CONSTANT variable ===========================
# display
DISPLAY_W = 800
DISPLAY_H = 600
BLOCK_SIZE = 40 
BASIC_FONT_SIZE = 40
SCORE_FONT_SIZE = 40
TIMER_FONT_SIZE = 40
# Snake
SNAKE_SPEED = 15
# food
FOOD_BLOCK_SIZE = 40 
# Color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FUNCTION  =====================================
def display_timer(disp, font_style, time, color = BLACK):
    txt = font_style.render("time: " + time, True, color)
    disp.blit(txt, [10, SCORE_FONT_SIZE])

def display_score(disp, font_style, score, color = BLACK):
    value = font_style.render("score: " + str(score), True, color)
    disp.blit(value, [10, 0])

def display_message(disp, font_style, text, position = [0, 0], color = BLACK):
    msg = font_style.render(text, True, color)
    disp.blit(msg, position)

def draw_snake(disp, snake_list,img_head, img,size = BLOCK_SIZE):
    for x in snake_list[:-1]:
        # pygame.draw.rect(disp, BLACK, [x[0], x[1], size, size])
        disp.blit(img, [x[0], x[1]])
    disp.blit(img_head, [snake_list[-1][0], snake_list[-1][1]])

def draw_blood(disp, blood_list,img):
    for x in blood_list:
        disp.blit(img, [x[0], x[1]])

def draw_food_img(disp, img, position = [0, 0]):
    disp.blit(img, position)

def is_hit_snake_and_food(snake_x, snake_y, food_x, food_y, snake_size, food_size):
    if (((food_x <= snake_x) and (snake_x <= (food_x + food_size))) and \
        ((food_y <= snake_y) and (snake_y <= (food_y + food_size)))) or \
        (((food_x <= (snake_x + snake_size)) and ((snake_x + snake_size) <= (food_x + food_size))) and \
        ((food_y <= (snake_y + snake_size)) and ((snake_y + snake_size) <= (food_y + food_size)))) or \
        (((food_x <= snake_x) and (snake_x <= (food_x + food_size))) and \
        ((food_y <= (snake_y + snake_size)) and ((snake_y + snake_size) <= (food_y + food_size)))) or \
        (((food_x <= (snake_x + snake_size)) and ((snake_x + snake_size) <= (food_x + food_size))) and \
        ((food_y <= snake_y) and (snake_y <= (food_y + food_size)))):
        return True
    else:
        return False

def calc_snake_pos_diff_by_key(key, move_amount):
    x1_change = 0
    y1_change = 0
    if key == pygame.K_LEFT: # ←
        x1_change = -move_amount
        y1_change = 0
    elif key == pygame.K_RIGHT: # →
        x1_change = move_amount 
        y1_change = 0
    elif key == pygame.K_UP: # ↑
        x1_change = 0
        y1_change = -move_amount
    elif key == pygame.K_DOWN: # ↓
        x1_change = 0
        y1_change = move_amount 
    return (x1_change, y1_change)


def game_loop():
    # /=========== game init ===============\
    pygame.init()
    disp = pygame.display.set_mode(([DISPLAY_W, DISPLAY_H]))
    pygame.display.set_caption("Snake game Duke VS Gopher")
    # init snake position
    snake_x = DISPLAY_W / 2
    snake_y = DISPLAY_H / 2
    snake_dx = 0
    snake_dy = 0
    # init food position
    food_x = round(random.randrange(0, DISPLAY_W - BLOCK_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, DISPLAY_H - BLOCK_SIZE) / 10.0) * 10.0
    # init font style
    basic_font_style = pygame.font.SysFont(None, BASIC_FONT_SIZE)
    socre_font_style = pygame.font.SysFont(None, SCORE_FONT_SIZE)
    timer_font_style = pygame.font.SysFont(None, TIMER_FONT_SIZE)
    # snake conf 
    snake_list = []
    length_of_snake = 1
    # clock time in pygame
    clock = pygame.time.Clock()
    # blood
    blood_list = []
    # game flag 
    game_over = False
    game_close = False
    close_out_display = False
    close_time_up = False
    close_hurt_self = False
    # timer
    counter = 60
    text = str(counter)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # \=========== game init ===============/

    # /=========== game main ===============\
    while not game_over:
        # img
        gopher_img = pygame.image.load('./gopher.png')
        gopher_d_img = pygame.image.load('./gopher_d.png')
        duke_img = pygame.image.load('./duke.png')
        blood_img = pygame.image.load('./blood.png')
        gopher_img = pygame.transform.scale(gopher_img, (FOOD_BLOCK_SIZE, FOOD_BLOCK_SIZE))
        gopher_d_img = pygame.transform.scale(gopher_d_img, (FOOD_BLOCK_SIZE, FOOD_BLOCK_SIZE))
        duke_img = pygame.transform.scale(duke_img, (BLOCK_SIZE, BLOCK_SIZE))
        blood_img = pygame.transform.scale(blood_img, (BLOCK_SIZE, BLOCK_SIZE))

        # /-------- game close process -----------\
        while game_close == True:
            disp.fill(WHITE)
            if close_hurt_self or close_out_display:
                display_message(disp,
                                basic_font_style,
                                "You Lost!",
                                position=[DISPLAY_W / 4, DISPLAY_H / 3])
            elif close_time_up:
                display_message(disp,
                                basic_font_style,
                                "time up!",
                                position=[DISPLAY_W / 4, DISPLAY_H / 3])

            display_message(disp,
                            basic_font_style,
                            "score: " + str(length_of_snake - 1),
                            position=[DISPLAY_W / 4, DISPLAY_H / 3 + BASIC_FONT_SIZE])
            display_message(disp,
                            basic_font_style,
                            "Press [Q] Quit [C] Play Again",
                            position=[DISPLAY_W / 4, DISPLAY_H / 3 + BASIC_FONT_SIZE*2])
            
            pygame.display.update() 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.QUIT:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        # \-------- game close process -----------/


        # /-------- game main process -----------\
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                snake_dx, snake_dy = calc_snake_pos_diff_by_key(event.key, BLOCK_SIZE)
            if event.type == pygame.USEREVENT:
                counter -= 1
                text = str(counter)
        
        if counter < 0:
            game_close = True
            close_time_up = True
        
        
        # go display outside
        if snake_x < 0 or DISPLAY_W <= snake_x or \
            snake_y < 0 or DISPLAY_H <= snake_y:
            game_close = True
            close_out_display = True

        # snake pos change
        snake_x += snake_dx
        snake_y += snake_dy

        # food draw
        disp.fill(WHITE)
        # pygame.draw.rect(disp, BLUE, [food_x, food_y, FOOD_BLOCK_SIZE, FOOD_BLOCK_SIZE])
        draw_blood(disp, blood_list, blood_img)
        draw_food_img(disp, gopher_img, [food_x, food_y])

        snake_Head = [snake_x, snake_y]
        snake_list.append(snake_Head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True
                close_hurt_self = True

        draw_snake(disp, snake_list, duke_img, gopher_d_img)
        display_score(disp, socre_font_style, length_of_snake - 1)
        display_timer(disp, timer_font_style, text)
        pygame.display.update()

        if is_hit_snake_and_food(snake_x, snake_y, food_x, food_y, BLOCK_SIZE, BLOCK_SIZE):
            blood_list.append([food_x, food_y])
            food_x = round(random.randrange(0, DISPLAY_W - BLOCK_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, DISPLAY_H - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1
        
        clock.tick(SNAKE_SPEED)
        
        # \-------- game main process -----------/

    pygame.quit()
    quit()
    # \=========== game main ===============/


if __name__ == "__main__":
    print("===Start Pygame [Snake Game]===")
    game_loop()