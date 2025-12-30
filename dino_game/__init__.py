import random
from pathlib import Path

import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_SPACE, QUIT, RLEACCEL

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
GROUND_Y = 390
BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
ASSET_DIR = Path(__file__).resolve().parent.parent / "images"

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run")


def load_image(name):
    return pygame.image.load(str(ASSET_DIR / name)).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.start_pos = (50, 363)
        self.surf = load_image("dino0.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center=self.start_pos)
        self.jump_count = 12
        self.is_jump = False

    def update(self, pressed_keys):
        if not self.is_jump:
            if pressed_keys[K_SPACE]:
                self.is_jump = True
        else:
            if self.jump_count >= -12:
                neg = 1 if self.jump_count >= 0 else -1
                self.rect.centery -= (self.jump_count ** 2) * 0.1 * neg
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 12


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = load_image("1x-horizon.png")
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, GROUND_Y))


class Cloud(pygame.sprite.Sprite):
    def __init__(self, speed=1):
        super().__init__()
        self.surf = load_image("1x-cloud.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 30, SCREEN_WIDTH + 120),
                random.randint(20, SCREEN_HEIGHT // 3),
            )
        )
        self.speed = speed

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < -50:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.surf = load_image("obs1.png")
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH + 20, 363))
        self.speed = speed

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < -20:
            self.kill()


class Game:
    ADD_ENEMY = pygame.USEREVENT + 1
    ADD_CLOUD = pygame.USEREVENT + 2

    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 28)
        self.big_font = pygame.font.Font("freesansbold.ttf", 48)
        self.enemy_interval = 1200
        self.cloud_interval = 3200
        self.running = True
        self.reset()

    def reset(self):
        self.score = 0
        self.active = True
        self.player = Player()
        self.ground = Ground()

        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.ground, self.player)

        for _ in range(2):
            self.spawn_cloud()

        pygame.time.set_timer(self.ADD_ENEMY, self.enemy_interval)
        pygame.time.set_timer(self.ADD_CLOUD, self.cloud_interval)

    def spawn_enemy(self):
        speed = random.randint(4, 7) + int(self.score // 250)
        speed = min(speed, 14)
        enemy = Enemy(speed)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def spawn_cloud(self):
        cloud = Cloud()
        self.clouds.add(cloud)
        self.all_sprites.add(cloud)

    def update_difficulty(self):
        target_interval = max(650, int(1200 - self.score * 0.2))
        if target_interval != self.enemy_interval:
            self.enemy_interval = target_interval
            pygame.time.set_timer(self.ADD_ENEMY, self.enemy_interval)

    def update_score(self, dt):
        self.score += dt * 100

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif not self.active and event.key == K_SPACE:
                    self.reset()

            if not self.active:
                continue

            if event.type == self.ADD_CLOUD:
                self.spawn_cloud()
            elif event.type == self.ADD_ENEMY:
                self.spawn_enemy()

    def update_gameplay(self, pressed_keys, dt):
        self.player.update(pressed_keys)
        self.enemies.update()
        self.clouds.update()
        self.update_score(dt)
        self.update_difficulty()

        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.active = False

    def draw(self):
        self.screen.fill(BG_COLOR)
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        score_surf = self.font.render(f"Score: {int(self.score)}", True, WHITE)
        self.screen.blit(score_surf, (20, 20))

        if not self.active:
            over_text = self.big_font.render("Game Over", True, WHITE)
            prompt = self.font.render("Press SPACE to restart", True, WHITE)
            over_rect = over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            )
            prompt_rect = prompt.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            )
            self.screen.blit(over_text, over_rect)
            self.screen.blit(prompt, prompt_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.handle_events()

            if self.active:
                pressed_keys = pygame.key.get_pressed()
                self.update_gameplay(pressed_keys, dt)

            self.draw()

        pygame.quit()


def main():
    Game().run()
