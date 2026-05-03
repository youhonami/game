import random
from dataclasses import dataclass
from pathlib import Path

import pygame


WIDTH = 800
HEIGHT = 600
FPS = 60
SIDEBAR_WIDTH = 260
BACKGROUND_IMAGE_PATH = Path(
    "/Users/honamiyuusuke/.cursor/projects/"
    "Users-honamiyuusuke-coachtech-game/assets/"
    "_______-5e35f2db-48bd-48a4-ae7b-476c8cda2f70.png"
)

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
BLUE = (80, 160, 255)
GREEN = (80, 220, 140)
RED = (240, 90, 90)
YELLOW = (245, 210, 90)
CYAN = (120, 225, 255)


@dataclass
class AppContext:
    screen: pygame.Surface
    clock: pygame.time.Clock
    font: pygame.font.Font
    small_font: pygame.font.Font
    background: pygame.Surface | None


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


def load_background() -> pygame.Surface | None:
    if not BACKGROUND_IMAGE_PATH.exists():
        return None

    image = pygame.image.load(str(BACKGROUND_IMAGE_PATH)).convert()
    return pygame.transform.smoothscale(image, (WIDTH, HEIGHT))


def create_font(size: int) -> pygame.font.Font:
    for font_name in ("hiraginosansgb", "applesdgothicneo", "applegothic", "stheitimedium"):
        font_path = pygame.font.match_font(font_name)
        if font_path is not None:
            return pygame.font.Font(font_path, size)

    return pygame.font.Font(None, size)


def show_menu(ctx: AppContext) -> str | None:
    menu_items = [
        ("1", "テトリス", "tetris"),
        ("2", "シューティング", "shooting"),
    ]
    item_rects = [
        pygame.Rect(30, 190 + index * 80, SIDEBAR_WIDTH - 60, 56)
        for index in range(len(menu_items))
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_1:
                    return "tetris"
                if event.key == pygame.K_2:
                    return "shooting"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, (_, _, game_id) in zip(item_rects, menu_items):
                    if rect.collidepoint(event.pos):
                        return game_id

        if ctx.background is not None:
            ctx.screen.blit(ctx.background, (0, 0))
        else:
            ctx.screen.fill(BLACK)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 20, 45, 70))
        pygame.draw.rect(overlay, (5, 18, 35, 215), (0, 0, SIDEBAR_WIDTH, HEIGHT))
        pygame.draw.line(overlay, (120, 225, 255, 130), (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, HEIGHT), 2)
        ctx.screen.blit(overlay, (0, 0))

        draw_text(ctx.screen, ctx.small_font, "Game Menu", WHITE, (SIDEBAR_WIDTH // 2, 80))
        draw_text(ctx.screen, ctx.font, "Ocean Game Hub", WHITE, (530, 165))
        draw_text(ctx.screen, ctx.small_font, "サイドバーからゲームを選択", CYAN, (530, 240))

        for rect, (shortcut, label, _) in zip(item_rects, menu_items):
            is_hovered = rect.collidepoint(mouse_pos)
            button_color = (30, 125, 170) if is_hovered else (15, 65, 105)
            pygame.draw.rect(ctx.screen, button_color, rect, border_radius=12)
            pygame.draw.rect(ctx.screen, CYAN, rect, width=2, border_radius=12)
            draw_text(
                ctx.screen,
                ctx.small_font,
                f"{shortcut}. {label}",
                WHITE,
                rect.center,
            )

        draw_text(ctx.screen, ctx.small_font, "Esc: 終了", WHITE, (SIDEBAR_WIDTH // 2, 520))
        pygame.display.flip()
        ctx.clock.tick(FPS)


def show_coming_soon(ctx: AppContext, title: str) -> None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        if ctx.background is not None:
            ctx.screen.blit(ctx.background, (0, 0))
        else:
            ctx.screen.fill(BLACK)

        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 145))
        ctx.screen.blit(veil, (0, 0))
        draw_text(ctx.screen, ctx.font, title, WHITE, (WIDTH // 2, 240))
        draw_text(ctx.screen, ctx.small_font, "準備中です", CYAN, (WIDTH // 2, 320))
        draw_text(ctx.screen, ctx.small_font, "Esc: メニューに戻る", WHITE, (WIDTH // 2, 410))
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
            font=create_font(64),
            small_font=create_font(34),
            background=load_background(),
        )

        while True:
            selected_game = show_menu(ctx)
            if selected_game is None:
                break
            if selected_game == "tetris":
                show_coming_soon(ctx, "テトリス")
            elif selected_game == "shooting":
                show_coming_soon(ctx, "シューティング")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
