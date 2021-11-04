import pygame

def main():
    print("===Start Pygame [Snake Game]===")
    pygame.init()
    disp = pygame.display.set_mode((400, 300))
    pygame.display.update()
    pygame.display.set_caption("Snake game")
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()