import pygame
from classes.GlobalVar.ScreenVar import ScreenVar

class GridVar:
    nb_cells_x: int = 50
    nb_cells_y: int = 30
    cell_size: int = 0
    grid_width: int = 0
    grid_height: int = 0
    offset_x: int = 0
    offset_y: int = 0
    min_offset_x: int = 100
    min_offset_y: int = 85

    @classmethod
    def update_grid(cls):
        """Met à jour les dimensions de la grille en fonction de la taille d'écran."""
        screen_width, screen_height = ScreenVar.screen.get_size()
        
        # Calcule la taille des cellules en fonction de l'espace disponible
        available_height = screen_height - cls.min_offset_y
        available_width = screen_width - (2 * cls.min_offset_x)
        
        # Utilise la contrainte la plus restrictive pour garder les cellules carrées
        cell_size_by_height = available_height // cls.nb_cells_y
        cell_size_by_width = available_width // cls.nb_cells_x
        cls.cell_size = min(cell_size_by_height, cell_size_by_width)
        
        # Calcule les dimensions réelles de la grille
        cls.grid_width = cls.nb_cells_x * cls.cell_size
        cls.grid_height = cls.nb_cells_y * cls.cell_size
        
        # Centre la grille avec des offsets minimums
        cls.offset_x = max((screen_width - cls.grid_width) // 2, cls.min_offset_x)
        cls.offset_y = max((screen_height - cls.grid_height) // 2, cls.min_offset_y)

    def __init__(self, nb_cells_x: int = 50, nb_cells_y: int = 30):
        GridVar.nb_cells_x = nb_cells_x
        GridVar.nb_cells_y = nb_cells_y
        GridVar.update_grid()

def test_grid_var():
    """Tests unitaires pour la classe GridVar"""
    
    print("="*70)
    print("TESTS UNITAIRES - GridVar")
    print("="*70)
    
    pygame.init()
    
    # Initialisation de base
    screen = pygame.display.set_mode((1920, 1080))
    ScreenVar(screen, (1920, 1080))
    
    # TEST 1: Initialisation par défaut (50x30 cellules)
    print("\n[TEST 1] Initialisation avec 50x30 cellules sur écran 1920x1080")
    print("-" * 70)
    GridVar(50, 30)
    
    assert GridVar.nb_cells_x == 50, "❌ nb_cells_x devrait être 50"
    assert GridVar.nb_cells_y == 30, "❌ nb_cells_y devrait être 30"
    assert GridVar.cell_size > 0, "❌ cell_size devrait être > 0"
    assert GridVar.grid_width == GridVar.nb_cells_x * GridVar.cell_size, "❌ grid_width mal calculé"
    assert GridVar.grid_height == GridVar.nb_cells_y * GridVar.cell_size, "❌ grid_height mal calculé"
    assert GridVar.offset_x >= GridVar.min_offset_x, "❌ offset_x sous le minimum"
    assert GridVar.offset_y >= GridVar.min_offset_y, "❌ offset_y sous le minimum"
    
    print(f"✓ Cellules: {GridVar.nb_cells_x}x{GridVar.nb_cells_y}")
    print(f"✓ Taille cellule: {GridVar.cell_size}px")
    print(f"✓ Dimensions grille: {GridVar.grid_width}x{GridVar.grid_height}px")
    print(f"✓ Offsets: X={GridVar.offset_x}px, Y={GridVar.offset_y}px")
    
    # Vérification que la grille ne dépasse pas
    screen_w, screen_h = screen.get_size()
    grid_end_x = GridVar.offset_x + GridVar.grid_width
    grid_end_y = GridVar.offset_y + GridVar.grid_height
    
    assert grid_end_x <= screen_w, f"❌ La grille dépasse à droite! {grid_end_x} > {screen_w}"
    assert grid_end_y <= screen_h, f"❌ La grille dépasse en bas! {grid_end_y} > {screen_h}"
    print(f"✓ Grille ne dépasse pas (fin: {grid_end_x}x{grid_end_y}, écran: {screen_w}x{screen_h})")
    
    # TEST 2: Changement de résolution 1280x720
    print("\n[TEST 2] Update avec résolution 1280x720")
    print("-" * 70)
    ScreenVar.screen = pygame.display.set_mode((1280, 720))
    ScreenVar.update_scale()
    GridVar.update_grid()
    
    old_cell_size = GridVar.cell_size
    assert GridVar.cell_size > 0, "❌ cell_size devrait être > 0"
    
    screen_w, screen_h = ScreenVar.screen.get_size()
    grid_end_x = GridVar.offset_x + GridVar.grid_width
    grid_end_y = GridVar.offset_y + GridVar.grid_height
    
    assert grid_end_x <= screen_w, f"❌ La grille dépasse à droite! {grid_end_x} > {screen_w}"
    assert grid_end_y <= screen_h, f"❌ La grille dépasse en bas! {grid_end_y} > {screen_h}"
    
    print(f"✓ Nouvelle taille cellule: {GridVar.cell_size}px (avant: {old_cell_size}px)")
    print(f"✓ Dimensions grille: {GridVar.grid_width}x{GridVar.grid_height}px")
    print(f"✓ Offsets: X={GridVar.offset_x}px, Y={GridVar.offset_y}px")
    print(f"✓ Grille ne dépasse pas (fin: {grid_end_x}x{grid_end_y}, écran: {screen_w}x{screen_h})")
    
    # TEST 3: Petite résolution 800x600
    print("\n[TEST 3] Update avec petite résolution 800x600")
    print("-" * 70)
    ScreenVar.screen = pygame.display.set_mode((800, 600))
    ScreenVar.update_scale()
    GridVar.update_grid()
    
    screen_w, screen_h = ScreenVar.screen.get_size()
    grid_end_x = GridVar.offset_x + GridVar.grid_width
    grid_end_y = GridVar.offset_y + GridVar.grid_height
    
    assert GridVar.cell_size > 0, "❌ cell_size devrait être > 0"
    assert grid_end_x <= screen_w, f"❌ La grille dépasse à droite! {grid_end_x} > {screen_w}"
    assert grid_end_y <= screen_h, f"❌ La grille dépasse en bas! {grid_end_y} > {screen_h}"
    
    print(f"✓ Taille cellule: {GridVar.cell_size}px")
    print(f"✓ Dimensions grille: {GridVar.grid_width}x{GridVar.grid_height}px")
    print(f"✓ Grille ne dépasse pas (fin: {grid_end_x}x{grid_end_y}, écran: {screen_w}x{screen_h})")
    
    # TEST 4: Grande résolution 2560x1440
    print("\n[TEST 4] Update avec grande résolution 2560x1440")
    print("-" * 70)
    ScreenVar.screen = pygame.display.set_mode((2560, 1440))
    ScreenVar.update_scale()
    GridVar.update_grid()
    
    screen_w, screen_h = ScreenVar.screen.get_size()
    grid_end_x = GridVar.offset_x + GridVar.grid_width
    grid_end_y = GridVar.offset_y + GridVar.grid_height
    
    assert GridVar.cell_size > 0, "❌ cell_size devrait être > 0"
    assert grid_end_x <= screen_w, f"❌ La grille dépasse à droite! {grid_end_x} > {screen_w}"
    assert grid_end_y <= screen_h, f"❌ La grille dépasse en bas! {grid_end_y} > {screen_h}"
    
    print(f"✓ Taille cellule: {GridVar.cell_size}px")
    print(f"✓ Dimensions grille: {GridVar.grid_width}x{GridVar.grid_height}px")
    print(f"✓ Grille ne dépasse pas (fin: {grid_end_x}x{grid_end_y}, écran: {screen_w}x{screen_h})")
    
    # TEST 5: Grille de taille différente (20x20)
    print("\n[TEST 5] Nouvelle grille 20x20 cellules")
    print("-" * 70)
    GridVar(20, 20)
    
    assert GridVar.nb_cells_x == 20, "❌ nb_cells_x devrait être 20"
    assert GridVar.nb_cells_y == 20, "❌ nb_cells_y devrait être 20"
    assert GridVar.grid_width == 20 * GridVar.cell_size, "❌ grid_width mal calculé"
    assert GridVar.grid_height == 20 * GridVar.cell_size, "❌ grid_height mal calculé"
    
    screen_w, screen_h = ScreenVar.screen.get_size()
    grid_end_x = GridVar.offset_x + GridVar.grid_width
    grid_end_y = GridVar.offset_y + GridVar.grid_height
    
    assert grid_end_x <= screen_w, f"❌ La grille dépasse à droite!"
    assert grid_end_y <= screen_h, f"❌ La grille dépasse en bas!"
    
    print(f"✓ Cellules: {GridVar.nb_cells_x}x{GridVar.nb_cells_y}")
    print(f"✓ Taille cellule: {GridVar.cell_size}px")
    print(f"✓ Dimensions grille: {GridVar.grid_width}x{GridVar.grid_height}px")
    print(f"✓ Grille ne dépasse pas")
    
    # TEST 6: Centrage de la grille
    print("\n[TEST 6] Vérification du centrage")
    print("-" * 70)
    
    space_left = GridVar.offset_x
    space_right = screen_w - grid_end_x
    space_top = GridVar.offset_y
    space_bottom = screen_h - grid_end_y
    
    print(f"Espaces - Gauche: {space_left}px, Droite: {space_right}px")
    print(f"         Haut: {space_top}px, Bas: {space_bottom}px")
    
    # Le centrage doit être symétrique (avec tolérance de 1px)
    if space_left >= GridVar.min_offset_x and space_right >= GridVar.min_offset_x:
        assert abs(space_left - space_right) <= 1, "❌ Centrage horizontal incorrect"
        print("✓ Grille centrée horizontalement")
    else:
        print("✓ Grille utilise l'offset minimum (trop grande pour centrer)")
    
    if space_top >= GridVar.min_offset_y and space_bottom >= GridVar.min_offset_y:
        assert abs(space_top - space_bottom) <= 1, "❌ Centrage vertical incorrect"
        print("✓ Grille centrée verticalement")
    else:
        print("✓ Grille utilise l'offset minimum (trop grande pour centrer)")
    
    pygame.quit()
    
    print("\n" + "="*70)
    print("✅ TOUS LES TESTS SONT PASSÉS!")
    print("="*70)


if __name__ == "__main__":
    test_grid_var()