import os
import pygame
from blazyck import *
from PIL import Image

class ResourceManager:
    """Singleton pour gérer les ressources pré-chargées du jeu"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not ResourceManager._initialized:
            self.planete_images = []
            self.asteroide_images = []
            ResourceManager._initialized = True
    
    def load_planetes(self, progress_callback=None):
        """Charge toutes les images de planètes avec callback de progression"""
        self.planete_images = []
        
        for i in range(1, MAX_PLANETES_ANIMATIONS):
            path = os.path.join(PLANETES_PATH, f"planet{i}.png")
            if os.path.exists(path):
                try:
                    # Utiliser PIL pour charger
                    pil_img = Image.open(path).convert("RGBA")
                    mode = pil_img.mode
                    size = pil_img.size
                    data = pil_img.tobytes()
                    img = pygame.image.fromstring(data, size, mode)
                    self.planete_images.append(img)
                    
                    if progress_callback:
                        progress = i / MAX_PLANETES_ANIMATIONS
                        progress_callback(progress)
                except Exception as e:
                    print(f"[ResourceManager] Erreur chargement {path} : {e}")
        
        print(f"[ResourceManager] {len(self.planete_images)} planètes chargées")
    
    def load_asteroides(self, progress_callback=None):
        """Charge toutes les images d'astéroïdes"""
        self.asteroide_images = []
        
        for i in range(1, 50):
            path = os.path.join(ASTEROIDES_PATH, f"aste{i}.png")
            if os.path.exists(path):
                try:
                    pil_img = Image.open(path).convert("RGBA")
                    mode = pil_img.mode
                    size = pil_img.size
                    data = pil_img.tobytes()
                    img = pygame.image.fromstring(data, size, mode)
                    img = pygame.transform.scale(img, (TAILLE_CASE, TAILLE_CASE))
                    self.asteroide_images.append(img)
                    
                    if progress_callback:
                        progress = i / 50
                        progress_callback(progress)
                except Exception as e:
                    print(f"[ResourceManager] Erreur chargement {path} : {e}")
        
        print(f"[ResourceManager] {len(self.asteroide_images)} astéroïdes chargés")
    
    def get_planete_images(self):
        return self.planete_images
    
    def get_asteroide_images(self):
        return self.asteroide_images