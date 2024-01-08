import random
import pygame

# Initialize the Pygame library
pygame.init()

# Define common color constants
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

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
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE),
                         (WIDTH, row * TILE_SIZE))

        for col in range(GRID_WIDTH):
            pygame.draw.line(screen, BLACK, (col * TILE_SIZE,
                             0), (col * TILE_SIZE, HEIGHT))

# Function to adjust the grid based on the game rules


def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        # Filter the neighbors to include only those in positions
        neighbors = list(filter(lambda x: x in positions, neighbors))

        # Rules to maintain current position
        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    # Check all neighboring positions
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        # Rule for empty position to become filled
        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions

# Function to get the neighbors of a particular position


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if 0 <= x + dx < GRID_WIDTH:
            for dy in [-1, 0, 1]:
                if 0 <= y + dy < GRID_HEIGHT:
                    if not (dx == 0 and dy == 0):
                        neighbors.append((x + dx, y + dy))
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

        # Update the count if the game is in playing mode
        if playing:
            count += 1

        # Update the game state based on count and playing state
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        # Set the window title based on the game state
        pygame.display.set_caption('Playing' if playing else 'Paused')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                # Toggle the position in the set upon mouse click
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                # Toggle playing state with the space key
                if event.key == pygame.K_SPACE:
                    playing = not playing

                # Clear the grid and pause game with 'c' key
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                # Generate random positions with 'g' key
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)

        # Draw the background and grid
        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()


# Entry point of the script
if __name__ == '__main__':
    main()
