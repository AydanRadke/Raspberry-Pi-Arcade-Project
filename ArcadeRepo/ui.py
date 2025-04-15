import pygame
from classes.floor import Floor
half_heart = pygame.image.load("ArcadeRepo/assets/heart_half.png")
full_heart = pygame.image.load("ArcadeRepo/assets/heart_full.png")
empty_heart = pygame.image.load("ArcadeRepo/assets/heart_empty.png")

def put_hearts_on_screen(health, WIDTH, HEIGHT):
    hearts = pygame.sprite.Group()
    fulls = health // 2 # number of full hearts
    half = health % 2 # whether there is a half heart or not.
    shift = 0.86 # shift factor
    for i in range(fulls):
        x, y = ((WIDTH / 16) * (i + shift) ), ((HEIGHT / 16))
        new_heart = Floor(full_heart, 34, 34, x, y)
        hearts.add(new_heart)
    
    if half == 1:
        x, y = ((WIDTH / 16) * (fulls + shift)), (HEIGHT / 16)
        new_heart = Floor(half_heart, 34, 34, x, y)
        hearts.add(new_heart)
    
    if health <= 4:
        x, y = ((WIDTH / 16) * (fulls + half + shift)), (HEIGHT / 16)
        new_heart = Floor(empty_heart, 34, 34, x, y)
        hearts.add(new_heart)

        if health <= 2:
            x, y = ((WIDTH / 16) * (fulls + half + 1 + shift)), (HEIGHT / 16)
            new_heart = Floor(empty_heart, 34, 34, x, y)
            hearts.add(new_heart)

    return hearts
            

    