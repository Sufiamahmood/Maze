import pygame
import random
import time

# Initializes Pygame
pygame.init()

# Screen dimensions
width, height = 650, 650
cols, rows = 21, 21
cell_size = width // cols
player_x, player_y = 1, 1
exit_x, exit_y = cols - 2, rows - 2

# Sets up display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Navigation Game")

# Colors
WHITE = (255, 255, 255)
LILAC = (164, 91, 170)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Loads the character image
try:
    character_image = pygame.image.load("C:/Projects/Character01.png")
    character_image = pygame.transform.scale(character_image, (cell_size, cell_size))
except pygame.error as e:
    print(f"Unable to load character image: {e}")
    pygame.quit()
    exit()

# Initializes the maze grid
maze = [[0 for _ in range(cols)] for _ in range(rows)]

# Initializes score
score = 0

def is_valid_move(x, y):
    return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

def carve_passages_from(current_x, current_y):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    random.shuffle(directions)
    for direction in directions:
        new_x = current_x + direction[0] * 2
        new_y = current_y + direction[1] * 2
        if is_valid_move(new_x, new_y):
            maze[current_y + direction[1]][current_x + direction[0]] = 1
            maze[new_y][new_x] = 1
            carve_passages_from(new_x, new_y)

def generate_maze():
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 1
    carve_passages_from(start_x, start_y)
    maze[exit_y][exit_x] = 1

def draw_maze():
    for y in range(rows):
        for x in range(cols):
            color = WHITE if maze[y][x] == 1 else LILAC
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
            if (x, y) == (player_x, player_y):
                screen.blit(character_image, (x * cell_size, y * cell_size))
            if (x, y) == (exit_x, exit_y):
                pygame.draw.rect(screen, GREEN, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
    draw_timer()

def move_player(key):
    global player_x, player_y
    new_x, new_y = player_x, player_y
    if key == pygame.K_UP:
        new_y -= 1
    elif key == pygame.K_DOWN:
        new_y += 1
    elif key == pygame.K_LEFT:
        new_x -= 1
    elif key == pygame.K_RIGHT:
        new_x += 1

    if maze[new_y][new_x] == 1:
        player_x, player_y = new_x, new_y

def show_message(message, color):
    font = pygame.font.Font(None, 30)
    text_lines = message.splitlines()  # Splits message into lines
    for line in text_lines:
        # Clears the screen
        screen.fill(LILAC)
        # Renders current line
        text = font.render(line, True, color)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)  # Adjusts the delay here (2 seconds per line)

def draw_timer():
    if start_time is not None:
        current_time = int(time.time() - start_time)
        time_left = max(0, level_time_limit - current_time)
        font = pygame.font.Font(None, 36)
        text_time = font.render(f"Time Left: {time_left}", True, BLACK)
        text_score = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text_time, (5, 5))
        screen.blit(text_score, (width - 150, 5))

def next_level():
    global cols, rows, cell_size, maze, player_x, player_y, exit_x, exit_y, score

    score += 10  # Increases score for next level
    cols += 4  # Increases the size of the maze for the next level
    rows += 4
    cell_size = width // cols
    player_x, player_y = 1, 1
    exit_x, exit_y = cols - 2, rows - 2
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    generate_maze()

def main():
    global player_x, player_y, start_time, level_time_limit, cols, rows, cell_size, maze, exit_x, exit_y, score

    # Tutorial messages
    tutorial_messages = [
        "Welcome to the Maze Game!",
        "Use arrow keys to move the character.",
        "Reach the green square to win each level.",
        "You have 1 minute per level. Good luck!"
    ]

    # Displays tutorial messages line by line
    for message in tutorial_messages:
        show_message(message, WHITE)

    generate_maze()
    player_x, player_y = 1, 1
    clock = pygame.time.Clock()
    start_time = time.time()
    level_time_limit = 60  
    running = True
    show_congratulations = False
    timeout_message_shown = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                move_player(event.key)

        elapsed_time = time.time() - start_time
        if elapsed_time > level_time_limit:
            if not timeout_message_shown:
                show_message("Time out, Try again!", WHITE)
                timeout_message_shown = True
                # Resets necessary variables 
                cols, rows = 21, 21  
                cell_size = width // cols
                player_x, player_y = 1, 1
                exit_x, exit_y = cols - 2, rows - 2
                maze = [[0 for _ in range(cols)] for _ in range(rows)]
                generate_maze()
                start_time = time.time()
            continue  

        if (player_x, player_y) == (exit_x, exit_y):
            if not show_congratulations:
                show_message("Congratulations, YOU WON!", WHITE)
                show_congratulations = True
            else:
                next_level()
                start_time = time.time()

        screen.fill(LILAC)
        draw_maze()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
