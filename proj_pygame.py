import pygame
import math

# initialize
pygame.init()

# flag
ok = True

# screen window size
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT) = (1000, 600)

# colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 100, 10)
YELLOW = (255, 255, 0)
PINK = (255, 100, 180)
PURPLE = (240, 0, 255)
RUST = (210, 150, 75)
LIME = (180, 255, 100)
# colors in one list
color = [BLACK, RED, GREEN, BLUE, ORANGE, YELLOW, PINK, PURPLE, RUST]
# i-th color
color_numbers = 0
# current colour
color_now = color[color_numbers]
# window
screen = pygame.display.set_mode(WINDOW_SIZE)

shape = 'line'
# setup fps
clock = pygame.time.Clock()
fps = 60
# Name(caption) of game
pygame.display.set_caption('Paint')
screen.fill(WHITE)

width = 1

prev = None  # previous
cur = None  # current
# type of font
font = pygame.font.SysFont('Verdana', 15)
font_ins = pygame.font.SysFont('Verdana', 12)

# Define the right margin for instructions
RIGHT_MARGIN = WINDOW_WIDTH - 160

# loop for game
while ok:
    # Очистка верхней и правой панели
    pygame.draw.rect(screen, WHITE, (0, 0, WINDOW_WIDTH, 30))  # Верхняя панель
    pygame.draw.rect(screen, WHITE, (RIGHT_MARGIN, 30, 160, WINDOW_HEIGHT))  # Правая панель

    # Перерисовка красных линий
    pygame.draw.line(screen, pygame.Color('red'), (0, 31), (WINDOW_WIDTH, 31), 5)  # Верхняя линия
    pygame.draw.line(screen, pygame.Color('red'), (RIGHT_MARGIN, 31), (RIGHT_MARGIN, WINDOW_HEIGHT), 5)  # Правая линия

    # Информация о режиме, ширине линии и текущем цвете (справа сверху)
    screen.blit(font.render(f'Mode: {shape}', True, BLACK), (RIGHT_MARGIN - 150, 10))
    screen.blit(font.render(f'Width: {width}', True, BLACK), (RIGHT_MARGIN - 350, 10))
    screen.blit(font.render(f'Color: {str(color_now)}', True, BLACK), (RIGHT_MARGIN - 550, 10))

    # Инструкции (в правой части)
    screen.blit(font.render(f'Instruction: ', True, BLACK), (RIGHT_MARGIN + 10, 40))
    instructions = [
        "next Color = n",
        "Circle = CTRL+c",
        "Rect = CTRL+r",
        "Line = CTRL+l",
        "Eraser = CTRL+e",
        "Square = CTRL+s",
        "eq_tr = CTRL+t",
        "r_tr = CTRL+m",
        "Rhombus = CTRL+h",
        "Increase Width = UP",
        "Decrease Width = DOWN",
    ]
    for i, instruction in enumerate(instructions):
        screen.blit(font_ins.render(instruction, True, BLACK), (RIGHT_MARGIN + 10, 65 + i * 20))

    # check if the keyboard pressed
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        ctrl_pressed = pressed[pygame.K_RCTRL] or pressed[pygame.K_LCTRL]

        if event.type == pygame.QUIT:
            ok = False

        # if pressed which shapes and width
        if event.type == pygame.KEYDOWN:
            if pressed[pygame.K_DOWN] and width > 1:
                width -= 1
            if pressed[pygame.K_UP]:
                width += 1
            if pressed[pygame.K_n]:
                color_numbers = (color_numbers + 1) % len(color)  # Зацикливаем индекс
                color_now = color[color_numbers]
            if ctrl_pressed and pressed[pygame.K_c]:
                shape = 'circle'
            if ctrl_pressed and pressed[pygame.K_r]:
                shape = 'rectangle'
            if ctrl_pressed and pressed[pygame.K_l]:
                shape = 'line'
            if ctrl_pressed and pressed[pygame.K_e]:
                shape = 'eraser'
            if ctrl_pressed and pressed[pygame.K_s]:
                shape = 'square'
            if ctrl_pressed and pressed[pygame.K_t]:
                shape = 'equilateral_triangle'
            if ctrl_pressed and pressed[pygame.K_m]:
                shape = 'right_triangle'
            if ctrl_pressed and pressed[pygame.K_h]:
                shape = 'rhombus'

        if shape == 'line' or shape == 'eraser':
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                cur = pygame.mouse.get_pos()
                if prev:
                    if shape == 'line':
                        pygame.draw.line(screen, color_now, prev, cur, width)
                    if shape == 'eraser':
                        pygame.draw.line(screen, WHITE, prev, cur, width)
                    prev = cur
            if event.type == pygame.MOUSEBUTTONUP:
                prev = None
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                cur = pygame.mouse.get_pos()
                if shape == 'circle':
                    x = (prev[0] + cur[0]) / 2
                    y = (prev[1] + cur[1]) / 2
                    rx = abs(prev[0] - cur[0]) / 2
                    ry = abs(prev[1] - cur[1]) / 2
                    r = (rx + ry) / 2
                    pygame.draw.circle(screen, color_now, (int(x), int(y)), int(r), width)
                elif shape == 'rectangle' or shape == 'square':
                    x = min(prev[0], cur[0])
                    y = min(prev[1], cur[1])
                    lx = abs(prev[0] - cur[0])
                    ly = abs(prev[1] - cur[1])
                    if shape == 'square':
                        lx = (lx + ly) / 2
                        ly = lx
                    pygame.draw.rect(screen, color_now, (x, y, lx, ly), width)
                elif shape == 'right_triangle' or shape == 'equilateral_triangle':
                    x = min(prev[0], cur[0])
                    y = min(prev[1], cur[1])
                    lx = abs(prev[0] - cur[0])
                    ly = abs(prev[1] - cur[1])
                    if shape == 'equilateral_triangle':
                        ly = math.sqrt(lx**2 - (lx / 2)**2)
                    points = (x, y + ly), (x + lx / 2, y), (x + lx, y + ly)
                    pygame.draw.polygon(screen, color_now, points, width)
                elif shape == 'rhombus':
                    x = min(prev[0], cur[0])
                    y = min(prev[1], cur[1])
                    lx = abs(prev[0] - cur[0])
                    ly = abs(prev[1] - cur[1])
                    points = (x + lx / 2, y), (x + lx, y + ly / 2), (x + lx / 2, y + ly), (x, y + ly / 2)
                    pygame.draw.polygon(screen, color_now, points, width)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
