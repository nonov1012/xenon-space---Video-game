import pygame

class ScreenVar:
    screen : pygame.Surface = None
    scale : float = 1.0
    base_width : int = 1920
    base_height : int = 1080

    def __init__(self, screen: pygame.Surface, base_size: tuple[int, int]=(1920, 1080)):
        """
        Initialise la classe Screen avec la surface d'écran et les dimensions de base.
        Args:
            screen (pygame.Surface): La surface d'écran principale.
            base_width (int): La largeur de base pour le calcul de l'échelle.
            base_height (int): La hauteur de base pour le calcul de l'échelle.
        """
        ScreenVar.screen = screen
        ScreenVar.base_width = base_size[0]
        ScreenVar.base_height = base_size[1]

        ScreenVar.update_scale()

    @classmethod
    def update_scale(cls):
        """Met à jour le facteur d'échelle en fonction de la taille actuelle de l'écran."""
        current_width, current_height = cls.screen.get_size()
        scale_x = current_width / cls.base_width
        scale_y = current_height / cls.base_height
        cls.scale = min(scale_x, scale_y)

if __name__ == "__main__":
    # Exemple d'initialisation
    pygame.init()
    screen_surface = pygame.display.set_mode((1920, 1080))
    ScreenVar.__init__(screen_surface, (1920, 1080))
    print(f"Screen size: {screen_surface.get_size()}, Scale factor: {ScreenVar.scale}")
    ScreenVar.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    ScreenVar.update_scale()
    print(f"Screen size: {ScreenVar.screen.get_size()}, Scale factor: {ScreenVar.scale}")
    runing = True
    while runing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
            elif event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                print(f"Screen size: {ScreenVar.screen.get_size()}, Scale factor: {ScreenVar.scale}")
    pygame.quit()