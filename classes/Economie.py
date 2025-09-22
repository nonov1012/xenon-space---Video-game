class Economie:
    def __init__(self, solde_initial=0):
        self.solde = int(solde_initial)
    
    def ajouter(self, montant: int) -> bool:
        """Ajoute de l'argent au solde"""
        if montant > 0:
            self.solde += montant
            return True
        return False
    
    def retirer(self, montant: int) -> bool:
        """Retire de l'argent si le joueur a assez"""
        if 0 < montant <= self.solde:
            self.solde -= montant
            return True
        return False
    
    def peut_payer(self, montant: int) -> bool:
        """Vérifie si le joueur peut payer"""
        return self.solde >= montant
    
    def etat(self) -> dict:
        return self.solde