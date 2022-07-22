from typing import Tuple
import random
from dataclasses import dataclass
import pygame


Num = int | float
Color = Tuple[int, int, int]

BLACK: Color = (0, 0, 0)
WHITE: Color = (255, 255, 255)
RED: Color = (255, 0, 0)
GREEN: Color = (0, 255, 0)
BLUE: Color = (0, 0, 255)

COLORS: list[Color] = [WHITE, RED, GREEN, BLUE]

WIN_RES: Tuple[int, int] = (1280, 720)

HEIGHT: int
WIDTH: int
WIDTH, HEIGHT = WIN_RES

FPS: int = 30

STAR_AMOUNT: int = 500

@dataclass
class Star:
    y: int = 0
    x: int = 0
    z: int = random.randint(1, WIDTH // 2)
    pz: int = z
    ps: float = 0

    def draw(self, window: pygame.surface.Surface, color: Color) -> None:
            size: float = translate(self.z, (0, WIDTH), (8, 1))
            sx: float = translate(self.x / self.z, (0, 1), (0, WIDTH // 2))
            sy: float = translate(self.y / self.z, (0, 1), (0, HEIGHT // 2))
            px: float = translate(self.x / self.pz, (0, 1), (0, WIDTH // 2))
            py: float = translate(self.y / self.pz, (0, 1), (0, HEIGHT // 2))
            pygame.draw.circle(window, color, (sx + WIDTH / 2, sy + HEIGHT / 2), size)
            pygame.draw.line(window, color,(px + WIDTH / 2, py + HEIGHT / 2), (sx + WIDTH / 2, sy + HEIGHT / 2), int(size))

    def renew(self) -> None:
        self.x = random.randint(-WIDTH // 2, WIDTH // 2)
        self.y = random.randint(-HEIGHT // 2, HEIGHT // 2)
        self.z = random.randint(1, WIDTH)
        self.pz = self.z

    def update(self, speed: int) -> None:
        self.pz = self.z
        self.z += -speed
        if self.z < 1:
            self.renew()
        
def translate(value: Num, tranlation_range_input: Tuple[Num, Num], translation_range_output: Tuple[Num, Num]) -> float:
    i_min: Num
    i_max: Num
    i_min, i_max = tranlation_range_input

    o_min: Num
    o_max: Num
    o_min, o_max = translation_range_output

    i_range: Num = i_max - i_min
    o_range: Num = o_max - o_min

    return (((value - i_min) * o_range) / i_range) + o_min


def main() -> None:
    pygame.init()
    pygame.display.set_caption("PyGame Experiment #1: Starfield")

    clock: pygame.time.Clock = pygame.time.Clock()

    running: bool = True


    window: pygame.surface.Surface = pygame.display.set_mode(WIN_RES)


    stars: list[Star] = [
        Star(
            y=random.randint(-HEIGHT // 2, HEIGHT // 2), 
            x=random.randint(-WIDTH // 2, WIDTH // 2), 
            z=random.randint(1, WIDTH)
            )
        for _ in range(STAR_AMOUNT)
    ]

    while running:
        window.fill(BLACK)
        event: pygame.event.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        speed: int = sum(pygame.mouse.get_pos())

        star: Star
        for star in stars:
            star.draw(window, WHITE)
            star.update(int(translate(speed, (0, HEIGHT + WIDTH), (5, 100))))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()