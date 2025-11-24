import json
import pygame
from pathlib import Path


class ConfigManager:
    """
    Gestionnaire centralisé de la configuration du jeu.
    Charge et sauvegarde les paramètres (touches, audio) depuis/vers save_parametre.json
    """

    DEFAULT_SETTINGS = {
        "touches": {
            "rotation_vaisseau": pygame.K_r,
            "terminer_tour": pygame.K_RETURN,
            "afficher_grille": pygame.K_LCTRL,
            "afficher_zones": pygame.K_LSHIFT,
            "menu_pause": pygame.K_ESCAPE
        },
        "audio": {
            "volume_general": 50,
            "volume_musique": 50,
            "volume_sons": 50
        }
    }

    _instance = None

    def __new__(cls):
        """Singleton pour garantir une seule instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialise le gestionnaire et charge les paramètres"""
        if self._initialized:
            return

        self._initialized = True
        self.config_path = Path(__file__).parent.parent / "save_parametre.json"
        self.settings = self._load_settings()
        self.sound_manager = None  # Sera défini plus tard

    def _load_settings(self):
        """Charge les paramètres depuis le fichier JSON"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)

                # Fusionner avec les paramètres par défaut pour gérer les nouvelles clés
                settings = self.DEFAULT_SETTINGS.copy()
                settings["touches"].update(loaded_settings.get("touches", {}))
                settings["audio"].update(loaded_settings.get("audio", {}))

                return settings
            else:
                # Créer le fichier avec les paramètres par défaut
                self.save_settings(self.DEFAULT_SETTINGS)
                return self.DEFAULT_SETTINGS.copy()

        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors du chargement des paramètres: {e}")
            return self.DEFAULT_SETTINGS.copy()

    def save_settings(self, settings=None):
        """Sauvegarde les paramètres dans le fichier JSON"""
        if settings is None:
            settings = self.settings

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}")

    def get_key(self, action):
        """
        Récupère le code de la touche pour une action donnée

        Args:
            action (str): Nom de l'action ('rotation_vaisseau', 'terminer_tour', etc.)

        Returns:
            int: Code pygame de la touche configurée
        """
        return self.settings["touches"].get(action, self.DEFAULT_SETTINGS["touches"].get(action))

    def set_key(self, action, key_code):
        """
        Définit la touche pour une action

        Args:
            action (str): Nom de l'action
            key_code (int): Code pygame de la touche
        """
        self.settings["touches"][action] = key_code

    def get_audio(self, setting):
        """
        Récupère un paramètre audio

        Args:
            setting (str): Nom du paramètre ('volume_general', 'volume_musique', 'volume_sons')

        Returns:
            int: Valeur du volume (0-100)
        """
        return self.settings["audio"].get(setting, self.DEFAULT_SETTINGS["audio"].get(setting))

    def set_audio(self, setting, value):
        """
        Définit un paramètre audio et l'applique au SoundManager si disponible

        Args:
            setting (str): Nom du paramètre
            value (int): Valeur du volume (0-100)
        """
        self.settings["audio"][setting] = value
        self._apply_audio_settings()

    def _apply_audio_settings(self):
        """Applique les paramètres audio au SoundManager"""
        if self.sound_manager is None:
            return

        try:
            self.sound_manager.set_master_volume(self.settings["audio"]["volume_general"])
            self.sound_manager.set_music_volume(self.settings["audio"]["volume_musique"])
            self.sound_manager.set_sfx_volume(self.settings["audio"]["volume_sons"])
        except Exception as e:
            print(f"Erreur lors de l'application des paramètres audio: {e}")

    def register_sound_manager(self, sound_manager):
        """
        Enregistre le SoundManager et applique les paramètres audio

        Args:
            sound_manager: Instance du SoundManager
        """
        self.sound_manager = sound_manager
        self._apply_audio_settings()

    def reload_settings(self):
        """Recharge les paramètres depuis le fichier"""
        self.settings = self._load_settings()
        self._apply_audio_settings()

    def reset_to_defaults(self):
        """Réinitialise tous les paramètres aux valeurs par défaut"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save_settings()
        self._apply_audio_settings()

    def is_key_pressed(self, action, event):
        """
        Vérifie si une touche d'action a été pressée

        Args:
            action (str): Nom de l'action
            event: Événement pygame KEYDOWN

        Returns:
            bool: True si la touche de l'action a été pressée
        """
        if event.type != pygame.KEYDOWN:
            return False
        return event.key == self.get_key(action)

    def is_key_held(self, action):
        """
        Vérifie si une touche d'action est maintenue enfoncée

        Args:
            action (str): Nom de l'action

        Returns:
            bool: True si la touche est actuellement enfoncée
        """
        keys = pygame.key.get_pressed()
        return keys[self.get_key(action)]


# Instance globale
config = ConfigManager()
