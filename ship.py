# ship.py
import pygame
import numpy as np

class Ship:
    def __init__(self, max_health: int, attack_power: int, attack_range: int, movement_range: int,
                 cost: int, value_on_death: int, size: tuple, can_mine: bool, can_transport: bool,
                 image: pygame.Surface, tier: int, row=0, col=0):
        """
        Initialise un vaisseau avec ses caractéristiques.
        """
        self.max_health = max_health
        self.current_health = max_health
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.movement_range = movement_range
        self.cost = cost
        self.value_on_death = value_on_death
        self.size = size  # (width, height) en cases
        self.can_mine = can_mine
        self.can_transport = can_transport
        self.cargo = np.array([None, None, None], dtype=object)
        self.image = image
        self.tier = tier

        self.row = row
        self.col = col
        self.direction = "down"
        self.preview_direction = self.direction

    # -------------------- Méthodes principales -------------------- #

    def get_dimensions(self, direction):
        """Retourne (width, height) selon la direction"""
        if direction in ("up", "down"):
            return self.size
        else:  # "left" ou "right"
            return (self.size[1], self.size[0])

    def draw(self, surface, tile_size):
        """Dessine le vaisseau sur la surface pygame"""
        width, height = self.get_dimensions(self.direction)
        x = self.col * tile_size
        y = self.row * tile_size
        w = width * tile_size
        h = height * tile_size

        if self.direction == "down":
            img_rot = self.image
        elif self.direction == "up":
            img_rot = pygame.transform.rotate(self.image, 180)
        elif self.direction == "left":
            img_rot = pygame.transform.rotate(self.image, 90)
        elif self.direction == "right":
            img_rot = pygame.transform.rotate(self.image, -90)

        img_rot = pygame.transform.scale(img_rot, (w, h))
        surface.blit(img_rot, (x, y))

    def take_damage(self, damage):
        """Réduit les PV du vaisseau"""
        self.current_health -= damage

    def dead(self):
        """Vaisseau détruit"""
        return self.current_health <= 0

    # -------------------- Déplacement -------------------- #

    def possible_adjacent_positions(self, nb_colonnes, nb_lignes):
        """Cases adjacentes autour de la tête du vaisseau"""
        width, height = self.get_dimensions(self.direction)
        head_row, head_col = self.row, self.col
        if self.direction == "right":
            head_col += width - 1

        positions = []
        for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = head_row + d_row, head_col + d_col
            if 0 <= new_row < nb_lignes and 0 <= new_col < nb_colonnes:
                positions.append((new_row, new_col))
        return positions

    def is_within_board(self, row, col, direction, nb_colonnes, nb_lignes):
        """Retourne True si le vaisseau reste dans le plateau"""
        width, height = self.get_dimensions(direction)
        return 0 <= row <= nb_lignes - height and 0 <= col <= nb_colonnes - width

    def get_possible_positions(self, nb_colonnes, nb_lignes):
        """Retourne les positions possibles pour le déplacement"""
        return self.possible_adjacent_positions(nb_colonnes, nb_lignes)

    def move_to(self, target_tile, nb_colonnes, nb_lignes):
        """Déplace le vaisseau vers target_tile si possible"""
        row, col = target_tile
        if (row, col) in self.get_possible_positions(nb_colonnes, nb_lignes) and \
           self.is_within_board(row, col, self.preview_direction, nb_colonnes, nb_lignes):
            self.row = row
            self.col = col
            self.direction = self.preview_direction
            return True
        return False

    # -------------------- Rotation -------------------- #

    def rotate_preview(self, nb_colonnes, nb_lignes, mouse_tile):
        """Tourne la prévisualisation si possible"""
        directions = ["up", "right", "down", "left"]
        idx = directions.index(self.preview_direction)
        new_direction = directions[(idx + 1) % 4]
        row, col = mouse_tile

        if self.is_within_board(row, col, new_direction, nb_colonnes, nb_lignes):
            self.preview_direction = new_direction

    def rotate_preview_if_possible(self, mouse_tile, nb_colonnes, nb_lignes):
        self.rotate_preview(nb_colonnes, nb_lignes, mouse_tile)
