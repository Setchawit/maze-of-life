from setting import *
from math import atan2, degrees

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class GroundSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True


class TreeSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Text(pygame.sprite.Sprite):
    def __init__(self, font, player, score, groups):
        # player connection
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(0, -1)

        # Sprite setup
        super(). __init__(groups)
        self.font = font
        self.score = score
        self.image = self.font.render(f"Goal Reached: {self.score}", True, 20)
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def update(self, _):
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        self.image = self.font.render(f"Goal Reached: {self.score}", True, 20)


class Curser(pygame.sprite.Sprite):
    def __init__(self, surf, player, groups):
        # player connection
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(1, 0)
        self.spawntime = pygame.time.get_ticks()
        self.lifetime = 100

        # Sprite setup
        super(). __init__(groups)
        self.image = surf
        self.curser_surf = self.image
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.mouse.get_pos()
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_curser(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 180
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.curser_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.curser_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, _):
        self.get_direction()
        self.rotate_curser()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        if pygame.mouse.get_just_pressed()[0]:
            self.kill()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, surf, player, groups):
        # player connection
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1, 0)
        self.spawntime = pygame.time.get_ticks()
        self.lifetime = 250

        # Sprite setup
        super(). __init__(groups)
        self.image = surf
        self.weapon_surf = self.image
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.mouse.get_pos()
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_weapon(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 180
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.weapon_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.weapon_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, True, False)
        
    def update(self, _):
        self.get_direction()
        self.rotate_weapon()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        if pygame.time.get_ticks() - self.spawntime >= self.lifetime:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, kill = False):
        super().__init__(groups)
        self.player = player
        self.frames, self.frames_index = frames, 0
        self.animation_speed = 6
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 150

    def move(self, dt):
        # get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        # update the rect position + collision
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index) % len(self.frames)]

    def update(self, dt):
        self.move(dt)
        self.animate(dt)


class Items(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)


class Warp(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)