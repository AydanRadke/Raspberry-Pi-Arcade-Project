import pygame
vec = pygame.math.Vector2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, WIDTH, HEIGHT):
        
        super().__init__()
        self.surf = image
        self.rect = self.surf.get_rect()
        self.pos = vec((2 *(WIDTH / 3), 2 * (HEIGHT / 3)))
        self.rect.center = self.pos
    
    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.rect.center = self.pos