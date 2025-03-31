import pgzrun
from player import Player
from level import Level
from menu import Menu

WIDTH = 1080
HEIGHT = 720

# Initialize game objects
level = Level(WIDTH, HEIGHT)
player = Player(100, 400)
menu = Menu()
menu_on = True
game_over = False
game_over_reason = ""

def on_mouse_down(pos, button):
    global menu_on
    if menu_on and button == mouse.LEFT:
        action = menu.handle_click(pos)
        if action == 'play':
            menu_on = False
        elif action == 'quit':
            exit()

def update():
    global menu_on, game_over, game_over_reason
    
    if game_over:
        if keyboard.r:
            reset_game()
        return
    
    if not menu_on:
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
    else:
        draw_game()

def draw_game():
    screen.fill((0, 0, 0))
    level.draw(screen)  # Pass screen to level.draw()
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
    global level, player, menu_on, game_over
    level = Level(WIDTH, HEIGHT)
    player = Player(100, 400)
    menu_on = False
    game_over = False

pgzrun.go()