from setting import *
from player import *
from sprites import *
from groups import *

class Game:
    def __init__(self):
        # set up
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Of Life")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision = pygame.sprite.Group()

        # sprite
        self.test_object = pygame.Surface((50, 50))
        self.test_object.fill("black")
        self.test = CollisionSprite((500, 600), self.test_object, (self.all_sprites, self.collision))
        self.player = Player((WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2), self.all_sprites, self.collision)

    def setup(self):
        pass

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick(FPS) / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill("#676767")
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()