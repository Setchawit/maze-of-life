from setting import *
from player import *
from sprites import *
from groups import *

from pytmx.util_pygame import load_pygame
from random import choice

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
        self.player_sprite = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.notcollision_sprites = pygame.sprite.Group()
        self.weapon_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.warp_sprites = pygame.sprite.Group()
        self.text_sprites = pygame.sprite.Group()

        # weapon
        self.weapon_show_time = 0
        self.weapon_show = False
        self.weapon_cooldown = 1000

        # curser
        self.curser_show = True
        self.curser_cooldown = 400

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []
        self.kill_enemy = False
        self.goal_reached = 0

        # warp
        self.warp_cooldown = 5000
        self.warp_time = 0

        # text
        self.stop = False

        self.load_images()
        self.load_musics()
        self.setup()

        # sprite

    def load_images(self):
        self.curser_surf = pygame.image.load(join("images", "tools", "curser", "curser.png")).convert_alpha()
        self.sword_surf = pygame.image.load(join("images", "tools", "weapon", "sword.png")).convert_alpha()
        self.item_surf = pygame.Surface((50, 50))
        self.item_surf.fill("black")
        self.font = pygame.font.Font(join("images", "text", "ComicNeueSansID.ttf"), 20)

        folders = list(walk(join("images", "enemies")))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join("images", "enemies", folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def load_musics(self):
        self.game_music = pygame.mixer.Sound(join("audio", "music.wav"))
        self.game_music.set_volume(0.05)
        self.game_music.play(loops=-1)
        self.damage_sound = pygame.mixer.Sound(join("audio", "damage.ogg"))
        self.damage_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound(join("audio", "impact.ogg"))
        self.hit_sound.set_volume(0.1)

    def load_texts(self):
        if self.goal_reached == 1 and not self.stop:
            self.text = Text(self.font, self.player, self.goal_reached,  (self.all_sprites, self.text_sprites))
            self.stop = True
        if self.goal_reached == 0 and self.stop:
            self.stop = False
            for text in self.text_sprites:
                text.kill()

    def input(self):
        if self.curser_show:
            self.curser = Curser(self.curser_surf, self.player, self.all_sprites)

        if pygame.mouse.get_just_pressed()[0] and self.weapon_show:
            self.curser_show = False
            Weapon(self.sword_surf, self.player, (self.all_sprites, self.weapon_sprites))
            self.weapon_show = False
            self.weapon_show_time = pygame.time.get_ticks()

        if self.goal_reached > 0:
            self.text.score = self.goal_reached

    def weapon_timer(self):
        if not self.weapon_show:
            current_time = pygame.time.get_ticks()
            if current_time - self.weapon_show_time >= self.weapon_cooldown:
                self.weapon_show = True
            if current_time - self.weapon_show_time >= self.curser_cooldown:
                self.curser_show = True

    def reload_game(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "kill":
                self.item = Items((obj.x, obj.y), self.item_surf, (self.all_sprites, self.item_sprites))
        for enemy in self.enemy_sprites:
            enemy.kill()

    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))

        for x, y ,image in map.get_layer_by_name("Ground").tiles():
            GroundSprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name("Objects"):
            if obj.name == "tree":
                TreeSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.notcollision_sprites))
            else:
                CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name("Collisions"):
            GroundSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), (self.all_sprites, self.player_sprite), self.collision_sprites)
                self.start_point_x = obj.x
                self.start_point_y = obj.y
            if obj.name == "Enemy":
                self.spawn_positions.append((obj.x, obj.y))
            if obj.name == "kill":
                self.item = Items((obj.x, obj.y), self.item_surf, (self.all_sprites, self.item_sprites))
            if obj.name == "Goal":
                self.goal = Items((obj.x, obj.y), self.item_surf, (self.all_sprites, self.warp_sprites))

            if obj.name == "Warp1":
                self.warp1 = Warp((obj.x, obj.y), self.item_surf, (self.all_sprites, self.warp_sprites))
            if obj.name == "Warp2":
                self.warp2 = Warp((obj.x, obj.y), self.item_surf, (self.all_sprites, self.warp_sprites))
            if obj.name == "Warp3":
                self.warp3 = Warp((obj.x, obj.y), self.item_surf, (self.all_sprites, self.warp_sprites))
            if obj.name == "Warp4":
                self.warp4 = Warp((obj.x, obj.y), self.item_surf, (self.all_sprites, self.warp_sprites))

            if obj.name == "Warp1e":
                self.warp1e_x = obj.x
                self.warp1e_y = obj.y
            if obj.name == "Warp2e":
                self.warp2e_x = obj.x
                self.warp2e_y = obj.y
            if obj.name == "Warp3e":
                self.warp3e_x = obj.x
                self.warp3e_y = obj.y
            if obj.name == "Warp4e":
                self.warp4e_x = obj.x
                self.warp4e_y = obj.y

    def enemy_collision(self):
        for player in self.player_sprite:
            if pygame.sprite.spritecollide(player, self.enemy_sprites, False, pygame.sprite.collide_mask):
                self.player.collision_hitbox_rect.x = self.start_point_x
                self.player.collision_hitbox_rect.y = self.start_point_y
                self.goal_reached = 0
                self.reload_game()

    def weapon_collision(self):
        for weapon in self.weapon_sprites:
            if pygame.sprite.spritecollide(weapon, self.enemy_sprites, True):
                self.hit_sound.play()

    def item_collision(self):
        for player in self.player_sprite:
            if pygame.sprite.spritecollide(player, self.item_sprites, True):
               for enemy in self.enemy_sprites:
                   self.hit_sound.play()
                   enemy.kill()

    def warp_collision(self):
        if pygame.time.get_ticks() - self.warp_time >= self.warp_cooldown:
            if pygame.sprite.collide_rect(self.player, self.warp1):
                self.player.collision_hitbox_rect.x = self.warp1e_x
                self.player.collision_hitbox_rect.y = self.warp1e_y
                self.warp_time = pygame.time.get_ticks()

            if pygame.sprite.collide_rect(self.player, self.warp2):
                self.player.collision_hitbox_rect.x = self.warp2e_x
                self.player.collision_hitbox_rect.y = self.warp2e_y
                self.warp_time = pygame.time.get_ticks()

            if pygame.sprite.collide_rect(self.player, self.warp3):
                self.player.collision_hitbox_rect.x = self.warp3e_x
                self.player.collision_hitbox_rect.y = self.warp3e_y
                self.warp_time = pygame.time.get_ticks()

            if pygame.sprite.collide_rect(self.player, self.warp4):
                self.player.collision_hitbox_rect.x = self.warp4e_x
                self.player.collision_hitbox_rect.y = self.warp4e_y
                self.warp_time = pygame.time.get_ticks()

    def goal_collision(self):
            if pygame.sprite.collide_rect(self.player, self.goal):
                self.player.collision_hitbox_rect.x = self.start_point_x
                self.player.collision_hitbox_rect.y = self.start_point_y
                self.goal_reached += 1
                self.reload_game()

    def collisions(self):
        self.weapon_collision()
        self.warp_collision()
        self.item_collision()
        self.goal_collision()
        self.enemy_collision()

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick(FPS) / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    self.enemy = Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player)

            # update
            self.load_texts()
            self.weapon_timer()
            self.input()
            self.all_sprites.update(dt)
            self.collisions()

            # draw
            self.display_surface.fill("#676767")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()