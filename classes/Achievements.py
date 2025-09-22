# achievements.py

class AchievementManager:
<<<<<<< HEAD
    def __init__(self, max_base_level=5):
        # succès disponibles
        self.achievements = {
            "Winner": "Gagner une partie",
            "Explorer": "Parcourir toutes les cases",
            "Great strategist": "Utiliser chaque type de vaisseau au moins une fois.",
            "Base level maximum": "Atteindre le niveau maximum de la base.",
            "Ship destroyer": "Détruire un certain nombre de vaisseaux ennemis.(10)",
            "Unlocked 5 ships": "Débloquer 5 vaisseaux",
            "Unlocked 10 ships": "Débloquer 10 vaisseaux",
        }
        self.unlocked = set()
        
        # Compteurs pour succès
        self.enemy_ships_destroyed = 0
        self.ships_unlocked = set()

        # Données nécessaires pour les succès
        self.ship_types_used = set()  
        self.all_ship_types = {"Petit", "Moyen", "Foreuse"}  
        self.base_level = 1
        self.max_base_level = max_base_level

    def unlock(self, achievement_id):
        """Débloque un succès si c'est pas déjà fait"""
        if achievement_id in self.achievements and achievement_id not in self.unlocked:
            self.unlocked.add(achievement_id)
            print(f"Succès débloqué : {self.achievements[achievement_id]}")
            
    def update_destroyed_ships(self, destroyed_this_turn):
        """
        Appelé à chaque tour pour mettre à jour le compteur de vaisseaux détruits
        :param destroyed_this_turn: int, nombre de vaisseaux ennemis détruits ce tour
        """
        self.enemy_ships_destroyed += destroyed_this_turn
        # Vérifie si le succès est débloqué
        if self.enemy_ships_destroyed >= 10:
            self.unlock("Ship destroyer")
            
    def unlocked_ship(self, ship_type):
        """Appelé quand un vaisseau est débloqué pour vérifier 'Unlocked 5 ships'"""
        self.ships_unlocked.add(ship_type)
        if len(self.ships_unlocked) >= 5:
            self.unlock("Unlocked 5 ships")
        if len(self.ships_unlocked) >= 10:
            self.unlock("Unlocked 10 ships")

    def update_ship_usage(self, ship):
        """Appelé quand un vaisseau est utilisé pour vérifier 'Grand stratège'"""
        ship_type = self.get_ship_type(ship)
        if ship_type:
            self.ship_types_used.add(ship_type)
            if self.all_ship_types.issubset(self.ship_types_used):
                self.unlock("Grand stratège")

    def get_ship_type(self, ship):
        """Détermine le type de vaisseau"""
        if ship.minage:
            return "Foreuse"
        elif ship.tiers == 1 and ship.att > 0:
            return "Petit"
        elif ship.tiers == 1 and ship.att > 100:
            return "Moyen"
        # Ajouter d'autres règles si tu as plus de types
        return None

    def update_base_level(self, level):
        """Appelé quand le niveau de la base change"""
        self.base_level = level
        if self.base_level >= self.max_base_level:
            self.unlock("Base niveau max")
=======
    def __init__(self):
        # Liste de tous les succès possibles
        self.achievements = {
            "winner": "Gagner une partie",
            "explorer": "Parcourir toutes les cases"
        }
        # Succès obtenus (par ID)
        self.unlocked = set()

    def unlock(self, achievement_id):
        """Débloque un succès si ce n'est pas déjà fait"""
        if achievement_id in self.achievements:
            if achievement_id not in self.unlocked:
                self.unlocked.add(achievement_id)
                print(f"Succès débloqué : {self.achievements[achievement_id]}")
            else:
                print(f"Succès déjà obtenu : {self.achievements[achievement_id]}")
        else:
            print(f"Succès inconnu : {achievement_id}")
>>>>>>> b173d32 (Ajout du fichier Achievements.py)

    def has(self, achievement_id):
        """Vérifie si un succès est déjà débloqué"""
        return achievement_id in self.unlocked

    def list_unlocked(self):
        """Retourne la liste des succès obtenus"""
        return [self.achievements[a] for a in self.unlocked]

    def list_all(self):
        """Retourne tous les succès (obtenus ou non)"""
        return self.achievements

<<<<<<< HEAD

=======
# Exemple d'utilisation
if __name__ == "__main__":                  
    manager = AchievementManager()
    manager.unlock("winner")
    manager.unlock("explorer")
    manager.unlock("winner")  # Tentative de débloquer à nouveau
    print("Succès obtenus :", manager.list_unlocked())
    print("Tous les succès :", manager.list_all())
>>>>>>> b173d32 (Ajout du fichier Achievements.py)
