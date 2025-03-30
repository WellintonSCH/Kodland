from pygame import Rect

class Camera:
    def __init__(self, width, height):
        self.camera = Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.offset = Rect(0, 0, width, height)
        self.smoothness = 0.05  # Quanto menor, mais suave o movimento

    def update(self, target):
        # Calcula onde a câmera deveria estar
        target_x = -target.rect.centerx + WIDTH // 2
        target_y = -target.rect.centery + HEIGHT // 2
        
        # Suaviza o movimento
        self.offset.x += (target_x - self.offset.x) * self.smoothness
        self.offset.y += (target_y - self.offset.y) * self.smoothness
        
        # Limita a câmera aos limites do nível
        self.offset.x = min(0, self.offset.x)  # Não passa do lado esquerdo
        self.offset.y = min(0, self.offset.y)  # Não passa do topo
        self.offset.x = max(-(level.width - WIDTH), self.offset.x)  # Não passa do lado direito
        self.offset.y = max(-(level.height - HEIGHT), self.offset.y)  # Não passa da base

    def apply(self, rect):
        """Aplica o offset a um retângulo Rect"""
        return rect.move(self.offset.x, self.offset.y)

    def apply_pos(self, pos):
        """Aplica o offset a uma posição (x, y)"""
        return (pos[0] + self.offset.x, pos[1] + self.offset.y)