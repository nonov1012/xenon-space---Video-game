from pypresence import Presence
import time
import psutil
import os

class DiscordRichPresence:
    def __init__(self, client_id):
        self.client_id = client_id
        self.RPC = Presence(client_id)
        self.start_time = int(time.time())
        self.connected = False
    
    def connect(self):
        """Se connecter à Discord RPC"""
        try:
            self.RPC.connect()
            self.connected = True
            print("✅ Connecté à Discord RPC")
            return True
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")
            return False
    
    def update_presence(self, state=None, details=None, large_image=None, 
                       large_text=None, small_image=None, small_text=None, 
                       buttons=None):
        """Mettre à jour la Rich Presence"""
        if not self.connected:
            return False
            
        try:
            self.RPC.update(
                state=state,
                details=details,
                large_image=large_image,
                large_text=large_text,
                small_image=small_image,
                small_text=small_text,
                start=self.start_time,
                buttons=buttons
            )
            return True
        except Exception as e:
            print(f"❌ Erreur mise à jour : {e}")
            return False
    
    def get_system_info(self):
        """Obtenir des informations système pour la présence"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        return {
            'cpu': f"{cpu_percent}%",
            'memory': f"{memory.percent}%"
        }
    
    def close(self):
        """Fermer la connexion RPC"""
        if self.connected:
            self.RPC.close()
            print("🔒 Connexion fermée")

def main():
    # Votre Client ID Discord
    CLIENT_ID = "1419749281190903848"  # Remplacez par votre Client ID
    
    # Initialiser la Rich Presence
    rpc = DiscordRichPresence(CLIENT_ID)
    
    if not rpc.connect():
        return
    
    try:
        counter = 0
        while True:
            # Obtenir les infos système
            system_info = rpc.get_system_info()
            
            # Différents états selon le temps
            states = [
                "🐍 Codage en Python",
                "🔧 Debug en cours",
                "📚 Apprentissage",
                "💡 Réflexion créative"
            ]
            
            current_state = states[counter % len(states)]
            
            # Mettre à jour la présence
            rpc.update_presence(
                state=current_state,
                details=f"CPU: {system_info['cpu']} | RAM: {system_info['memory']}",
                large_image="python",
                large_text="Développeur Python",
                small_image="computer",
                small_text="En ligne",
                buttons=[
                    {"label": "Mon GitHub", "url": "https://github.com/username"},
                    {"label": "Portfolio", "url": "https://monportfolio.com"}
                ]
            )
            
            print(f"🔄 Présence mise à jour : {current_state}")
            
            # Attendre 30 secondes avant la prochaine mise à jour
            time.sleep(30)
            counter += 1
            
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt du programme...")
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        rpc.close()

if __name__ == "__main__":
    main()