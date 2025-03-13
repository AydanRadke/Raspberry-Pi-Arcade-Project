import pygame
vec = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, starting_position, enemies, starting_direction):
        super().__init__()
        self.surf = pygame.Surface((5, 10))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect()
        self.pos = vec(starting_position)
        self.rect.center = self.pos
        # Find closest enemy, that is target. If no enemy, bullet will go straight
        if enemies:
            self.target = min(enemies, key=lambda e: self.pos.distance_to(e.rect.center))
        else:
            self.target = None
        self.speed = speed
        self.direction = starting_direction
        self.damage = 50


    def update(self, delta_time, enemies, walls, friendly=True):
        if pygame.sprite.spritecollideany(self, walls):
            print("Hit wall?")
            self.kill()
            return True
        if self.target and self.target.health > 0:
            self.direction = vec(self.target.rect.center) - self.pos # finds direction by taking the target center and subracting self
            if self.direction.length() > 0:  # Normalize direction to avoid division by zero
                self.direction = self.direction.normalize()
        else:
            if self.target in enemies:
                enemies.remove(self.target)
                self.target.kill()
            self.target = None


        self.pos += self.direction * self.speed * delta_time
        self.rect.center = self.pos

        if self.target and self.rect.colliderect(self.target.rect):
            self.target.health -= self.damage
            self.kill()
            if self.target.health <= 0:
                self.target.kill()
            return True
        return False
    
    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.rect.center = self.pos

    
