from PIL import Image, ImageSequence

def gif_to_spritesheet(gif_path, output_path, rows=None, cols=None):
    """
    Convertit un fichier GIF en une spritesheet.

    Le GIF est chargé et toutes les frames sont extraites.
    Les frames sont ensuite collées dans une grille qui est sauvegardée
    dans le fichier output_path.

    :param gif_path: Chemin du fichier GIF
    :param output_path: Chemin du fichier de sortie
    :param rows: Nombre de lignes dans la grille (défaut = None)
    :param cols: Nombre de colonnes dans la grille (défaut = None)
    """
    # Charger le GIF
    gif = Image.open(gif_path)

    # Extraire toutes les frames
    frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(gif)]
    frame_width, frame_height = frames[0].size
    num_frames = len(frames)

    # Si pas de grille imposée -> une seule ligne
    if not cols:
        cols = num_frames
    if not rows:
        rows = (num_frames + cols - 1) // cols

    # Créer la spritesheet
    sheet_width = cols * frame_width
    sheet_height = rows * frame_height
    spritesheet = Image.new("RGBA", (sheet_width, sheet_height))

    # Coller chaque frame dans la grille
    for i, frame in enumerate(frames):
        x = (i % cols) * frame_width
        y = (i // cols) * frame_height
        spritesheet.paste(frame, (x, y))

    # Sauvegarder
    spritesheet.save(output_path)
    print(f"Spritesheet sauvegardée dans {output_path}")
