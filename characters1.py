import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 600, 600  # Increased screen size for better spacing
cols, rows = 21, 21  # Ensure cols and rows are odd numbers for a perfect maze
cell_size = width // cols
player_x, player_y = 1, 1
exit_x, exit_y = cols - 2, rows - 2

# Set up display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generator")

# Colors
WHITE = (255, 255, 255)
LILAC = (164, 91, 170)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Load character images
try:
    character_images = [
        pygame.image.load("C:/projects/Character01.png"),
        pygame.image.load("C:/projects/Character02.png"),
        pygame.image.load("C:/projects/Character03.png"),
        pygame.image.load("C:/projects/Character04.png")
    ]
    for i in range(len(character_images)):
        # Scale character images to fit within the maze cells
        character_images[i] = pygame.transform.scale(character_images[i], (cell_size - 10, cell_size - 10))  # Adjust size here
except pygame.error as e:
    print(f"Unable to load character image: {e}")
    pygame.quit()
    exit()

# Initialize the maze grid
maze = [[0 for _ in range(cols)] for _ in range(rows)]

# Initialize score
score = 0

# Selected character index
selected_character = 0
character_marker_x = (width // 2) - (cell_size * 2 + 20)  # Initial position of the blue square
character_marker_y = (height // 2) - (cell_size * 2 + 20)
character_spacing = 20
marker_size = cell_size  # The size of the blue outline

def is_valid_move(x, y):
    return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 1

def carve_passages_from(current_x, current_y):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    random.shuffle(directions)
    for direction in directions:
        new_x = current_x + direction[0] * 2
        new_y = current_y + direction[1] * 2
        if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x] == 0:
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
                # Calculate position to center the character image in the maze cell
                char_x = x * cell_size + (cell_size - character_images[selected_character].get_width()) // 2
                char_y = y * cell_size + (cell_size - character_images[selected_character].get_height()) // 2
                screen.blit(character_images[selected_character], (char_x, char_y))

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

    if is_valid_move(new_x, new_y):
        player_x, player_y = new_x, new_y

def show_message(message, color):
    font = pygame.font.Font(None, 30)
    text_lines = message.splitlines()  # Split message into lines
    for line in text_lines:
        # Clear screen
        screen.fill(LILAC)
        # Render current line
        text = font.render(line, True, color)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)  # Adjust the delay here (2 seconds per line)

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

    score += 10  # Increase score for next level
    cols += 4  # Increase the size of the maze for the next level
    rows += 4
    cell_size = width // cols
    player_x, player_y = 1, 1
    exit_x, exit_y = cols - 2, rows - 2
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    generate_maze()

def select_character():
    global selected_character, character_marker_x, character_marker_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        selected_character = (selected_character - 1) % len(character_images)
    elif keys[pygame.K_RIGHT]:
        selected_character = (selected_character + 1) % len(character_images)

    # Update character marker position
    character_marker_x = (width // 2) - (cell_size * 2 + 20) + (selected_character % 2) * (marker_size + character_spacing)
    character_marker_y = (height // 2) - (cell_size * 2 + 20) + (selected_character // 2) * (marker_size + character_spacing)

def display_character_selection():
    screen.fill(LILAC)
    font = pygame.font.Font(None, 30)
    selection_text = font.render("Choose your character:", True, WHITE)
    screen.blit(selection_text, (width // 2 - 150, 50))

    # Display character images with numbers in a 2x2 grid
    for i, image in enumerate(character_images):
        x = (width // 2) - (cell_size * 2 + 20) + (i % 2) * (marker_size + character_spacing)
        y = (height // 2) - (cell_size * 2 + 20) + (i // 2) * (marker_size + character_spacing)
        screen.blit(image, (x, y))

    # Display character selection marker
    pygame.draw.rect(screen, BLUE, pygame.Rect(character_marker_x, character_marker_y, marker_size, marker_size), 2)

def main():
    global player_x, player_y, start_time, level_time_limit, cols, rows, cell_size, maze, exit_x, exit_y, score

    # Tutorial messages
    tutorial_messages = [
        "Welcome to the Maze Game!",
        "Use arrow keys to move the character.",
        "Reach the green square to win each level.",
        "You have 1 minute per level. Good luck!"
    ]

    # Display tutorial messages line by line
    for message in tutorial_messages:
        show_message(message, WHITE)

    # Character selection
    display_character_selection()
    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected = True
                    break
        select_character()
        display_character_selection()  # Redraw the selection screen to update the marker position
        pygame.display.flip()

    generate_maze()
    player_x, player_y = 1, 1
    clock = pygame.time.Clock()
    start_time = time.time()
    level_time_limit = 60  # 1 minute time limit
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
                # Reset necessary variables for a new game
                cols, rows = 21, 21  # Reset maze dimensions
                cell_size = width // cols
                player_x, player_y = 1, 1
                exit_x, exit_y = cols - 2, rows - 2
                maze = [[0 for _ in range(cols)] for _ in range(rows)]
                generate_maze()
                start_time = time.time()
            continue  # Skip the rest of the loop for this frame if timed out

        if (player_x, player_y) == (exit_x, exit_y):
            if not show_congratulations:
                show_message("Congratulations, YOU WON!", WHITE)
                show_congratulations = True
            else:
                next_level()
                # Reset necessary variables for the next level
                cols += 4
                rows += 4
                cell_size = width // cols
                player_x, player_y = 1, 1
                exit_x, exit_y = cols - 2, rows - 2
                maze = [[0 for _ in range(cols)] for _ in range(rows)]
                generate_maze()
                start_time = time.time()

        screen.fill(LILAC)
        draw_maze()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
