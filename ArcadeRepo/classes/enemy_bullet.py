import pygame
vec = pygame.math.Vector2

class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, starting_position, player):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.pos = vec(starting_position)
        self.rect.center = self.pos
        self.speed = speed
        self.player = player
        self.direction = vec(player.rect.center) - self.pos
        if self.direction.length() > 0:  # Normalize direction to avoid division by zero
                self.direction = self.direction.normalize()


    def update(self, delta_time, enemies, walls, friendly=True):
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()
            return True

        self.pos += self.direction * self.speed * delta_time
        self.rect.center = self.pos

        if self.player and self.rect.colliderect(self.player.rect):
            if not (self.player.dashing_cooldown - self.player.dashing_cooldown_left <= 0.5): # THIS ADDS HALF A SECOND AFTER A DASH WHERE THE PLAYER CANNOT BE HIT
                if self.player.damage_cooldown_left <= 0:
                    self.player.health -= 1
                    self.player.damage_cooldown_left = self.player.damage_cooldown
                    # Kill him dude
                    if self.player.health <= 0:
                        self.player.kill()
                self.kill()
                return True
        return False
    
    def move(self, ACC, delta_time, FRIC, all_sprites):
        self.rect.center = self.pos

    
