import pygame
import sys

# تنظیمات بازی
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 5, 5  # تعداد ردیف و ستون نقطه‌ها
DOT_RADIUS = 5
LINE_WIDTH = 5
SQUARE_SIZE = 100
MARGIN = 50

PLAYER_COLORS = [(255, 0, 0), (0, 0, 255)]  # قرمز و آبی

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots and Boxes")
font = pygame.font.SysFont(None, 48)

# ساخت ماتریس خطوط
h_lines = [[False for _ in range(COLS - 1)] for _ in range(ROWS)]
v_lines = [[False for _ in range(COLS)] for _ in range(ROWS - 1)]
squares = [[-1 for _ in range(COLS - 1)] for _ in range(ROWS - 1)]

current_player = 0
scores = [0, 0]

def draw_board():
    screen.fill((255, 255, 255))
    # رسم نقاط
    for i in range(ROWS):
        for j in range(COLS):
            x = MARGIN + j * SQUARE_SIZE
            y = MARGIN + i * SQUARE_SIZE
            pygame.draw.circle(screen, (0, 0, 0), (x, y), DOT_RADIUS)

    # رسم خطوط افقی
    for i in range(ROWS):
        for j in range(COLS - 1):
            if h_lines[i][j]:
                x = MARGIN + j * SQUARE_SIZE
                y = MARGIN + i * SQUARE_SIZE
                pygame.draw.line(screen, PLAYER_COLORS[h_lines[i][j] - 1], (x, y), (x + SQUARE_SIZE, y), LINE_WIDTH)

    # رسم خطوط عمودی
    for i in range(ROWS - 1):
        for j in range(COLS):
            if v_lines[i][j]:
                x = MARGIN + j * SQUARE_SIZE
                y = MARGIN + i * SQUARE_SIZE
                pygame.draw.line(screen, PLAYER_COLORS[v_lines[i][j] - 1], (x, y), (x, y + SQUARE_SIZE), LINE_WIDTH)

    # رسم خانه‌های تکمیل شده
    for i in range(ROWS - 1):
        for j in range(COLS - 1):
            if squares[i][j] != -1:
                x = MARGIN + j * SQUARE_SIZE + SQUARE_SIZE // 2
                y = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.rect(screen, PLAYER_COLORS[squares[i][j]], 
                                 (x - 20, y - 20, 40, 40))

def check_square_completion():
    completed = False
    for i in range(ROWS - 1):
        for j in range(COLS - 1):
            if squares[i][j] == -1:
                if h_lines[i][j] and h_lines[i+1][j] and v_lines[i][j] and v_lines[i][j+1]:
                    squares[i][j] = current_player
                    scores[current_player] += 1
                    completed = True
    return completed

def get_line_clicked(pos):
    x, y = pos
    for i in range(ROWS):
        for j in range(COLS - 1):
            x1 = MARGIN + j * SQUARE_SIZE
            y1 = MARGIN + i * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            y2 = y1
            if abs((y - y1)) < 25 and x1 <= x <= x2:
                if not h_lines[i][j]:
                    return ('h', i, j)

    for i in range(ROWS - 1):
        for j in range(COLS):
            x1 = MARGIN + j * SQUARE_SIZE
            y1 = MARGIN + i * SQUARE_SIZE
            x2 = x1
            y2 = y1 + SQUARE_SIZE
            if abs((x - x1)) < 25 and y1 <= y <= y2:
                if not v_lines[i][j]:
                    return ('v', i, j)

    return (None, None, None)

def game_over():
    for row in squares:
        for square in row:
            if square == -1:
                return False
    return True

def show_winner():
    screen.fill((255, 255, 255))
    if scores[0] > scores[1]:
        text = font.render("Player 1 Wins!", True, (255, 0, 0))
    elif scores[1] > scores[0]:
        text = font.render("Player 2 Wins!", True, (0, 0, 255))
    else:
        text = font.render("Draw!", True, (0, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(3000)

# حلقه‌ی اصلی بازی
running = True
while running:
    draw_board()
    pygame.display.flip()

    if game_over():
        show_winner()
        running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            line_type, i, j = get_line_clicked(pygame.mouse.get_pos())
            if line_type == 'h':
                h_lines[i][j] = current_player + 1
                if not check_square_completion():
                    current_player = 1 - current_player
            elif line_type == 'v':
                v_lines[i][j] = current_player + 1
                if not check_square_completion():
                    current_player = 1 - current_player

pygame.quit()
sys.exit()