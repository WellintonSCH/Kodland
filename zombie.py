from pgzero.actor import Actor
from pygame import Rect
from pgzero.loaders import sounds

class Zombie:
    def __init__(self, name, health, damage, x, y, speed=2):
        # Atributos básicos
        self.name = name
        self.health = health
        self.damage = damage
        self.state = "idle"
        self.rect = Rect(x, y, 50, 80)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.4
        self.speed = speed
        self.detection_range = 150
        self.attack_distance = 50
        self.attack_range = 50
        self.facing_right = True
        self.on_ground = False
        
        # Sistema de combate
        self.attack_cooldown = 0
        self.attack_delay = 0.5
        self.attacking = False
        self.invincible = False
        self.invincible_time = 0
        
        # Sistema de animação
        self.setup_animations()
        self.actor = Actor(self.idle_r_frames[0], (x, y))
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.15

        # Flags para controle de som
        self.has_played_attack_sound = False
        self.has_played_detect_sound = False

    def setup_animations(self):
        """Configura todos os frames de animação"""
        base_path = 'enemy/zombies/male_'
        
        # Ataque
        self.attack_r_frames = [f'{base_path}r/attack{i}' for i in range(1, 3)]
        self.attack_l_frames = [f'{base_path}l/attack{i}' for i in range(1, 3)]
        
        # Caminhada
        self.walk_r_frames = [f'{base_path}r/walk{i}' for i in range(1, 11)]
        self.walk_l_frames = [f'{base_path}l/walk{i}' for i in range(1, 11)]
        
        # Idle
        self.idle_r_frames = [f'{base_path}r/idle1']
        self.idle_l_frames = [f'{base_path}l/idle1']
        
        # Morte
        self.death_r_frames = [f'{base_path}r/dead1']
        self.death_l_frames = [f'{base_path}l/dead1']

    def is_dead(self):
        """Verifica se o zumbi está morto"""
        return self.state == "dead" or self.health <= 0

    def update(self, player, platforms):
        """Atualiza o estado do zumbi a cada frame"""
        if not self.is_dead():
            self.handle_movement(player)
            self.apply_physics()
            self.handle_collisions(platforms)
            self.update_combat(player)
            self.update_invincibility()
        
        self.update_animation()
        self.sync_actor_position()

    def handle_movement(self, player):
        """Controla o movimento em direção ao jogador"""
        if self.attacking or self.attack_cooldown > 0:
            self.vel_x = 0
            return
            
        dx = player.rect.x - self.rect.x
        distance_x = abs(dx)
        
        # Verifica se o jogador está no mesmo nível
        is_player_on_same_level = abs(self.rect.bottom - player.rect.bottom) < 20
        
        if distance_x < self.detection_range and is_player_on_same_level:

            if self.state != "walking" and not self.has_played_detect_sound:
                sounds.zombie_detect.play()
                self.has_played_detect_sound = True
            
            if distance_x < self.attack_distance:
                self.vel_x = 0
                self.state = "idle"
            else:
                self.state = "walking"
                if dx > 0:
                    self.vel_x = self.speed
                    self.facing_right = True
                else:
                    self.vel_x = -self.speed
                    self.facing_right = False
        else:
            self.state = "idle"
            self.vel_x = 0
            self.has_played_detect_sound = False 

    def can_hit(self, player):
        """Verifica se o jogador está no alcance e no mesmo nível"""
        in_range_x = abs(self.rect.centerx - player.rect.centerx) < self.attack_range

        in_range_y = abs(self.rect.bottom - player.rect.bottom) < 20
        return in_range_x and in_range_y

    def apply_physics(self):
        """Aplica física e gravidade"""
        if not self.on_ground:
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, 10)
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def handle_collisions(self, platforms):
        """Detecta e resolve colisões com plataformas"""
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
                    elif self.vel_y < 0:
                        self.rect.top = platform.bottom
                        self.vel_y = 0

    def update_combat(self, player):
        """Gerencia lógica de combate"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1/60
            return
            
        if self.can_hit(player):
            if not self.attacking:
   
                self.attacking = True
                self.state = "attacking"
                self.attack_delay = 0.5  #
                self.has_played_attack_sound = False 
            else:

                self.attack_delay -= 1/60
                if self.attack_delay <= 0.3 and not self.has_played_attack_sound:
  
                    sounds.zombie_attack.play()
                    self.has_played_attack_sound = True
                
                if self.attack_delay <= 0:
    
                    player.take_damage(self.damage)
                    self.attack_cooldown = 1.5 
                    self.attacking = False
        else:
            self.attacking = False
            self.has_played_attack_sound = False 

    def take_damage(self, amount):
        """Processa dano recebido"""
        if not self.invincible and self.state != "dead":
            self.health -= amount
            self.invincible = True
            self.invincible_time = 0.5
            if self.health <= 0:
                self.state = "dead"
                self.vel_x = 0
                self.attacking = False

    def update_invincibility(self):
        """Atualiza estado de invencibilidade"""
        if self.invincible:
            self.invincible_time -= 1/60
            if self.invincible_time <= 0:
                self.invincible = False

    def update_animation(self):
        """Atualiza a animação atual"""
        self.animation_time += self.animation_speed
        
        if self.state == "dead":
            frames = self.death_r_frames if self.facing_right else self.death_l_frames
            self.actor.image = frames[0]
        elif self.state == "attacking":
            frames = self.attack_r_frames if self.facing_right else self.attack_l_frames
            self.current_frame = int(self.animation_time) % len(frames)
            self.actor.image = frames[self.current_frame]
        elif self.state == "walking":
            frames = self.walk_r_frames if self.facing_right else self.walk_l_frames
            self.current_frame = int(self.animation_time) % len(frames)
            self.actor.image = frames[self.current_frame]
        else:  # idle
            frames = self.idle_r_frames if self.facing_right else self.idle_l_frames
            self.actor.image = frames[0]
        
        self.actor.flip_x = not self.facing_right

    def sync_actor_position(self):
        """Sincroniza posição do ator com a hitbox"""
        self.actor.pos = (self.rect.centerx, self.rect.centery)

    def draw(self, screen=None, camera=None):
        """Desenha o zumbi na tela com suporte para câmera"""
        if self.invincible and self.invincible_time > 0.3:
            self.actor.opacity = 120
        else:
            self.actor.opacity = 255
        
        if camera and screen:
            screen.blit(
                self.actor._surf,
                camera.apply_pos(self.actor.pos)
            )
        else:
            self.actor.draw()