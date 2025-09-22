# achievements.py

class AchievementManager:
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

    def has(self, achievement_id):
        """Vérifie si un succès est déjà débloqué"""
        return achievement_id in self.unlocked

    def list_unlocked(self):
        """Retourne la liste des succès obtenus"""
        return [self.achievements[a] for a in self.unlocked]

    def list_all(self):
        """Retourne tous les succès (obtenus ou non)"""
        return self.achievements

# Exemple d'utilisation
if __name__ == "__main__":                  
    manager = AchievementManager()
    manager.unlock("winner")
    manager.unlock("explorer")
    manager.unlock("winner")  # Tentative de débloquer à nouveau
    print("Succès obtenus :", manager.list_unlocked())
    print("Tous les succès :", manager.list_all())