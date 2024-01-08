import random
import pygame

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
MINT = (64, 224, 208)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def gen(num):
    positions = []
    for _ in range(num):
        positions.append((random.randrange(0, GRID_HEIGHT),
                         random.randrange(0, GRID_WIDTH)))
    return set(positions)


def draw_grid(positions):
    for position in positions:
        pygame.draw.rect(
            screen, MINT, (position[0] * TILE_SIZE, position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    horizontal_lines = [((0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
                        for row in range(GRID_HEIGHT)]
    vertical_lines = [((col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
                      for col in range(GRID_WIDTH)]

    for start, end in horizontal_lines + vertical_lines:
        pygame.draw.line(screen, BLACK, start, end)


def adjust_grid(positions):
    new_positions = positions.copy()
    to_check = positions | set().union(*[get_neighbors(p) for p in positions])

    for position in to_check:
        neighbors = get_neighbors(position)
        alive_neighbors = len([n for n in neighbors if n in positions])

        if position in positions:
            if alive_neighbors not in [2, 3]:
                new_positions.discard(position)
        else:
            if alive_neighbors == 3:
                new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx, dy) != (0, 0) and 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT:
                neighbors.append((x + dx, y + dy))
    return neighbors


def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
            if count >= update_freq:
                count = 0
                positions = adjust_grid(positions)

        pygame.display.set_caption('Playing' if playing else 'Paused')

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    pos = (x // TILE_SIZE, y // TILE_SIZE)
                    positions ^= {pos}
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_SPACE:
                            playing = not playing
                        case pygame.K_c:
                            positions = set()
                            playing = False
                            count = 0
                        case pygame.K_g:
                            positions |= gen(random.randint(4, 9) * GRID_WIDTH)

        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
