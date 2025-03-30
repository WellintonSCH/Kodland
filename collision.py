'''Essa classe será responsável por verificar se houve colisão entre dois objetos.'''

class Collision:

    def __init__(self):
        self.collisions = []  # Lista para armazenar colisões detectadas

    def check_collision(self, rect1, rect2):
        """Verifica se dois retângulos colidem."""
        return rect1.colliderect(rect2)

    def add_collision(self, rect1, rect2):
        """Adiciona uma colisão à lista."""
        if self.check_collision(rect1, rect2):
            self.collisions.append((rect1, rect2))

    def clear_collisions(self):
        """Limpa a lista de colisões."""
        self.collisions.clear()

    
    #função responsavel por verificar o lado da colisão
    def check_side_collision(rect1, rect2):
        """Verifica o lado da colisão entre dois retângulos."""
        if check_collision(rect1, rect2): # type: ignore
            # Verifica a direção da colisão
            if rect1.bottom <= rect2.top:
                return "top"
            elif rect1.top >= rect2.bottom:
                return "bottom"
            elif rect1.right <= rect2.left:
                return "left"
            elif rect1.left >= rect2.right:
                return "right"
        return None