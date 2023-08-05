import random
import pygame as pg
import pygame.event


def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def handle_event(events):
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                quit()
def render_text(screen,text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
def random_spawn_x(WIDTH,obj_width):
    return random.randrange(0 + obj_width + 5 , WIDTH - obj_width - 5)
def random_spawn_y(HEIGHT,obj_HEIGHT):
    return random.randrange(0 + obj_HEIGHT + 5 , HEIGHT - obj_HEIGHT - 5)



