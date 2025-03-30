from pgzero.actor import Actor
from pygame import Rect 
from pgzero.keyboard import keyboard
from pygame.locals import *

class Player:
    def __init__(self, x, y):
        self.health = 100
        self.max_health = 100
        self.actor = Actor('player/knight_r/idle1.png', (x, y))
        self.facing_right = True
        self.state = "idle"
        self.rect = Rect(x, y, self.actor.width * 0.75, self.actor.height * 0.9)  # Hitbox menor que o sprite
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.4
        self.jump_power = -12
        self.max_speed = 4

        self.on_ground = False
        self.attack_cooldown = 0
        self.attack_range = 70
        self.attack_damage = 20
        self.invincible = False
        self.invincible_time = 0
        self.hit_flash_time = 0
        
        # Animação
        self.frames_path = 'player/knight_r/' if self.facing_right else 'player/knight_l/'
        
        self.walk_r_frames = [f'player/knight_r/run{i}' for i in range(1, 11)]
        self.walk_l_frames = [f'player/knight_l/run{i}' for i in range(1, 11)]
        self.attack_r_frames = [f'player/knight_r/attack{i}' for i in range(1, 3)]
        self.attack_l_frames = [f'player/knight_l/attack{i}' for i in range(1, 3)]

        self.walk_frames = self.walk_r_frames if self.facing_right else self.walk_l_frames

        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.3

    def update(self, platforms, enemies):   
        self.handle_input()
        self.apply_physics()
        self.handle_collisions(platforms)
        self.update_animation()
        self.sync_actor_position()
        self.update_combat(enemies)
        self.update_invincibility()

    def update_combat(self, enemies):
        if self.state == "attacking" and self.attack_cooldown <= 0:
            for enemy in enemies:
                if self.can_hit(enemy):
                    enemy.take_damage(self.attack_damage)
            self.attack_cooldown = 0.5  # Tempo de recarga do ataque
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1/60  # Reduz o tempo de recarga
            
    def can_hit(self, enemy):
        # Verifica se o inimigo está dentro do alcance de ataque
        in_range_x = abs(self.rect.centerx - enemy.rect.centerx) < self.attack_range
        in_range_y = abs(self.rect.centery - enemy.rect.centery) < 50
        facing_correct = (self.facing_right and enemy.rect.centerx > self.rect.centerx) or \
                        (not self.facing_right and enemy.rect.centerx < self.rect.centerx)
        return in_range_x and in_range_y and facing_correct
    
    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_time = 1.0  # 1 segundo de invencibilidade
            self.hit_flash_time = 0.1  # Efeito visual
            
    def update_invincibility(self):
        if self.invincible:
            self.invincible_time -= 1/60
            self.hit_flash_time -= 1/60
            if self.invincible_time <= 0:
                self.invincible = False

    def handle_input(self):

        if keyboard.a:  # Movimento para esquerda
            self.vel_x = max(self.vel_x - 0.1, -self.max_speed)
            self.facing_right = False

            if self.on_ground:
                self.state = "walking"
                
        elif keyboard.d:  # Movimento para direita
            self.vel_x = min(self.vel_x + 0.1, self.max_speed)
            self.facing_right = True

            if self.on_ground:
                self.state = "walking"
                
        else:  # Desaceleração
            self.vel_x *= 0.8
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0
                if self.on_ground:
                    self.state = "idle"

        if keyboard.space and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.state = "jumping"

        if keyboard.j:  # Ataque
            self.state = "attacking"
            self.vel_x = 0  # Parar movimento durante o ataque


    def apply_physics(self):
        # Aplicar gravidade
        if not self.on_ground:
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, 10)
        
        # Movimento
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    
    def handle_collisions(self, platforms):
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform):
                # Calcula a sobreposição em cada eixo
                overlap_x = min(self.rect.right, platform.right) - max(self.rect.left, platform.left)
                overlap_y = min(self.rect.bottom, platform.bottom) - max(self.rect.top, platform.top)
                
                # Resolve a colisão no eixo com menor sobreposição primeiro
                if overlap_x < overlap_y:
                    
                    if self.vel_x > 0:  # Indo para direita
                        self.rect.right = platform.left
                    elif self.vel_x < 0:  # Indo para esquerda
                        self.rect.left = platform.right
                    self.vel_x = 0
                else:
                    
                    if self.vel_y > 0:  # Caindo
                        self.rect.bottom = platform.top
                        self.vel_y = 0
                        self.on_ground = True
                        if self.state == "jumping":
                            self.state = "idle"
                    elif self.vel_y < 0:  # Subindo
                        self.rect.top = platform.bottom
                        self.vel_y = 0

    def update_animation(self):
        # Atualizar animação baseada no estado
        if self.state == "walking":
            self.animation_time += self.animation_speed
            self.current_frame = int(self.animation_time) % len(self.walk_frames)
            self.actor.image = self.walk_frames[self.current_frame]
        elif self.state == "jumping":
            self.actor.image = f"{self.frames_path}jump8"
        elif self.state == "attacking":
            self.animation_time += self.animation_speed
            self.current_frame = int(self.animation_time) % len(self.attack_r_frames if self.facing_right else self.attack_l_frames)
            self.actor.image = (self.attack_r_frames if self.facing_right else self.attack_l_frames)[self.current_frame]
            if self.current_frame == len(self.attack_r_frames) - 1:
                self.state = "idle"
        else:
            self.actor.image = f"{self.frames_path}idle1"

        self.walk_frames = self.walk_r_frames if self.facing_right else self.walk_l_frames
        self.frames_path = 'player/knight_r/' if self.facing_right else 'player/knight_l/'


    def sync_actor_position(self):
        """Sincroniza o Actor com o retângulo de colisão"""
        self.actor.pos = (self.rect.centerx, self.rect.centery)


    def draw(self):
        self.actor.draw()