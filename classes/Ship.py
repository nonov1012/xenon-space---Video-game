import pygame
import numpy as np
import os
from typing import Tuple, List, Optional
from classes.Animator import Animator


class Ship:
    def __init__(self,
                 pv_max: int,
                 attaque: int,
                 port_attaque: int,
                 port_deplacement: int,
                 cout: int,
                 valeur_mort: int,
                 taille: Tuple[int, int],
                 peut_miner: bool,
                 peut_transporter: bool,
                 image: pygame.Surface,
                 tier: int,
                 ligne: int = 0,
                 colonne: int = 0,
                 screen: Optional[pygame.Surface] = None,
                 uid: Optional[int] = None):
        
        # caractéristiques
        self.pv_max = pv_max
        self.pv_actuel = pv_max
        self.attaque = attaque
        self.port_attaque = port_attaque
        self.port_deplacement = port_deplacement
        self.cout = cout
        self.valeur_mort = valeur_mort
        self.taille = tuple(taille)
        self.peut_miner = peut_miner
        self.peut_transporter = peut_transporter
        self.cargaison = np.array([None, None, None], dtype=object)

        # graphisme / niveau
        self.image = image
        self.tier = tier

        # id stable
        self.id = uid

        # position réelle
        self.ligne = ligne
        self.colonne = colonne
        self.direction = "haut"

        # aperçu (preview)
        self.aperçu_direction = self.direction
        self.aperçu_ligne = ligne
        self.aperçu_colonne = colonne

        self.screen = screen
        self.animator = Animator(
            screen=screen,
            path=f"assets/img/Ships/{self.__class__.__name__.lower()}",
            dimensions=self.taille,
            coord=(self.colonne*40, self.ligne*40),  # TAILLE_CASE = 40
            PV_actuelle=self.pv_actuel,
            PV_max=self.pv_max
        )

    # ------------ utilitaires ------------
    def donner_dimensions(self, direction: str) -> Tuple[int, int]:
        """Retourne (largeur, hauteur) selon l'orientation."""
        if direction in ("haut", "bas"):
            return self.taille
        elif direction in ("droite", "gauche"):
            return (self.taille[1], self.taille[0])

    def _centre_depuis_coin(self, ligne_coin, colonne_coin, direction):
        largeur, hauteur = self.donner_dimensions(direction)
        return ligne_coin + (hauteur-1)/2, colonne_coin + (largeur-1)/2

    def _coin_depuis_centre(self, centre_l, centre_c, direction):
        largeur, hauteur = self.donner_dimensions(direction)
        return int(round(centre_l-(hauteur-1)/2)), int(round(centre_c-(largeur-1)/2))

    # ------------ dessin ------------
    def dessiner(self, surface, taille_case, preview=False):
        if preview:
            ligne, colonne, direction = self.aperçu_ligne, self.aperçu_colonne, self.aperçu_direction
        else:
            ligne, colonne, direction = self.ligne, self.colonne, self.direction

        largeur, hauteur = self.donner_dimensions(direction)
        x, y = colonne*taille_case, ligne*taille_case
        w, h = largeur*taille_case, hauteur*taille_case

        if direction=="haut":
            img = self.image
        elif direction=="droite":
            img = pygame.transform.rotate(self.image, -90)
        elif direction=="gauche":
            img = pygame.transform.rotate(self.image, 90)
        elif direction=="bas":
            img = pygame.transform.rotate(self.image, 180)

        img = pygame.transform.scale(img, (w,h))
        surface.blit(img, (x,y))
        self.update()
        self.animator.update_and_draw()
    
    def update(self):
        self.animator.update(self.pv_actuel, self.pv_max)

        

    # ------------ combat ------------
    def attaquer(self, cible: "Ship"):
        cible.subir_degats(self.attaque)

    def subir_degats(self, degats):
        self.pv_actuel -= degats

    def est_mort(self):
        return self.pv_actuel <= 0

    # ------------ plateau numpy ------------
    def occuper_plateau(self, plateau, valeur, direction=None, ligne=None, colonne=None):
        if direction is None: direction=self.direction
        if ligne is None: ligne=self.ligne
        if colonne is None: colonne=self.colonne
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne+hauteur):
            for c in range(colonne, colonne+largeur):
                plateau[l,c]=valeur

    def verifier_collision(self, plateau, ligne, colonne, direction):
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne+hauteur):
            for c in range(colonne, colonne+largeur):
                if plateau[l,c]!=0: return False
        return True

    # ------------ déplacement / attaque ------------
    def positions_possibles_adjacentes(self, nombre_colonne, nombre_lignes, plateau, direction=None):
        if direction is None:
            direction = self.direction
        largeur, hauteur = self.donner_dimensions(direction)
        positions=[]
        for y in range(-self.port_deplacement,self.port_deplacement+1):
            for i in range(-self.port_deplacement,self.port_deplacement+1):
                if y==0 and i==0: 
                    continue
                if abs(y)+abs(i)<=self.port_deplacement:
                    nl, nc = self.ligne + y, self.colonne + i   # ✅ position réelle
                    if 0 <= nl <= nombre_lignes - hauteur and 0 <= nc <= nombre_colonne - largeur:
                        collision = False
                        for l in range(nl, nl+hauteur):
                            for c in range(nc, nc+largeur):
                                if plateau[l,c]!=0 and plateau[l,c]!=self.id:
                                    collision = True
                        if not collision:
                            positions.append((nl,nc))
        return positions


    def positions_possibles_attaque(self, nombre_colonne, nombre_lignes, direction=None):
        if direction is None:
            direction = self.direction
        positions=[]
        for y in range(-self.port_attaque, self.port_attaque+1):
            for i in range(-self.port_attaque, self.port_attaque+1):
                if y == 0 and i == 0:
                    continue
                if abs(y) + abs(i) <= self.port_attaque:
                    nl, nc = self.ligne + y, self.colonne + i   # calcul brut
                    # ✅ on garde seulement si c’est encore dans la grille
                    if 0 <= nl < nombre_lignes and 0 <= nc < nombre_colonne:
                        positions.append((nl, nc))
        return positions





    def deplacement(self, case_cible, nombre_colonne, nombre_lignes, plateau, Ships):
        if self.id is None: raise ValueError("Ship.id non défini")
        ligne, colonne = case_cible
        cible_direction = self.aperçu_direction  # direction souhaitée après déplacement / rotation

        # ---- attaque si possible (avec la direction visée) ----
        if case_cible in self.positions_possibles_attaque(nombre_colonne, nombre_lignes, direction=cible_direction):
            cible_id = plateau[ligne,colonne]
            if cible_id!=0 and cible_id!=self.id:
                cible_Ship = next((s for s in Ships if s.id==int(cible_id)), None)
                if cible_Ship:
                    self.attaquer(cible_Ship)
                    if cible_Ship.est_mort():
                        cible_Ship.occuper_plateau(plateau,0)
                        Ships.remove(cible_Ship)
                    return True

        # ---- déplacement ----
        # accepter la cible seulement si elle est dans les positions valides pour la direction visée
        if case_cible not in self.positions_possibles_adjacentes(nombre_colonne, nombre_lignes, plateau, direction=cible_direction):
            return False

        ancienne_ligne, ancienne_colonne, ancienne_direction = self.ligne,self.colonne,self.direction
        # libérer l'ancienne occupation
        self.occuper_plateau(plateau,0,direction=ancienne_direction,ligne=ancienne_ligne,colonne=ancienne_colonne)
        # vérifier collision en posant le vaisseau avec la nouvelle direction à la case cible
        if self.verifier_collision(plateau, ligne, colonne, cible_direction):
            self.ligne,self.colonne,self.direction = ligne,colonne,cible_direction
            self.occuper_plateau(plateau,int(self.id),direction=self.direction,ligne=self.ligne,colonne=self.colonne)
            return True
        else:
            # remettre à l'ancienne position si échec
            self.occuper_plateau(plateau,int(self.id),direction=ancienne_direction,ligne=ancienne_ligne,colonne=ancienne_colonne)
            return False

    # ------------ rotation aperçu ------------
    def rotation_aperçu(self, nombre_colonne, nombre_lignes):
        ordre = ["haut","droite","bas","gauche"]
        idx = ordre.index(self.aperçu_direction) if self.aperçu_direction in ordre else 0
        nouvelle_direction = ordre[(idx+1)%len(ordre)]
        centre_l, centre_c = self._centre_depuis_coin(self.aperçu_ligne,self.aperçu_colonne,self.aperçu_direction)
        nouvelle_ligne, nouvelle_col = self._coin_depuis_centre(centre_l,centre_c,nouvelle_direction)
        largeur, hauteur = self.donner_dimensions(nouvelle_direction)
        if 0<=nouvelle_ligne<=nombre_lignes-hauteur and 0<=nouvelle_col<=nombre_colonne-largeur:
            self.aperçu_direction = nouvelle_direction
            self.aperçu_ligne, self.aperçu_colonne = nouvelle_ligne, nouvelle_col

    def rotation_aperçu_si_possible(self, case_souris, nombre_colonne, nombre_lignes):
        self.aperçu_ligne,self.aperçu_colonne = case_souris
        self.rotation_aperçu(nombre_colonne,nombre_lignes)


# ------------ Sous-classes ------------

current_dir = os.path.dirname(__file__)
IMG_DIRS = {
    "petit": os.path.join(current_dir, "..", "assets", "img", "Ships", "petit"),
    "moyen": os.path.join(current_dir, "..", "assets", "img", "Ships", "moyen"),
    "lourd": os.path.join(current_dir, "..", "assets", "img", "Ships", "lourd"),
    "foreuse": os.path.join(current_dir, "..", "assets", "img", "Ships", "foreuse"),
    "transport": os.path.join(current_dir, "..", "assets", "img", "Ships", "transport"),
}


# ------------ Sous-Sous-classes ------------


class petit(Ship):
    def __init__(self, screen: pygame.Surface, position: tuple[int,int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = screen
        self.animator = Animator(
            screen,
            self.image,
            self.taille,
            (position[1]*32, position[0]*32),
            tile_size=32
        )
        self.is_dead_anim_playing = False

    def subir_degats(self, amount: int):
        self.take_damage(amount)

    def take_damage(self, amount: int):
        self.pv_actuel = max(0, self.pv_actuel - max(0, amount))
        if self.pv_actuel > 0:
            self.animator.play("shield")
        else:
            if not self.is_dead_anim_playing:
                self.animator.play("destruction")
                self.is_dead_anim_playing = True

    def dead(self) -> bool:
        return self.pv_actuel <= 0 and self.is_dead_anim_playing and self.animator.is_animation_finished("destruction")

    def update(self):
        self.animator.update(self.pv_actuel, self.pv_max)

    def dessiner(self, surface, taille_case):
        self.update()
        self.animator.update_and_draw()

class moyen(Ship):
    def __init__(self, screen: pygame.Surface, position: tuple[int,int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = screen
        self.animator = Animator(
            screen,
            self.image,
            self.taille,
            (position[1]*32, position[0]*32),
            tile_size=32
        )
        self.is_dead_anim_playing = False

    def subir_degats(self, amount: int):
        self.take_damage(amount)

    def take_damage(self, amount: int):
        self.pv_actuel = max(0, self.pv_actuel - max(0, amount))
        if self.pv_actuel > 0:
            self.animator.play("shield")
        else:
            if not self.is_dead_anim_playing:
                self.animator.play("destruction")
                self.is_dead_anim_playing = True

    def dead(self) -> bool:
        return self.pv_actuel <= 0 and self.is_dead_anim_playing and self.animator.is_animation_finished("destruction")

    def update(self):
        self.animator.update(self.pv_actuel, self.pv_max)

    def dessiner(self, surface, taille_case):
        self.update()
        self.animator.update_and_draw()


class lourd(Ship):
    def __init__(self, screen: pygame.Surface, position: tuple[int,int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = screen
        self.animator = Animator(
            screen,
            self.image,
            self.taille,
            (position[1]*32, position[0]*32),
            tile_size=32
        )
        self.is_dead_anim_playing = False

    def subir_degats(self, amount: int):
        self.take_damage(amount)

    def take_damage(self, amount: int):
        self.pv_actuel = max(0, self.pv_actuel - max(0, amount))
        if self.pv_actuel > 0:
            self.animator.play("shield")
        else:
            if not self.is_dead_anim_playing:
                self.animator.play("destruction")
                self.is_dead_anim_playing = True

    def dead(self) -> bool:
        return self.pv_actuel <= 0 and self.is_dead_anim_playing and self.animator.is_animation_finished("destruction")

    def update(self):
        self.animator.update(self.pv_actuel, self.pv_max)

    def dessiner(self, surface, taille_case):
        self.update()
        self.animator.update_and_draw()



class foreuse(Ship):
    def __init__(self, screen: pygame.Surface, position: tuple[int,int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = screen
        self.animator = Animator(
            screen,
            self.image,
            self.taille,
            (position[1]*32, position[0]*32),
            tile_size=32
        )
        self.is_dead_anim_playing = False

    def subir_degats(self, amount: int):
        self.take_damage(amount)

    def take_damage(self, amount: int):
        self.pv_actuel = max(0, self.pv_actuel - max(0, amount))
        if self.pv_actuel > 0:
            self.animator.play("shield")
        else:
            if not self.is_dead_anim_playing:
                self.animator.play("destruction")
                self.is_dead_anim_playing = True

    def dead(self) -> bool:
        return self.pv_actuel <= 0 and self.is_dead_anim_playing and self.animator.is_animation_finished("destruction")

    def update(self):
        self.animator.update(self.pv_actuel, self.pv_max)

    def dessiner(self, surface, taille_case):
        self.update()
        self.animator.update_and_draw()



class Transport(Ship):
    def __init__(self, screen: pygame.Surface, image_dir: str, position: tuple[int,int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cargaison = []  # liste des vaisseaux stockés
        self.screen = screen
        self.animator = Animator(
            screen,
            image_dir,
            self.taille,
            (position[1]*32, position[0]*32),
            tile_size=32
        )
        self.is_dead_anim_playing = False

    def subir_degats(self, amount: int):
        self.take_damage(amount)

    def take_damage(self, amount: int):
        self.pv_actuel = max(0, self.pv_actuel - max(0, amount))
        if self.pv_actuel > 0:
            self.animator.play("shield")
        else:
            if not self.is_dead_anim_playing:
                self.animator.play("destruction")
                self.is_dead_anim_playing = True

    def dead(self) -> bool:
        return self.pv_actuel <= 0 and self.is_dead_anim_playing and self.animator.is_animation_finished("destruction")

    def update(self):
        self.animator.update(self.pv_actuel, self.pv_max)

    def dessiner(self, surface, taille_case):
        self.update()
        self.animator.update_and_draw()


    def ajouter_cargo(self, Ship: Ship, plateau) -> bool:
        """Ajoute un vaisseau dans le transport si possible."""
        # Autoriser seulement petit ou moyen
        if not isinstance(Ship, (petit, moyen)):
            return False

        if len(self.cargaison) >= 3:
            return False

        taille_cargo = [self._taille_vaisseau(s) for s in self.cargaison] + [self._taille_vaisseau(Ship)]
        if sum(taille_cargo) > 3:
            return False

        # Retirer du plateau
        Ship.occuper_plateau(plateau, 0)

        # Ajouter dans la cargaison
        self.cargaison.append(Ship)
        return True



    def retirer_cargo(self, index: int, ligne: int, colonne: int, plateau) -> bool:
        """Débarque un vaisseau du transport sur le plateau."""
        if 0 <= index < len(self.cargaison):
            Ship = self.cargaison.pop(index)
            Ship.ligne, Ship.colonne = ligne, colonne
            Ship.direction = "haut"
            Ship.occuper_plateau(plateau, Ship.id)
            return True
        return False

    def _taille_vaisseau(self, Ship: Ship) -> int:
        if isinstance(Ship, petit):
            return 1
        elif isinstance(Ship, moyen):
            return 2
        else:
            return 3

    def subir_degats(self, degats, plateau=None):
        """Si le transport meurt, tous les vaisseaux embarqués meurent."""
        super().subir_degats(degats)
        if self.est_mort() and plateau is not None:
            for Ship in self.cargaison:
                Ship.pv_actuel = 0
                Ship.occuper_plateau(plateau, 0)
            self.cargaison.clear()
    
    def afficher_cargaison(self, fenetre, taille_case):
        """Affiche les vaisseaux stockés avec images miniatures au-dessus du transport"""
        for i, Ship in enumerate(self.cargaison):
            mini_img = pygame.transform.scale(Ship.image, (20,20))
            x = self.colonne * taille_case + i*22
            y = self.ligne * taille_case - 22
            fenetre.blit(mini_img, (x, y))


    def positions_debarquement(self, Ship_stocke, plateau, nombre_lignes, nombre_colonnes):
        """Retourne les positions valides pour débarquer un vaisseau depuis ce transport."""
        positions_valides = []
        port = self.port_deplacement
        for dy in range(-port, port+1):
            for dx in range(-port, port+1):
                if abs(dy) + abs(dx) > port:
                    continue
                nl = self.ligne + dy
                nc = self.colonne + dx
                largeur, hauteur = Ship_stocke.donner_dimensions(Ship_stocke.direction)

                # Vérifier que tout le rectangle du vaisseau est dans la grille
                if not (0 <= nl <= nombre_lignes - hauteur and 0 <= nc <= nombre_colonnes - largeur):
                    continue

                # Vérifier que toutes les cases sont libres
                collision = False
                for l in range(nl, nl+hauteur):
                    for c in range(nc, nc+largeur):
                        if plateau[l,c] != 0:
                            collision = True
                            break
                    if collision:
                        break

                if not collision:
                    positions_valides.append((nl,nc))
        return positions_valides


