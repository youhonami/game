import random
from dataclasses import dataclass

import pygame


WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
BLUE = (80, 160, 255)
GREEN = (80, 220, 140)
RED = (240, 90, 90)
YELLOW = (245, 210, 90)


@dataclass
class AppContext:
    screen: pygame.Surface
    clock: pygame.time.Clock
    font: pygame.font.Font
    small_font: pygame.font.Font


def draw_text(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    center: tuple[int, int],
) -> None:
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)


def show_menu(ctx: AppContext) -> str | None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_1:
                    return "dodge"
                if event.key == pygame.K_2:
                    return "target"

        ctx.screen.fill(BLACK)
        draw_text(ctx.screen, ctx.font, "Game Hub", WHITE, (WIDTH // 2, 150))
        draw_text(ctx.screen, ctx.small_font, "1: Dodge Game", BLUE, (WIDTH // 2, 260))
        draw_text(ctx.screen, ctx.small_font, "2: Click Target", GREEN, (WIDTH // 2, 320))
        draw_text(ctx.screen, ctx.small_font, "Esc: Quit", WHITE, (WIDTH // 2, 420))
        pygame.display.flip()
        ctx.clock.tick(FPS)


def run_dodge_game(ctx: AppContext) -> None:
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)
    blocks: list[pygame.Rect] = []
    score = 0
    spawn_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 6
        if keys[pygame.K_RIGHT]:
            player.x += 6
        if keys[pygame.K_UP]:
            player.y -= 6
        if keys[pygame.K_DOWN]:
            player.y += 6
        player.clamp_ip(ctx.screen.get_rect())

        spawn_timer += 1
        if spawn_timer >= 30:
            spawn_timer = 0
            blocks.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40))

        for block in blocks:
            block.y += 5
        blocks = [block for block in blocks if block.y < HEIGHT]
        score += 1

        if any(player.colliderect(block) for block in blocks):
            return

        ctx.screen.fill(BLACK)
        pygame.draw.rect(ctx.screen, BLUE, player)
        for block in blocks:
            pygame.draw.rect(ctx.screen, RED, block)
        draw_text(ctx.screen, ctx.small_font, f"Score: {score}", WHITE, (90, 30))
        draw_text(ctx.screen, ctx.small_font, "Esc: Menu", WHITE, (700, 30))
        pygame.display.flip()
        ctx.clock.tick(FPS)


def run_click_target(ctx: AppContext) -> None:
    target = pygame.Rect(0, 0, 60, 60)
    target.center = (random.randint(80, WIDTH - 80), random.randint(100, HEIGHT - 80))
    score = 0
    time_left = FPS * 20

    while time_left > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and target.collidepoint(event.pos):
                score += 1
                target.center = (
                    random.randint(80, WIDTH - 80),
                    random.randint(100, HEIGHT - 80),
                )

        time_left -= 1
        seconds = time_left // FPS

        ctx.screen.fill(BLACK)
        pygame.draw.ellipse(ctx.screen, YELLOW, target)
        draw_text(ctx.screen, ctx.small_font, f"Score: {score}", WHITE, (90, 30))
        draw_text(ctx.screen, ctx.small_font, f"Time: {seconds}", WHITE, (WIDTH // 2, 30))
        draw_text(ctx.screen, ctx.small_font, "Esc: Menu", WHITE, (700, 30))
        pygame.display.flip()
        ctx.clock.tick(FPS)


def main() -> None:
    pygame.init()
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Hub")
        ctx = AppContext(
            screen=screen,
            clock=pygame.time.Clock(),
            font=pygame.font.Font(None, 72),
            small_font=pygame.font.Font(None, 40),
        )

        while True:
            selected_game = show_menu(ctx)
            if selected_game is None:
                break
            if selected_game == "dodge":
                run_dodge_game(ctx)
            elif selected_game == "target":
                run_click_target(ctx)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
