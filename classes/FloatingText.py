import pygame

class FloatingText:
    instances = []  # liste globale de tous les floating texts

    def __init__(self, text, pos, color=(255, 255, 255), lifetime=1.0, rise_speed=30):
        self.text = text
        self.pos = pygame.Vector2(pos)
        self.color = color
        self.lifetime = lifetime  # durée de vie en secondes
        self.age = 0
        self.rise_speed = rise_speed  # vitesse de montée en px/sec
        self.font = pygame.font.SysFont("consolas", 20)

        # On ajoute automatiquement l’instance à la liste globale
        FloatingText.instances.append(self)

    def update(self, dt):
        """Met à jour la position et l’âge"""
        self.age += dt
        self.pos.y -= self.rise_speed * dt

    def draw(self, surface):
        """Dessine le texte et le supprime automatiquement s’il est expiré"""
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        if alpha <= 0:
            # Supprime automatiquement de la liste globale
            if self in FloatingText.instances:
                FloatingText.instances.remove(self)
            return

        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(int(alpha))
        surface.blit(text_surf, (self.pos.x - text_surf.get_width()//2, self.pos.y))

    @classmethod
    def update_all(cls, dt):
        """Met à jour tous les floating texts existants"""
        for ft in cls.instances[:]:
            ft.update(dt)

    @classmethod
    def draw_all(cls, surface):
        """Dessine tous les floating texts existants"""
        for ft in cls.instances[:]:
            ft.draw(surface)

    @classmethod
    def update_and_draw_all(cls, surface, dt):
        """Met à jour et dessine tous les floating texts existants"""
        cls.update_all(dt)
        cls.draw_all(surface)
