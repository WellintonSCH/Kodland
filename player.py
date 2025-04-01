from pgzero.actor import Actor
from pygame import Rect 
from pgzero.keyboard import keyboard

class Player:
    def __init__(self, x, y):
        # Configurações básicas
        self.actor = Actor('player/knight_r/idle1.png', (x, y))
        self.rect = Rect(x, y, self.actor.width, self.actor.height)
        self.facing_right = True
        self.state = "idle"
        
        # Física e movimento
        self.vel_x, self.vel_y = 0, 0
        self.gravity = 0.4
        self.jump_power = -14
        self.max_speed = 4
        self.on_ground = False
        
        # Sistema de combate
        self.health = self.max_health = 100
        self.attack_cooldown = 0
        self.attack_range, self.attack_damage = 70, 20
        self.invincible = False
        self.invincible_time = 0
        
        # Progresso do jogo
        self.score = self.coins_collected = 0
        self.fell_off = False
        
        # Configuração de animações
        self._setup_animations()
        self.current_frame = self.animation_time = 0
        self.animation_speed = 0.4

    def _setup_animations(self):
        """Prepara todas as animações do jogador"""
        base_path = 'player/knight_{}/'
        directions = ['r', 'l']
        

        for direction in directions:
            setattr(self, f'walk_{direction}_frames', [f'{base_path.format(direction)}run{i}' for i in range(1, 11)])
            setattr(self, f'attack_{direction}_frames', [f'{base_path.format(direction)}attack{i}' for i in range(1, 3)])
        
        self.idle_frame_r = "player/knight_r/idle1"
        self.idle_frame_l = "player/knight_l/idle1"
        self.jump_frame_r = "player/knight_r/jump8"
        self.jump_frame_l = "player/knight_l/jump8"

    def update(self, platforms, enemies):
        """Atualiza o estado do jogador a cada frame"""
        self._handle_input()
        self._apply_physics()
        self._handle_collisions(platforms)
        self._update_combat(enemies)
        self._update_animation()
        self.actor.pos = self.rect.center
        
        # Verifica se caiu fora da tela
        if self.rect.y > 600: 
            self.fell_off = True

    def _handle_input(self):
        """Processa entrada do jogador"""
        # Movimento horizontal
        if keyboard.a or keyboard.d:
            self.vel_x += -0.1 if keyboard.a else 0.1
            self.vel_x = max(min(self.vel_x, self.max_speed), -self.max_speed)
            self.facing_right = keyboard.d
            if self.on_ground: 
                self.state = "walking"
        else:
            self.vel_x *= 0.8
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0
                if self.on_ground and self.state != "attacking":
                    self.state = "idle"

        # Pulo
        if keyboard.space and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.state = "jumping"

        # Ataque
        if keyboard.j and self.attack_cooldown <= 0 and self.state != "jumping":
            self.state = "attacking"
            self.vel_x = 0
            self.animation_time = 0

    def _apply_physics(self):
        """Aplica física básica (gravidade)"""
        if not self.on_ground:
            self.vel_y = min(self.vel_y + self.gravity, 10)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def _handle_collisions(self, platforms):
        """Detecta e resolve colisões com plataformas"""
        self.on_ground = False
        
       
        original_x = self.rect.x
        original_y = self.rect.y
        
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

                if abs(self.rect.x - original_x) > self.actor.width or abs(self.rect.y - original_y) > self.actor.height:

                    self.rect.x = original_x
                    self.rect.y = original_y
                    break

    def _update_combat(self, enemies):
        """Atualiza lógica de combate"""
        if self.state == "attacking" and self.attack_cooldown <= 0:
            for enemy in enemies:
                if self._can_hit(enemy):
                    enemy.take_damage(self.attack_damage)
                    if enemy.health <= 0:
                        self.score += 50
            self.attack_cooldown = 0.5

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1/60
        if self.invincible:
            self.invincible_time -= 1/60
            if self.invincible_time <= 0:
                self.invincible = False

    def _can_hit(self, enemy):
        """Verifica se o inimigo está no alcance do ataque"""

        in_range_x = abs(self.rect.centerx - enemy.rect.centerx) < self.attack_range

        in_range_y = abs(self.rect.centery - enemy.rect.centery) < 50
        
        facing_correct = (self.facing_right and enemy.rect.centerx > self.rect.centerx) or \
                    (not self.facing_right and enemy.rect.centerx < self.rect.centerx)
        
        return in_range_x and in_range_y and facing_correct

    def _update_animation(self):
        """Atualiza a animação atual do jogador"""
        self.animation_time += self.animation_speed
        direction = 'r' if self.facing_right else 'l'
        
        # Seleciona frames baseado no estado
        if self.state == "walking":
            frames = getattr(self, f'walk_{direction}_frames')
            self.actor.image = frames[int(self.animation_time) % len(frames)]
        elif self.state == "jumping":
            self.actor.image = getattr(self, f'jump_frame_{direction}')
        elif self.state == "attacking":
            frames = getattr(self, f'attack_{direction}_frames')
            self.actor.image = frames[int(self.animation_time) % len(frames)]
            if int(self.animation_time) >= len(frames)-1:
                self.state = "idle" if self.on_ground else "jumping"
        else:  # idle
            self.actor.image = getattr(self, f'idle_frame_{direction}')

        # Efeito de dano (piscar)
        self.actor.opacity = 120 if self.invincible and self.invincible_time > 0.1 else 255

    def take_damage(self, amount):
        """Aplica dano ao jogador com invencibilidade temporária"""
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_time = 1.0

    def collect_item(self, value=10):
        """Coleta itens/power-ups"""
        self.score += value
        self.coins_collected += 1

    def draw(self):
        """Renderiza o jogador"""
        self.actor.draw()
    