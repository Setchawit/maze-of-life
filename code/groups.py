from setting import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, targetpos): # camera follow player  
        self.offset.x = -(targetpos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(targetpos[1] - WINDOW_HEIGHT / 2)

        ground_layer = [sprite for sprite in self if hasattr(sprite, "ground")]
        object_layer = [sprite for sprite in self if not hasattr(sprite, "ground")]

        for layer in [ground_layer, object_layer]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)