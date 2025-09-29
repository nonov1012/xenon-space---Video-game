class GameState:
    """Énumération des états du jeu"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class XenonSpaceGame:
    """Classe principale qui gère le jeu complet"""
    
    def __init__(self):
        # État du jeu
        self.state = GameState.MENU
        self.running = True
        
        # Gestionnaire audio
        self.sound_manager = SoundManager()
        
        # Variables de jeu
        self.map = None
        self.player1 = None
        self.player2 = None
        self.achievements = AchievementManager()
        self.shop = None