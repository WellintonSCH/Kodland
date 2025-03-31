from pgzero.actor import Actor
from pgzero.builtins import *

class Menu:
    def __init__(self):

        
        # Configurações de tela
        self.screen_width = 1080
        self.screen_height = 720
        
        # Background
        self.background = Actor('menu/background.png')
        self.background.width = self.screen_width
        self.background.height = self.screen_height
        self.background.pos = (self.screen_width // 2, self.screen_height // 2)
        
        # Botões centralizados
        button_x = self.screen_width // 2
        self.play_button = Actor('menu/play_button.png', (button_x, self.screen_height // 2 - 50))
        self.quit_button = Actor('menu/quit_button.png', (button_x, self.screen_height // 2 + 50))
        
        # Botão de som no canto superior direito
        sounds_x = self.screen_width - 50
        sounds_y = 50
        self.sounds_button = Actor('menu/sounds_on.png', (sounds_x, sounds_y))
        
        # Configurações de áudio
        self.music_on = True
        self.button_click_sound = "button_click"
        self.music_toggle_sound = "music_toggle"
        
        # Estados dos botões
        self.play_button.clicked = False
        self.quit_button.clicked = False
        self.sounds_button.clicked = False

    def update(self, mouse_pos, mouse_clicked):
        """Atualiza o estado do menu com base nas interações do mouse"""
        play_hover = self.play_button.collidepoint(mouse_pos)
        quit_hover = self.quit_button.collidepoint(mouse_pos)
        sounds_hover = self.sounds_button.collidepoint(mouse_pos)
        
        if mouse_clicked:
            if play_hover and not self.play_button.clicked:
                self.play_button.clicked = True
                if self.music_on:
                    sounds.tema.play()  # Toca o som do clique
                    
            if quit_hover and not self.quit_button.clicked:
                self.quit_button.clicked = True
                if self.music_on:
                    pass
                    
            if sounds_hover and not self.sounds_button.clicked:
                self.sounds_button.clicked = True
                self.music_on = not self.music_on
                if self.music_on:  # Toca som mesmo quando desligando
                    pass
        else:
            self.play_button.clicked = False
            self.quit_button.clicked = False
            self.sounds_button.clicked = False

    def draw(self):
        self.background.draw()
        self.play_button.draw()
        self.quit_button.draw()
        self.sounds_button.draw()
    
        if self.music_on:
            self.sounds_button.image = 'menu/sounds_on.png'
        else:
            self.sounds_button.image = 'menu/sounds_off.png'

    def get_action(self):
        """Retorna a ação selecionada no menu"""
        if self.play_button.clicked:
            return 'play'
        elif self.quit_button.clicked:
            return 'quit'
        return None