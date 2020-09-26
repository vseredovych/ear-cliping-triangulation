import pygame
from earclip import EarClipTriangulation

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN
)


def draw_vertex_circles(vertices):
    for vertex in vertices:
        pygame.draw.circle(screen, GREEN, vertex, RADIUS, RADIUS)


def fix_polygon_end_points(polygon, eps):
    finished = False

    if len(polygon) < 2:
        return finished, polygon

    start = polygon[0]
    end = polygon[-1]

    start_end_distance = ((start[0] - end[0])**2 + (start[1] - end[1])**2) ** (1/2)

    if start_end_distance < eps:
        polygon.pop(-1)
        polygon.append(polygon[0])
        finished = True

    return finished, polygon


def draw_polygon(polygon):
    if len(polygon) > 1:
        pygame.draw.aalines(screen, WHITE, False, polygon, RADIUS)
        draw_vertex_circles(polygon)


def draw_line_animation(polygon):
    if len(polygon) < 1:
        return

    p1 = polygon[-1]
    p2 = pygame.mouse.get_pos()
    pygame.draw.line(screen, WHITE, p1, p2)


def draw_triangulation(triangles):
    for tr in triangles:
        start_point = [tr.p1.x, abs(tr.p1.y)]
        end_point = [tr.p3.x, abs(tr.p3.y)]
        pygame.draw.aaline(screen, WHITE, start_point, end_point, LINE_WIDTH)


def draw_buttons(button_draw, button_triangulate):
    if button_draw_state:
        pygame.draw.rect(screen, GREEN, button_draw)
    else:
        pygame.draw.rect(screen, WHITE, button_draw)

    if button_triangulate_state:
        pygame.draw.rect(screen, GREEN, button_triangulate)
    else:
        pygame.draw.rect(screen, WHITE, button_triangulate)


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LINE_WIDTH = 1
EPS = 5
RADIUS = 5

GREEN = (60, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

polygon_area = 0
polygon = []
triangulation = []
running = True

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

button_draw = pygame.Rect(SCREEN_WIDTH - 120, 10, 50, 25)
button_triangulate = pygame.Rect(SCREEN_WIDTH - 60, 10, 50, 25)
button_draw_state = False
button_triangulate_state = False

font = pygame.font.SysFont('serif', 12)
area_text = font.render(f'Polygon area: {polygon_area}', 1, GREEN)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if button_draw.collidepoint(mouse_pos):
                button_draw_state = button_draw_state ^ True
                button_triangulate_state = False
                polygon_area = 0
                polygon = []
                triangulation = []

            elif button_triangulate.collidepoint(mouse_pos):
                button_triangulate_state = button_triangulate_state ^ True

                if len(polygon) > 3 and not triangulation:
                    triangulation = []
                    earclip = EarClipTriangulation()

                    fixed_polygon = [(x, -y) for x, y in polygon]
                    triangulation = earclip.triangulate(fixed_polygon)
                    polygon_area = earclip.compute_triangles_area(triangulation)

            elif button_draw_state:
                polygon.append(event.pos)
                polygon_finished, polygon = fix_polygon_end_points(polygon, EPS)

                if polygon_finished:
                    button_draw_state = False

    screen.fill(BLACK)

    # Draw buttons
    draw_buttons(button_draw, button_triangulate)

    # Draw polygon
    draw_polygon(polygon)

    # Drawing animation
    if button_draw_state:
        draw_line_animation(polygon)

    # Draw triangulation
    if button_triangulate_state:
        draw_triangulation(triangulation)

    # Draw information text
    area_text = font.render(f'Polygon area: {polygon_area}', 1, GREEN)
    screen.blit(area_text, (SCREEN_WIDTH - 130, 50))

    pygame.display.flip()

pygame.quit()





