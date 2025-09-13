import pygame
class Base:
    def __init__(self, PV_max: int, PV_actuelle: int, att: int, distance_att: int, 
                 cout: int, taille: float, img: pygame.image, tiers: int):
        self.PV_max = PV_max
        self.PV_actuelle = PV_actuelle
        self.att = att
        self.distance_att = distance_att
        self.cout = cout
        self.taille = taille
        self.img = img
        self.tiers = tiers

    def attack(self, cible):
        """Gère l'attaque sur une cible"""
        pass

    def draw(self, surface):
        """Affiche le vaisseau sur l’écran"""
        pass

    def take_damage(self, degats: int):
        """Gère les dégâts reçus"""
        pass

    def dead(self) -> bool:
        """Gere la base détruite"""
        pass
