import pygame
import random

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 75
CELL_COUNT = SCREEN_WIDTH // CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 36)


def draw_grid():
    for i in range(CELL_COUNT):
        for j in range(CELL_COUNT):
            pygame.draw.rect(screen, WHITE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)


def draw_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))


def draw_game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (
    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))


def generate_random_tile(board):
    while True:
        row = random.randint(0, CELL_COUNT - 1)
        col = random.randint(0, CELL_COUNT - 1)
        if board[row][col] == 0:
            board[row][col] = random.choice([2, 4])
            break


def move_tiles_left(board):
    for row in range(CELL_COUNT):
        for col in range(1, CELL_COUNT):
            if board[row][col] != 0:
                value = board[row][col]
                board[row][col] = 0
                j = col - 1
                while j >= 0:
                    if board[row][j] == 0:
                        board[row][j] = value
                        break
                    elif board[row][j] == value:
                        board[row][j] *= 2
                        break
                    j -= 1
                else:
                    board[row][col] = value


def move_tiles_right(board):
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT - 2, -1, -1):
            if board[row][col] != 0:
                value = board[row][col]
                board[row][col] = 0
                j = col + 1
                while j < CELL_COUNT:
                    if board[row][j] == 0:
                        board[row][j] = value
                        break
                    elif board[row][j] == value:
                        board[row][j] *= 2
                        break
                    j += 1
                else:
                    board[row][col] = value


def move_tiles_up(board):
    for col in range(CELL_COUNT):
        for row in range(1, CELL_COUNT):
            if board[row][col] != 0:
                value = board[row][col]
                board[row][col] = 0
                i = row - 1
                while i >= 0:
                    if board[i][col] == 0:
                        board[i][col] = value
                        break
                    elif board[i][col] == value:
                        board[i][col] *= 2
                        break
                    i -= 1
                else:
                    board[row][col] = value


def move_tiles_down(board):
    for col in range(CELL_COUNT):
        for row in range(CELL_COUNT - 2, -1, -1):
            if board[row][col] != 0:
                value = board[row][col]
                board[row][col] = 0
                i = row + 1
                while i < CELL_COUNT:
                    if board[i][col] == 0:
                        board[i][col] = value
                        break
                    elif board[i][col] == value:
                        board[i][col] *= 2
                        break
                    i += 1
                else:
                    board[row][col] = value


def is_move_possible(board):
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT):
            if board[row][col] == 0:
                return True
            if col > 0 and board[row][col] == board[row][col - 1]:
                return True
            if col < CELL_COUNT - 1 and board[row][col] == board[row][col + 1]:
                return True
            if row > 0 and board[row][col] == board[row - 1][col]:
                return True
            if row < CELL_COUNT - 1 and board[row][col] == board[row + 1][col]:
                return True
    return False


def start_new_game():
    board = [[0] * CELL_COUNT for _ in range(CELL_COUNT)]
    generate_random_tile(board)
    generate_random_tile(board)
    score = 0
    return board, score


def draw_tiles(board):
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT):
            value = board[row][col]
            color = (255, 255, 255)
            if value == 2:
                color = (238, 228, 218)
            elif value == 4:
                color = (237, 224, 200)
            elif value == 8:
                color = (242, 177, 121)
            elif value == 16:
                color = (245, 149, 99)
            elif value == 32:
                color = (246, 124, 95)
            elif value == 64:
                color = (246, 94, 59)
            elif value == 128:
                color = (237, 207, 114)
            elif value == 256:
                color = (237, 204, 97)
            elif value == 512:
                color = (237, 200, 80)
            elif value == 1024:
                color = (237, 197, 63)
            elif value == 2048:
                color = (237, 194, 46)
            pygame.draw.rect(screen, color, (col * CELL_SIZE + 2, row * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))
            if value != 0:
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)


board, score = start_new_game()
best_score = 0
is_game_over = False

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board, score = start_new_game()
                is_game_over = False
            elif not is_game_over:
                if event.key == pygame.K_LEFT:
                    move_tiles_left(board)
                elif event.key == pygame.K_RIGHT:
                    move_tiles_right(board)
                elif event.key == pygame.K_UP:
                    move_tiles_up(board)
                elif event.key == pygame.K_DOWN:
                    move_tiles_down(board)

                if is_move_possible(board):
                    generate_random_tile(board)

    screen.fill(BLACK)

    if score > best_score:
        best_score = score

    if is_game_over:
        draw_game_over()
    else:
        draw_tiles(board)
        draw_grid()
        draw_score(score)

        if not is_move_possible(board):
            is_game_over = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()