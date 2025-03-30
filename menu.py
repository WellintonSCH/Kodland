from pgzero.actor import Actor
from pygame import Rect 
import pygame

class Menu:
    def __init__(self):

        self.background = Actor('menu/background.png')
        
        self.play_button = Actor('menu/play_button.png', (400, 300))
        self.quit_button = Actor('menu/quit_button.png', (400, 400))
        self.sounds_button = Actor('menu/sounds_on.png', (400, 500))
        self.music_on = True

        self.play_button.clicked = False
        self.quit_button.clicked = False
        self.sounds_button.clicked = False

    def update(self, mouse_pos, mouse_clicked):
        """Atualiza o estado do menu com base nas interações do mouse
        
        Args:
            mouse_pos: Posição (x, y) do mouse
            mouse_clicked: Booleano indicando se o botão do mouse está pressionado
        """
        # Verifica colisão do mouse com os botões
        play_hover = self.play_button.collidepoint(mouse_pos)
        quit_hover = self.quit_button.collidepoint(mouse_pos)
        sounds_hover = self.sounds_button.collidepoint(mouse_pos)
        
        # Atualiza estado dos botões
        if mouse_clicked:
            if play_hover and not self.play_button.clicked:
                self.play_button.clicked = True
            if quit_hover and not self.quit_button.clicked:
                self.quit_button.clicked = True
            if sounds_hover and not self.sounds_button.clicked:
                self.sounds_button.clicked = True
                self.music_on = not self.music_on  # Alterna estado da música
        else:
            # Reseta o estado de clicked quando o mouse é solto
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
        """Retorna a ação selecionada no menu
        
        Returns:
            str: 'play', 'quit' ou None se nenhuma ação foi selecionada
        """
        if self.play_button.clicked:
            return 'play'
        elif self.quit_button.clicked:
            return 'quit'
        return None