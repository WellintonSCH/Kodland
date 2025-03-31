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
        self.background_color = (50, 50, 70)  # Cor de fundo mais escura
        self.platform_color = (80, 110, 80)   # Cor das plataformas
        self.danger_zones = []                # Áreas perigosas
        self.create_danger_zones()
        self.collectibles = []                # Itens colecionáveis
        self.create_collectibles()

    def create_platforms(self):

        platforms = [
            # Plataformas base (mantidas altas)
            pygame.Rect(150, 650, 250, 20),   # 1ª plataforma (y=650)
            pygame.Rect(500, 550, 250, 20),   # 2ª plataforma (+100px)
            pygame.Rect(850, 450, 250, 20),   # 3ª plataforma (+100px)
            
            # Plataformas intermediárias (altura reduzida)
            pygame.Rect(200, 350, 200, 20),   # 4ª plataforma (y=350, era 300)
            pygame.Rect(550, 250, 200, 20),   # 5ª plataforma (y=250, era 200)
            
            # Plataformas superiores (mais acessíveis)
            pygame.Rect(900, 180, 200, 20),   # 6ª plataforma (y=180, era 100)
            
            # Plataforma móvel (ajustada proporcionalmente)
            pygame.Rect(600, 120, 100, 15),   # 7ª plataforma (y=120, era 50)
        ]
        return platforms
    
    def create_danger_zones(self):
        """Cria áreas perigosas como lava ou espinhos"""
        self.danger_zones = [
            pygame.Rect(0, self.height - 30, 150, 30),  # Lava à esquerda
            pygame.Rect(1100, self.height - 30, 180, 30),  # Lava à direita
            pygame.Rect(450, 550, 30, 50),  # Espinhos
        ]
    
    def create_collectibles(self):
        """Cria itens colecionáveis"""
        for _ in range(5):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            self.collectibles.append(pygame.Rect(x, y, 15, 15))

    def draw(self, screen):
        """Desenha todos os elementos do nível"""
        # Fundo
        screen.fill(self.background_color)
        
        # Plataformas
        for platform in self.platforms:
            screen.draw.filled_rect(platform, self.platform_color)
        
        # Zonas perigosas
        for danger in self.danger_zones:
            screen.draw.filled_rect(danger, (200, 50, 50))  # Vermelho
        
        # Colecionáveis
        for item in self.collectibles:
            screen.draw.filled_rect(item, (255, 255, 0))  # Amarelo
        
        # Inimigos
        for enemy in self.enemies:
            enemy.draw()

    def create_enemies(self):
        """Cria inimigos em posições estratégicas"""
        enemies = []
        enemy_count = random.randint(3, 6)  # Entre 3 e 6 inimigos
        
        for _ in range(enemy_count):
            # Escolhe uma plataforma aleatória (exceto o chão principal)
            spawnable_platforms = [p for p in self.platforms if p.y < self.height - 100]
            
            if spawnable_platforms:
                platform = random.choice(spawnable_platforms)
                
                # Posiciona o zumbi na plataforma
                spawn_x = random.randint(
                    platform.left + 30, 
                    platform.right - 30
                )
                spawn_y = platform.top - 30  # 30 pixels acima da plataforma
                
                # Cria tipos diferentes de zumbis
                enemy_type = random.choice(["normal", "strong", "fast"])
                
                if enemy_type == "normal":
                    enemies.append(Zombie("Zumbi", 100, 10, spawn_x, spawn_y))
                elif enemy_type == "strong":
                    enemies.append(Zombie("Zumbi Forte", 150, 15, spawn_x, spawn_y))
                elif enemy_type == "fast":
                    enemies.append(Zombie("Zumbi Rápido", 80, 8, spawn_x, spawn_y, speed=3))
        
        return enemies

    def update(self, player):
        """Atualiza todos os elementos do nível"""
        # Atualiza inimigos
        for enemy in self.enemies[:]:
            enemy.update(player, self.platforms)
            
            # Remove inimigos mortos
            if enemy.health <= 0:
                self.enemies.remove(enemy)
        
        # Aplica gravidade aos inimigos
        self.apply_gravity(self.enemies)
        
        # Verifica colisões com zonas perigosas (opcional)
        self.check_danger_collisions(player)
        
        # Verifica coleta de itens (opcional)
        self.check_collectibles(player)

    def apply_gravity(self, enemies):
        """Aplica gravidade a todos os inimigos"""
        for enemy in enemies:
            on_ground = False
            for platform in self.platforms:
                if enemy.rect.colliderect(platform) and enemy.vel_y > 0:
                    on_ground = True
                    enemy.rect.bottom = platform.top
                    enemy.vel_y = 0
                    break
            
            if not on_ground:
                enemy.vel_y += enemy.gravity

    def check_danger_collisions(self, player):
        """Verifica se o jogador tocou em áreas perigosas"""
        for danger in self.danger_zones:
            if player.rect.colliderect(danger):
                player.take_damage(5)  # Dano contínuo

    def check_collectibles(self, player):
        """Verifica se o jogador coletou itens"""
        for item in self.collectibles[:]:
            if player.rect.colliderect(item):
                self.collectibles.remove(item)
                player.score += 10  # Ou outro benefício