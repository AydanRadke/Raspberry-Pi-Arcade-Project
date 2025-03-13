import pygame

buildings = pygame.image.load("ArcadeRepo/assets/neo_zero_buildings_02.png")
dungeon_tiles = pygame.image.load("ArcadeRepo/assets/neo_zero_dungeon_02.png")
tiles = pygame.image.load("ArcadeRepo/assets/neo_zero_tileset_02.png")

def get_building(x, y):
    width = 48
    height = 32
    image = pygame.Surface((width, height), pygame.SRCALPHA)  # Preserve transparency
    image.blit(buildings, (0, 0), (x, y, width, height))  # Copy the desired part
    return image

def get_dungeon_tile(x, y):
    width = 16
    height = 16
    image = pygame.Surface((width, height), pygame.SRCALPHA)  # Preserve transparency
    image.blit(dungeon_tiles, (0, 0), (x, y, width, height))  # Copy the desired part
    return image

def get_tile(x, y):
    width = 16
    height = 16
    image = pygame.Surface((width, height), pygame.SRCALPHA)  # Preserve transparency
    image.blit(dungeon_tiles, (0, 0), (x, y, width, height))  # Copy the desired part
    return image
    