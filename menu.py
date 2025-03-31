from pgzero.actor import Actor
from pgzero.loaders import sounds  # Proper way to import sounds

class Menu:
    def __init__(self):
        # Screen settings
        self.screen_width = 1080
        self.screen_height = 720
        
        # Background
        self.background = Actor('menu/background')
        self.background.width = self.screen_width
        self.background.height = self.screen_height
        self.background.pos = (self.screen_width // 2, self.screen_height // 2)
        
        # Centered buttons
        button_x = self.screen_width // 2
        self.play_button = Actor('menu/play_button', (button_x, self.screen_height // 2 - 50))
        self.quit_button = Actor('menu/quit_button', (button_x, self.screen_height // 2 + 50))
        
        # Sound button in top right corner
        sounds_x = self.screen_width - 50
        sounds_y = 50
        self.sounds_button = Actor('menu/sounds_on', (sounds_x, sounds_y))
        
        # Audio settings
        self.music_on = True
        self.button_click_sound = "click"  # Make sure this exists in sounds folder
        self.music_toggle_sound = "toggle"  # Make sure this exists in sounds folder

    def handle_click(self, pos):
        """Handle mouse click and return action"""
        if self.play_button.collidepoint(pos):
            if self.music_on:
                sounds.theme.play()  # Toca o som do clique                    sounds.tema.play()  # Toca o som do clique

            return 'play'
        elif self.quit_button.collidepoint(pos):

            return 'quit'
        elif self.sounds_button.collidepoint(pos):
            self.music_on = not self.music_on

        return None

    def draw(self):
        self.background.draw()
        self.play_button.draw()
        self.quit_button.draw()
        
        # Update sound button image based on state
        self.sounds_button.image = 'menu/sounds_on' if self.music_on else 'menu/sounds_off'
        self.sounds_button.draw()