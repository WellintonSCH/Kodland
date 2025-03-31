import pgzrun
import pygame
from player import Player
from level import Level
from menu import Menu

from pygame.locals import *

WIDTH = 1080
HEIGHT = 720

# Inicialização dos objetos
level = Level(WIDTH, HEIGHT)
player = Player(100, 400)
menu = Menu()
menu_on = True
game_over = False  # Adicionado estado de game over
game_over_reason = ""  # Razão do game over

def update():
    global menu_on, game_over, game_over_reason
    
    if game_over:
        # Verifica se o jogador quer reiniciar
        if keyboard.r:
            reset_game()
        return
    
    # Verificar se o menu está ativo
    if menu_on:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        menu.update(mouse_pos, mouse_clicked)
        
        action = menu.get_action()
        if action == 'play':
            menu_on = False
        elif action == 'quit':
            exit()
    else:
        player.update(level.platforms, level.enemies)
        level.update(player)
        # Remove zumbis mortos
        level.enemies = [enemy for enemy in level.enemies if enemy.state != "dead"]
        
        
        if player.health <= 0:
            game_over = True
            game_over_reason = "Você foi derrotado!"

        # Verifica se o jogador caiu no limbo
        if player.rect.y > level.height + 100:  # 100px abaixo do nível
            game_over = True
            game_over_reason = "Você caiu no limbo!"

def draw():
    if menu_on:
        menu.draw()
    elif game_over:
        draw_game_over()
    else:
        draw_game()

def draw_game():
    screen.fill((0, 0, 0))
    level.draw(screen)
    player.draw()
    # Desenha a barra de vida ou outras HUDs aqui
    screen.draw.text(
        f"Vida: {player.health}",
        (10, 10),
        color="white",
        fontsize=30
    )

def draw_game_over():
    """Desenha a tela de game over"""
    # Desenha o jogo esmaecido
    draw_game()
    screen.draw.filled_rect(
        Rect(0, 0, WIDTH, HEIGHT),
        (0, 0, 0, 150)  # Overlay preto semi-transparente
    )
    
    # Mensagem principal
    screen.draw.text(
        game_over_reason,
        center=(WIDTH/2, HEIGHT/2 - 50),
        fontsize=60,
        color="red"
    )
    
    # Instrução para reiniciar
    screen.draw.text(
        "Pressione R para reiniciar",
        center=(WIDTH/2, HEIGHT/2 + 50),
        fontsize=40,
        color="white"
    )

def reset_game():
    """Reinicia o jogo"""
    global level, player, menu_on, game_over
    level = Level(3500, 2000)
    player = Player(100, 400)
    menu_on = False
    game_over = False

pgzrun.go()