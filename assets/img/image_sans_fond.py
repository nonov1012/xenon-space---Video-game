from PIL import Image
import os

def remove_black_pixels(input_path, output_path=None, threshold=10):
    """
    Enlève tous les pixels noirs d'une image PNG en les rendant transparents.
    
    Args:
        input_path: Chemin vers l'image PNG d'entrée
        output_path: Chemin de sortie (optionnel, ajoute '_no_black' par défaut)
        threshold: Seuil pour considérer un pixel comme noir (0-255)
                   0 = strictement noir, 10 = proche du noir
    """
    # Ouvrir l'image
    img = Image.open(input_path)
    
    # Convertir en RGBA si ce n'est pas déjà le cas
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Récupérer les données de pixels
    pixels = img.load()
    width, height = img.size
    
    # Parcourir tous les pixels
    pixels_modified = 0
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Si le pixel est noir (ou proche du noir)
            if r <= threshold and g <= threshold and b <= threshold:
                # Le rendre transparent
                pixels[x, y] = (r, g, b, 0)
                pixels_modified += 1
    
    # Générer le nom de sortie si non fourni
    if output_path is None:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_no_black{ext}"
    
    # Sauvegarder l'image
    img.save(output_path, 'PNG')
    
    print(f"✓ Image traitée: {input_path}")
    print(f"✓ {pixels_modified} pixels noirs rendus transparents")
    print(f"✓ Sauvegardée: {output_path}")
    
    return output_path


def batch_remove_black_pixels(folder_path, threshold=10):
    """
    Traite tous les fichiers PNG d'un dossier.
    
    Args:
        folder_path: Chemin vers le dossier contenant les PNG
        threshold: Seuil pour considérer un pixel comme noir
    """
    processed = 0
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(folder_path, filename)
            try:
                remove_black_pixels(input_path, threshold=threshold)
                processed += 1
            except Exception as e:
                print(f"✗ Erreur avec {filename}: {e}")
    
    print(f"\n✓ {processed} images traitées au total")


# --- Utilisation ---
if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("  Suppression des pixels noirs dans les PNG")
    print("=" * 50)
    print()
    
    # Mode 1: Un seul fichier
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
        threshold = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
        
        if os.path.isfile(input_file):
            remove_black_pixels(input_file, threshold=threshold)
        elif os.path.isdir(input_file):
            batch_remove_black_pixels(input_file, threshold=threshold)
        else:
            print(f"✗ Fichier ou dossier introuvable: {input_file}")
    
    # Mode 2: Interface interactive
    else:
        print("1. Traiter un seul fichier")
        print("2. Traiter tous les PNG d'un dossier")
        print()
        choice = input("Votre choix (1 ou 2): ").strip()
        
        if choice == "1":
            input_file = input("Chemin du fichier PNG: ").strip()
            threshold = input("Seuil (0-255, défaut=10): ").strip()
            threshold = int(threshold) if threshold else 10
            
            if os.path.isfile(input_file):
                remove_black_pixels(input_file, threshold=threshold)
            else:
                print(f"✗ Fichier introuvable: {input_file}")
        
        elif choice == "2":
            folder = input("Chemin du dossier: ").strip()
            threshold = input("Seuil (0-255, défaut=10): ").strip()
            threshold = int(threshold) if threshold else 10
            
            if os.path.isdir(folder):
                batch_remove_black_pixels(folder, threshold=threshold)
            else:
                print(f"✗ Dossier introuvable: {folder}")
        
        else:
            print("✗ Choix invalide")
    
    print()
    print("=" * 50)