from pypresence import Presence
import time

class DiscordRP:
    def __init__(self, client_id):
        self.client_id = client_id
        self.RPC = Presence(client_id)
        self.start_time = int(time.time())
        self.connected = False
        self.large_image = "cover"
        self.large_text = "Xenon Space"
    
    def connect(self):
        """Se connecter à Discord RPC"""
        try:
            self.RPC.connect()
            self.connected = True
            print("[Discord RPC] Connecté")
            return True
        except Exception as e:
            print(f"[Discord RPC] Erreur de connexion : {e}")
            return False
        
    def update(self, state=None, details=None):
        if not self.connected:
            return False
            
        try:
            self.RPC.update(state=state, details=details, large_image=self.large_image, large_text=self.large_text, start=self.start_time)
            return True
        except Exception as e:
            print(f"[Discord RPC] Erreur mise à jour : {e}")
            return False
        
        
if __name__ == "__main__":
        discord = DiscordRP("1419749281190903848")
        discord.connect()
    
        while True:
            discord.update(state="En jeu")
            time.sleep(15)
            