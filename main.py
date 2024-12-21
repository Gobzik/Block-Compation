import pygame
import sys
import random

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Company")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 123, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 200, 150)
DARK_BLUE = (10, 10, 80)
LIGHT_BLUE = (48, 163, 230)

font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, icon=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.icon = icon

    def draw(self, screen, mouse_pos):
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=15)

        if self.icon:
            icon_rect = self.icon.get_rect(midleft=(self.rect.left + 20, self.rect.centery))
            screen.blit(self.icon, icon_rect)

        text_surface = font_medium.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed


clock_icon = pygame.image.load("clock_icon.png")
clock_icon = pygame.transform.scale(clock_icon, (40, 40))
infinity_icon = pygame.image.load("infinity_icon.png")
infinity_icon = pygame.transform.scale(infinity_icon, (40, 40))

buttons = [
    Button("Adventure", SCREEN_WIDTH // 2 - 150, 300, 300, 70, ORANGE, (255, 200, 100), icon=clock_icon),
    Button("Classic", SCREEN_WIDTH // 2 - 150, 400, 300, 70, GREEN, (100, 255, 200), icon=infinity_icon),
]


class Snowflake:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-SCREEN_HEIGHT, 0)
        self.size = random.randint(2, 5)
        self.speed = random.randint(10, 30) / FPS

    def fall(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)


snowflakes = [Snowflake() for _ in range(150)]


def draw_gradient_background(screen, top_color, bottom_color):
    for y in range(SCREEN_HEIGHT):
        color = [
            top_color[i] + (bottom_color[i] - top_color[i]) * y // SCREEN_HEIGHT
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))


def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        draw_gradient_background(screen, DARK_BLUE, LIGHT_BLUE)

        for snowflake in snowflakes:
            snowflake.fall()
            snowflake.draw(screen)

        title_surface = font_large.render("BLOCK COMP", True, RED)
        subtitle_surface = font_small.render("Gobziii", True, WHITE)
        screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for button in buttons:
            button.draw(screen, mouse_pos)
            if button.is_clicked(mouse_pos, mouse_pressed):
                if button.text == "Adventure":
                    print("Start Adventure mode")
                elif button.text == "Classic":
                    print("Start Classic mode")
        pygame.display.flip()


if __name__ == "__main__":
    main()
