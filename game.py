import pgzrun
import pygame
from player import Player
from level import Level
from menu import Menu

from pygame.locals import *

WIDTH = 1280
HEIGHT = 720

# Inicialização dos objetos
level = Level(3500, 2000)



player = Player(100, 400)
menu = Menu()  # Passando screen para o menu
menu_on = True

def update():
    global menu_on
    
    # Verificar se o menu está ativo
    if menu_on:
        # Obter estado do mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]  # Botão esquerdo
        
        # Atualizar menu
        menu.update(mouse_pos, mouse_clicked)
        
        # Verificar ações do menu
        action = menu.get_action()
        if action == 'play':
            menu_on = False  # Sai do menu e começa o jogo
        elif action == 'quit':
            exit()  # Sai do jogo
    else:
        # Atualizar o jogo normalmente
        player.update(level.platforms, level.enemies)
        level.update(player)
        

def draw():
    if menu_on:
        menu.draw()  # Desenha o menu
    else:
        draw_game()  # Desenha o jogo

def draw_game():
    screen.fill((0, 0, 0))
    level.draw(screen)
    player.draw()
    

    screen.draw.text(
        f"Facing: {'RIGHT' if player.facing_right else 'LEFT'}\n"
        f"State: {player.state}\n"
        f"Zombie: {level.enemies[0].state}\n"
        f"Zombie vel_x: {level.enemies[0].vel_x}\n"
        f"Zombie vel_y: {level.enemies[0].vel_y}\n"
        f"Zombie pos: {level.enemies[0].rect.x}, {level.enemies[0].rect.y}",
        (10, 10), color="white"
    )

pgzrun.go()