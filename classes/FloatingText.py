import pygame

class FloatingText:
    instances = []  # liste globale de tous les floating texts

    def __init__(self, text, pos, color=(255, 255, 255), lifetime=1.0, rise_speed=30):
        """
        Initialise un texte flottant.

        :param text: Le texte à afficher
        :param pos: La position initiale du texte (en pixels)
        :param color: La couleur du texte (par défaut, blanc)
        :param lifetime: La durée de vie du texte (en secondes, par défaut 1.0)
        :param rise_speed: La vitesse de montée du texte (en px/sec, par défaut 30)
        """
        self.text = text
        self.pos = pygame.Vector2(pos)
        self.color = color
        self.lifetime = lifetime  # durée de vie en secondes
        self.age = 0
        self.rise_speed = rise_speed  # vitesse de montée en px/sec
        self.font = pygame.font.SysFont("consolas", 20)

        # On ajoute automatiquement l'instance à la liste globale
        FloatingText.instances.append(self)

    def update(self, dt):
        """Met à jour la position et l'âge du texte flottant

        La position est mise à jour en fonction de la vitesse de montée
        (en px/sec) et du temps écoulé (en secondes).

        L'âge est incrémenté du temps écoulé.
        """
        self.age += dt
        self.pos.y -= self.rise_speed * dt

    def draw(self, surface):
        """
        Dessine le texte et le supprime automatiquement s'il est expiré

        La transparence de l'image est mise à jour en fonction de l'âge du texte
        et de sa durée de vie. Si l'âge est supérieur à la durée de vie, le texte est supprimé
        automatiquement de la liste globale.
        """
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        if alpha <= 0:
            # Supprime automatiquement de la liste globale
            if self in FloatingText.instances:
                # On retire le texte de la liste globale
                FloatingText.instances.remove(self)
            # On s'arrête là
            return

        # Rendu du texte
        text_surf = self.font.render(self.text, True, self.color)
        # Mise à jour de la transparence
        text_surf.set_alpha(int(alpha))
        # Dessin du texte
        surface.blit(text_surf, (self.pos.x - text_surf.get_width()//2, self.pos.y))

    @classmethod
    def update_all(cls, dt):
        """
        Met à jour tous les floating texts existants.

        :param dt: Le temps écoulé en secondes
        """
        for ft in cls.instances[:]:
            # Mettre à jour l'âge et la position du texte flottant
            ft.update(dt)

    @classmethod
    def draw_all(cls, surface):
        """Dessine tous les floating texts existants
        
        Cette méthode parcourt la liste des instances de la classe
        FloatingText et appelle la méthode draw() sur chaque instance.
        
        :param surface: La surface sur laquelle on souhaite dessiner
        """
        for ft in cls.instances[:]:
            ft.draw(surface)

    @classmethod
    def update_and_draw_all(cls, surface, dt):
        """
        Met à jour et dessine tous les floating texts existants.

        Cette méthode appelle d'abord la méthode update_all() pour mettre à jour
        l'âge et la position de tous les floating texts existants, puis appelle
        la méthode draw_all() pour dessiner tous les floating texts existants sur la
        surface passée en paramètre.

        :param surface: La surface sur laquelle on souhaite dessiner
        :param dt: Le temps écoulé en secondes
        """
        cls.update_all(dt)
        cls.draw_all(surface)