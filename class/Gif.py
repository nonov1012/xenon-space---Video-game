import pygame
from PIL import Image

def load_gif_as_frames(gif_path):
    """
    Charge un GIF et retourne une liste de surfaces Pygame correspondant à chaque frame.
    """
    frames = []
    pil_gif = Image.open(gif_path)

    try:
        while True:
            frame = pil_gif.convert("RGBA")  # RGBA pour garder la transparence
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            py_image = pygame.image.fromstring(data, size, mode)
            frames.append(py_image)
            pil_gif.seek(pil_gif.tell() + 1)  # passer à la frame suivante
    except EOFError:
        pass  # fin des frames

    return frames