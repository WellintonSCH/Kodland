import pgzrun
from player import Player
from level import Level
from menu import Menu

WIDTH = 1080
HEIGHT = 720

level = Level(WIDTH, HEIGHT)
player = Player(100, 400)
menu = Menu()
menu_on = True
game_over = False
game_over_reason = ""
show_controls = False 
controls_timer = 0  

def on_mouse_down(pos, button):
    global menu_on, show_controls, controls_timer
    if menu_on and button == mouse.LEFT:
        action = menu.handle_click(pos)
        if action == 'play':
            menu_on = False
            show_controls = True
            controls_timer = 180
        elif action == 'quit':
            exit()

def update():
    global menu_on, game_over, game_over_reason, show_controls, controls_timer
    
    if game_over:
        if keyboard.r:
            reset_game()
        return

    if show_controls:
        controls_timer -= 1
        if controls_timer <= 0:
            show_controls = False
    
    if not menu_on and not show_controls:
        player.update(level.platforms, level.enemies)
        level.update(player)
        level.enemies = [enemy for enemy in level.enemies if enemy.state != "dead"]
        
        if player.health <= 0:
            game_over = True
            game_over_reason = "Você foi derrotado!"

        if player.rect.y > level.height + 100:
            game_over = True
            game_over_reason = "Você caiu no limbo!"

def draw():
    if menu_on:
        menu.draw()
    elif game_over:
        draw_game_over()
    elif show_controls:
        draw_controls()
    else:
        draw_game()

def draw_controls():
    """Desenha a tela de instruções de controle"""
    screen.fill((0, 0, 0))
    
    # Título
    screen.draw.text(
        "Controles",
        center=(WIDTH/2, HEIGHT/2 - 100),
        fontsize=80,
        color="white"
    )
    
    # Instruções
    controls = [
        "Mover para a esquerda: A",
        "Mover para a direita: D",
        "Pular: BARRA DE ESPAÇO",
        "Atacar: J"
    ]
    
    for i, control in enumerate(controls):
        screen.draw.text(
            control,
            center=(WIDTH/2, HEIGHT/2 + i * 50),
            fontsize=40,
            color="white"
        )
    
    # Mensagem para continuar
    screen.draw.text(
        "O jogo começará em breve...",
        center=(WIDTH/2, HEIGHT - 50),
        fontsize=30,
        color="gray"
    )

def draw_game():
    screen.fill((0, 0, 0))
    level.draw(screen)
    player.draw()
    screen.draw.text(
        f"Vida: {player.health}",
        (10, 10),
        color="white",
        fontsize=30
    )

def draw_game_over():
    draw_game()
    screen.draw.filled_rect(
        Rect(0, 0, WIDTH, HEIGHT),
        (0, 0, 0, 150)
    )
    
    screen.draw.text(
        game_over_reason,
        center=(WIDTH/2, HEIGHT/2 - 50),
        fontsize=60,
        color="red"
    )
    
    screen.draw.text(
        "Pressione R para reiniciar",
        center=(WIDTH/2, HEIGHT/2 + 50),
        fontsize=40,
        color="white"
    )

def reset_game():
    global level, player, menu_on, game_over, show_controls, controls_timer
    level = Level(WIDTH, HEIGHT)
    player = Player(100, 400)
    menu_on = False
    game_over = False
    show_controls = True
    controls_timer = 180

pgzrun.go()