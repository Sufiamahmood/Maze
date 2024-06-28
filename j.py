import pygame

# Define the maze dimensions
maze_width = 20
maze_height = 10
cell_size = 45


# Define the maze
maze = [
    "####################",
    "#                  #",
    "#  #######  ####   #",
    "#  #              ##",
    "#  #  #####  ####  #",
    "#  #  #        #   #",
    "#  #  #  ##### #   #",
    "#     #        #   #",
    "# ###############  #",
    "####################"
]

# Define the player's starting position
player_x, player_y = 1, 1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

def draw_maze(screen):
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == '#':
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
            elif maze[y][x] == ' ':
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
            if x == player_x and y == player_y:
                pygame.draw.rect(screen, BLUE, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

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

    if maze[new_y][new_x] == ' ':
        player_x, player_y = new_x, new_y

def main():
    pygame.init()
    screen = pygame.display.set_mode((maze_width * cell_size, maze_height * cell_size))
    pygame.display.set_caption('Maze Navigation Game')

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                move_player(event.key)
        
        screen.fill(WHITE)
        draw_maze(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()

