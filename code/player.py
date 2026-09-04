from setting import *
import os

os.chdir(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # fix import path by changing working directory to project root


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down", "0.png"))
        self.rect = self.image.get_frect(center=pos)
    