# achievements.py

class AchievementManager:
    def __init__(self, max_base_level=5):
        # succès disponibles
        self.achievements = {
            "winner": "Gagner une partie",
            "explorer": "Parcourir toutes les cases",
            "Grand stratège": "Utiliser chaque type de vaisseau au moins une fois.",
            "Base niveau max": "Atteindre le niveau maximum de la base.",
        }
        self.unlocked = set()

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

    def has(self, achievement_id):
        """Vérifie si un succès est déjà débloqué"""
        return achievement_id in self.unlocked

    def list_unlocked(self):
        """Retourne la liste des succès obtenus"""
        return [self.achievements[a] for a in self.unlocked]

    def list_all(self):
        """Retourne tous les succès (obtenus ou non)"""
        return self.achievements


