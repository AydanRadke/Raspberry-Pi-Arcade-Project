import pygame
vec = pygame.math.Vector2

class Wall(pygame.sprite.Sprite):
    def __init__(self, image, WALL_WIDTH, WALL_HEIGHT, WIDTH, HEIGHT):
        super().__init__()
        image = pygame.transform.scale(image, (WALL_WIDTH, WALL_HEIGHT))
        self.surf = image
        self.rect = self.surf.get_rect()

        self.pos = vec((WIDTH / 3, HEIGHT / 3))

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
    
    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.rect.center = self.pos