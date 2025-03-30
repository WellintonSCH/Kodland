from pgzero.actor import Actor
from pygame import Rect

class Zombie:
    def __init__(self, name, health, damage, x, y):
        # Atributos básicos
        self.name = name
        self.health = health
        self.damage = damage  # <-- Este é o atributo correto para o dano
        self.attack_damage = damage  # <-- Adicionando também como attack_damage para compatibilidade
        
        # Estados e física
        self.state = "idle"
        self.rect = Rect(x, y, 50, 80)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.4
        self.speed = 2
        self.detection_range = 300
        self.facing_right = True
        self.on_ground = False
        
        # Sistema de combate
        self.attack_cooldown = 0
        self.attack_range = 50  # Distância para atacar
        self.invincible = False
        self.invincible_time = 0
        
        # Sistema de animação
        self.setup_animations()
        self.actor = Actor(self.idle_r_frames[0], (x, y))
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.15

    def setup_animations(self):
        """Configura todos os frames de animação"""
        base_path = 'enemy/zombies/male_'
        
        self.attack_r_frames = [f'{base_path}r/attack{i}' for i in range(1, 4)]
        self.attack_l_frames = [f'{base_path}l/attack{i}' for i in range(1, 4)]
        self.walk_r_frames = [f'{base_path}r/walk{i}' for i in range(1, 5)]
        self.walk_l_frames = [f'{base_path}l/walk{i}' for i in range(1, 5)]
        self.idle_r_frames = [f'{base_path}r/idle{i}' for i in range(1, 3)]
        self.idle_l_frames = [f'{base_path}l/idle{i}' for i in range(1, 3)]
        self.death_r_frames = [f'{base_path}r/death{i}' for i in range(1, 4)]
        self.death_l_frames = [f'{base_path}l/death{i}' for i in range(1, 4)]

    def update_combat(self, player):
        """Lógica de combate do zumbi"""
        if self.attack_cooldown <= 0 and self.can_hit(player):
            player.take_damage(self.damage)  # Usando self.damage
            self.attack_cooldown = 1.5  # Tempo de recarga
            self.state = "attacking"
        elif self.attack_cooldown > 0:
            self.attack_cooldown -= 1/60  # Reduz o tempo de recarga

    def can_hit(self, player):
        """Verifica se o jogador está no alcance de ataque"""
        in_range_x = abs(self.rect.centerx - player.rect.centerx) < self.attack_range
        in_range_y = abs(self.rect.centery - player.rect.centery) < 60
        return in_range_x and in_range_y

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
        self.death_r_frames = [f'{base_path}r/death1']
        self.death_l_frames = [f'{base_path}l/death1']

    def update_animation(self):
        """Atualiza a animação baseada no estado atual"""
        self.animation_time += self.animation_speed
        
        if self.state == "dead":
            frames = self.death_r_frames if self.facing_right else self.death_l_frames
            self.current_frame = min(int(self.animation_time), len(frames)-1)
        elif self.state == "attacking":
            frames = self.attack_r_frames if self.facing_right else self.attack_l_frames
            self.current_frame = int(self.animation_time) % len(frames)
        elif self.state == "walking":
            frames = self.walk_r_frames if self.facing_right else self.walk_l_frames
            self.current_frame = int(self.animation_time) % len(frames)
        else:  # idle
            frames = self.idle_r_frames if self.facing_right else self.idle_l_frames
            self.current_frame = int(self.animation_time) % len(frames)
        
        self.actor.image = frames[self.current_frame]
        self.actor.flip_x = not self.facing_right

    def update(self, player, platforms):
        if self.state != "dead":
            self.handle_movement(player)
            self.apply_physics()
            self.handle_collisions(platforms)
            self.update_combat(player)
            self.update_invincibility()
        
        self.update_animation()
        self.sync_actor_position()

    
    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_time = 0.5
            if self.health <= 0:
                self.state = "dead"
                
    def update_invincibility(self):
        if self.invincible:
            self.invincible_time -= 1/60
            if self.invincible_time <= 0:
                self.invincible = False

    def handle_movement(self, player):
        # Calcula a distância horizontal para o jogador
        dx = player.rect.x - self.rect.x
        distance_x = abs(dx)
        
        if distance_x < self.detection_range:
            self.state = "walking"
            if dx > 0:  # Jogador à direita
                self.vel_x = self.speed
                self.facing_right = True
            else:  # Jogador à esquerda
                self.vel_x = -self.speed
                self.facing_right = False
        else:
            self.state = "idle"
            self.vel_x = 0

    def apply_physics(self):
        # Aplica gravidade se não estiver no chão
        if not self.on_ground:
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, 10)  # Limita a velocidade de queda
        
        # Aplica movimento
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def handle_collisions(self, platforms):
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform):
                # Calcula a sobreposição em cada eixo
                overlap_x = min(self.rect.right, platform.right) - max(self.rect.left, platform.left)
                overlap_y = min(self.rect.bottom, platform.bottom) - max(self.rect.top, platform.top)
                
                # Resolve a colisão no eixo com menor sobreposição
                if overlap_x < overlap_y:
                    if self.vel_x > 0:  # Colisão à direita
                        self.rect.right = platform.left
                    elif self.vel_x < 0:  # Colisão à esquerda
                        self.rect.left = platform.right
                    self.vel_x = 0
                else:
                    if self.vel_y > 0:  # Colisão por baixo (caindo)
                        self.rect.bottom = platform.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Colisão por cima (subindo)
                        self.rect.top = platform.bottom
                        self.vel_y = 0


    def sync_actor_position(self):
        """Sincroniza o Actor com o retângulo de colisão"""
        self.actor.pos = (self.rect.centerx, self.rect.centery)

    def draw(self):
        if self.invincible and self.invincible_time > 0.3:
            self.actor.opacity = 120  # Efeito de dano
        else:
            self.actor.opacity = 255
        self.actor.draw()