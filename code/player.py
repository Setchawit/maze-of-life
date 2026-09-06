from setting import *
import os

os.chdir(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # fix import path by changing working directory to project root

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frames_index = "down", 0
        self.image = pygame.image.load(join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.collision_hitbox_rect = self.rect.inflate(-60, -90)

        # set up
        self.speed = 670
        self.direction = pygame.math.Vector2()
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

        self.direction = (self.direction.normalize() if self.direction else self.direction) # speed normalization

        
    def move(self, dt):
        self.collision_hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.collision_hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.collision_hitbox_rect.center


    def load_images(self):
        self.frames = {"down" : [], "left" : [], "right" : [], "up" : []}

        for state in self.frames.keys():
                for folder_path, sub_folders, file_names in walk(join("images", "player", state)):
                    for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])): # sort proof
                        full_path = join(folder_path, file_name)
                        load_frames = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(load_frames)

    def collision(self, direction):
        for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.collision_hitbox_rect):
                    if direction == "vertical":
                        if self.direction.y < 0 : 
                            self.collision_hitbox_rect.top = sprite.rect.bottom
                        if self.direction.y > 0 : 
                            self.collision_hitbox_rect.bottom = sprite.rect.top
                    else:
                        if self.direction.x > 0 : self.collision_hitbox_rect.right = sprite.rect.left
                        if self.direction.x < 0 : self.collision_hitbox_rect.left = sprite.rect.right


    def animate(self, dt):
        # get state
        if self.direction.y != 0:
            self.state = "up" if self.direction.y < 0 else "down"
        if self.direction.x != 0:
            self.state = "left" if self.direction.x < 0 else "right"

        # animate
        self.frames_index = self.frames_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frames_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
    