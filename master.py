import random
import pygame

# Initialize the Pygame library
pygame.init()

# Define common color constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
MINT = (64, 224, 208)

# Screen dimensions and properties
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize clock for controlling frame rate
clock = pygame.time.Clock()

# Function to generate a set of positions


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

# Function to draw the grid and filled squares


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

# Function to adjust the grid based on the game rules


def adjust_grid(positions):
    new_positions = positions.copy()

    # Positions that need to be checked
    to_check = positions.union(*[get_neighbors(p) for p in positions])

    # Check each position, and apply the rules
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

# Function to get the neighbors of a particular position


def get_neighbors(pos):
    x, y = pos
    neighbors = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy)
                 != (0, 0) and 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT]
    return neighbors
# Main function where the game loop resides


def main():
    # Game state variables
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
                    positions ^= {pos}  # Toggle using symmetric difference
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


# Entry point of the script
if __name__ == '__main__':
    main()
