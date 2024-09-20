import pygame
vec = pygame.math.Vector2

class Wall(pygame.sprite.Sprite):
    def __init__(self, image, WALL_WIDTH, WALL_HEIGHT, x, y):
        super().__init__()
        image = pygame.transform.scale(image, (WALL_WIDTH, WALL_HEIGHT))
        self.surf = image
        self.rect = self.surf.get_rect()

        self.pos = vec((x, y))

        self.rect.topleft = self.pos
    
    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.rect.topleft = self.pos