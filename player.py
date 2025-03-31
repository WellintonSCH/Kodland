from pgzero.actor import Actor
from pygame import Rect 
from pgzero.keyboard import keyboard
from pygame.locals import *

class Player:
    def __init__(self, x, y):
        self.actor = Actor('player/knight_r/idle1.png', (x, y))
        self.facing_right = True
        self.state = "idle"
        self.rect = Rect(x, y, self.actor.width , self.actor.height)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.4
        self.jump_power = -14
        self.max_speed = 4
        self.on_ground = False

        self.fell_off = False
        self.limbo_threshold = 0  # Altura máxima permitida antes de considerar que caiu no limbo
        
        # Sistema de combate
        self.health = 100
        self.max_health = 100
        self.attack_cooldown = 0.3
        self.attack_range = 70
        self.attack_damage = 20
        self.invincible = False
        self.invincible_time = 0
        self.hit_flash_time = 0
        
        # Sistema de pontuação
        self.score = 0  # Adicionado o atributo score
        self.coins_collected = 0  # Opcional: para contar colecionáveis
        
        # Inicialização das animações
        self.setup_animations()
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.4

    def setup_animations(self):
        self.walk_r_frames = [f'player/knight_r/run{i}' for i in range(1, 11)]
        self.walk_l_frames = [f'player/knight_l/run{i}' for i in range(1, 11)]
        self.attack_r_frames = [f'player/knight_r/attack{i}' for i in range(1, 3)]
        self.attack_l_frames = [f'player/knight_l/attack{i}' for i in range(1, 3)]
        self.idle_frame_r = "player/knight_r/idle1"
        self.idle_frame_l = "player/knight_l/idle1"
        self.jump_frame_r = "player/knight_r/jump8"  # Frame de pulo para direita
        self.jump_frame_l = "player/knight_l/jump8"  # Frame de pulo para esquerda

    def update(self, platforms, enemies):
        self.handle_input()
        self.apply_physics()
        self.handle_collisions(platforms)
        self.update_combat(enemies)
        self.update_invincibility()
        self.update_animation()
        self.sync_actor_position()

        # Verifica se caiu no limbo
        if self.rect.y > self.limbo_threshold:
            self.fell_off = True

    def update_combat(self, enemies):
        if self.state == "attacking" and self.attack_cooldown <= 0:
            for enemy in enemies:
                if self.can_hit(enemy):
                    enemy.take_damage(self.attack_damage)
                    # Adiciona pontos ao derrotar inimigos (opcional)
                    if enemy.health <= 0:
                        self.score += 50
            self.attack_cooldown = 0.5
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1/60
            
    def can_hit(self, enemy):
        in_range_x = abs(self.rect.centerx - enemy.rect.centerx) < self.attack_range
        in_range_y = abs(self.rect.centery - enemy.rect.centery) < 50
        facing_correct = (self.facing_right and enemy.rect.centerx > self.rect.centerx) or \
                        (not self.facing_right and enemy.rect.centerx < self.rect.centerx)
        return in_range_x and in_range_y and facing_correct
    
    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_time = 1.0
            self.hit_flash_time = 0.1
            
    def update_invincibility(self):
        if self.invincible:
            self.invincible_time -= 1/60
            self.hit_flash_time -= 1/60
            if self.invincible_time <= 0:
                self.invincible = False

    def handle_input(self):
        if keyboard.a:  # Esquerda
            self.vel_x = max(self.vel_x - 0.1, -self.max_speed)
            self.facing_right = False
            if self.on_ground:
                self.state = "walking"
                
        elif keyboard.d:  # Direita
            self.vel_x = min(self.vel_x + 0.1, self.max_speed)
            self.facing_right = True
            if self.on_ground:
                self.state = "walking"
                
        else:  # Desaceleração
            self.vel_x *= 0.8
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0
                if self.on_ground and self.state != "attacking":
                    self.state = "idle"

        if keyboard.space and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.state = "jumping"

        if keyboard.j and self.attack_cooldown <= 0 and self.state != "jumping":
            self.state = "attacking"
            self.vel_x = 0
            self.animation_time = 0  # Reinicia animação de ataque

    def apply_physics(self):
        if not self.on_ground:
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, 10)
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def handle_collisions(self, platforms):
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform):
                overlap_x = min(self.rect.right, platform.right) - max(self.rect.left, platform.left)
                overlap_y = min(self.rect.bottom, platform.bottom) - max(self.rect.top, platform.top)
                
                if overlap_x < overlap_y:
                    if self.vel_x > 0:
                        self.rect.right = platform.left
                    elif self.vel_x < 0:
                        self.rect.left = platform.right
                    self.vel_x = 0
                else:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.top
                        self.vel_y = 0
                        self.on_ground = True
                        if self.state == "jumping":
                            self.state = "idle"
                    elif self.vel_y < 0:
                        self.rect.top = platform.bottom
                        self.vel_y = 0

    def update_animation(self):
        self.animation_time += self.animation_speed
        
        # Determina os frames baseados na direção
        if self.facing_right:
            walk_frames = self.walk_r_frames
            attack_frames = self.attack_r_frames
            idle_frame = self.idle_frame_r
            jump_frame = self.jump_frame_r
        else:
            walk_frames = self.walk_l_frames
            attack_frames = self.attack_l_frames
            idle_frame = self.idle_frame_l
            jump_frame = self.jump_frame_l

        if self.state == "walking":
            self.current_frame = int(self.animation_time) % len(walk_frames)
            self.actor.image = walk_frames[self.current_frame]
        elif self.state == "jumping":
            self.actor.image = jump_frame
        elif self.state == "attacking":
            self.current_frame = int(self.animation_time) % len(attack_frames)
            self.actor.image = attack_frames[self.current_frame]
            
            # Verifica se a animação de ataque terminou
            if self.current_frame == len(attack_frames) - 1:
                if self.on_ground:
                    self.state = "idle"
                else:
                    self.state = "jumping"
        else:  # idle
            self.actor.image = idle_frame

        # Efeito de dano (piscar)
        if self.invincible and self.hit_flash_time > 0:
            self.actor.opacity = 120
        else:
            self.actor.opacity = 255

    def sync_actor_position(self):
        self.actor.pos = (self.rect.centerx, self.rect.centery)

    def draw(self):
        self.actor.draw()

    def collect_item(self, value=10):
        """Método para coletar itens e aumentar pontuação"""
        self.score += value
        self.coins_collected += 1  # Opcional