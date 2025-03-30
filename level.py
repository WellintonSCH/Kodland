import pygame
import random
from pygame.locals import *
from zombie import Zombie

class Level:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.platforms = self.create_platforms()
        self.enemies = self.create_enemies()
        self.gravity = 0.4
        self.gravity_speed = 0.5

    def create_platforms(self):
        platforms = [
            pygame.Rect(0, 550, 450, 100),  # Chão
            pygame.Rect(600, 100, 200, 50),
            pygame.Rect(500, 250, 200, 50),
            pygame.Rect(280, 400, 200, 50),
        ]
        return platforms
    
    def draw(self, screen):
        for platform in self.platforms:
            screen.draw.filled_rect(platform, (100, 100, 100))
        for enemy in self.enemies:
            enemy.draw()

    def create_enemies(self):
        enemies = []
        
        # Escolhe uma plataforma aleatória (exceto o chão)
        spawnable_platforms = [p for p in self.platforms if p.y < 500]
        if spawnable_platforms:
            platform = random.choice(spawnable_platforms)
            
            # Posiciona o zumbi no centro da plataforma
            spawn_x = platform.x + platform.width/2
            spawn_y = platform.y - 30  # 20 pixels acima da plataforma
            
            enemies.append(Zombie("Zombie", 100, 10, spawn_x, spawn_y))
        
        return enemies

    def update(self, player):
        # Atualiza todos os inimigos
        for enemy in self.enemies:
            enemy.update(player, self.platforms)
        
        # Aplica gravidade aos inimigos
        self.apply_gravity(self.enemies)

    def apply_gravity(self, enemies):
        for enemy in enemies:
            if enemy.rect.bottom < self.height:
                enemy.vel_y += enemy.gravity
            else:
                enemy.vel_y = 0