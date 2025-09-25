import pygame

BAR_HEIGHT = 100
ICON_SIZE = 60
ICON_MARGIN = 20
CASE_PADDING = 10

class Shop:
    def __init__(self, player, font, screen):
        self.player = player  # Player doit maintenant avoir un attribut self.economie
        self.font = font
        self.screen = screen

        # Liste des vaisseaux disponibles
        self.ships = [
            {"name": "Petit", "price": 325, "image": self.load_image("assets/img/ships/shop/petit.png")},
            {"name": "Moyen", "price": 650, "image": self.load_image("assets/img/ships/shop/moyen.png")},
            {"name": "Grand", "price": 1050, "image": self.load_image("assets/img/ships/shop/grand.png")},
            {"name": "Foreuse", "price": 400, "image": self.load_image("assets/img/ships/shop/foreuse.png")},
            {"name": "Transporteur", "price": 500, "image": self.load_image("assets/img/ships/shop/transporteur.png")}
        ]

    def load_image(self, path, size=(ICON_SIZE, ICON_SIZE)):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except pygame.error:
            placeholder = pygame.Surface(size, pygame.SRCALPHA)
            placeholder.fill((150, 150, 150))
            return placeholder

    def buy_ship(self, ship):
        # Vérifie si le joueur peut payer via Economie
        if self.player.economie.retirer(ship["price"]):
            # Ajoute le vaisseau au joueur
            #self.player.add_ship(ship["name"])
            print(f"Acheté: {ship['name']}")
        else:
            print("Pas assez de coins !")

    def draw(self):
        num_ships = len(self.ships)
        total_width = num_ships * (ICON_SIZE + 2 * CASE_PADDING) + (num_ships - 1) * ICON_MARGIN
        start_x = (self.screen.get_width() - total_width) // 2
        y = self.screen.get_height() - BAR_HEIGHT + (BAR_HEIGHT - ICON_SIZE) // 2

        mouse_pos = pygame.mouse.get_pos()

        for i, ship in enumerate(self.ships):
            x = start_x + i * (ICON_SIZE + 2 * CASE_PADDING + ICON_MARGIN)
            case_rect = pygame.Rect(x, y, ICON_SIZE + 2 * CASE_PADDING, ICON_SIZE + 2 * CASE_PADDING)

            # Effet au survol
            hovered = case_rect.collidepoint(mouse_pos)
            color = (80, 80, 80) if not hovered else (120, 120, 160)
            pygame.draw.rect(self.screen, color, case_rect, border_radius=8)

            # Dessin de l'icône
            icon_size = ICON_SIZE + 10 if hovered else ICON_SIZE
            icon_img = pygame.transform.scale(ship["image"], (icon_size, icon_size))
            icon_x = x + CASE_PADDING + (ICON_SIZE - icon_size) // 2
            icon_y = y + CASE_PADDING + (ICON_SIZE - icon_size) // 2
            self.screen.blit(icon_img, (icon_x, icon_y))

            ship["rect"] = case_rect

            # Info survol
            if hovered:
                info_text = self.font.render(f"{ship['name']} - {ship['price']} coins", True, (255, 255, 0))
                text_rect = info_text.get_rect(center=(case_rect.centerx, case_rect.top - 15))
                self.screen.blit(info_text, text_rect)

    def handle_click(self, pos):
        for ship in self.ships:
            if ship["rect"].collidepoint(pos):
                self.buy_ship(ship)