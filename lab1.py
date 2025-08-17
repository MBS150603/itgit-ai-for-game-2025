# Example file showing a basic pygame "game loop"
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2

screen_width = 1230
screen_height = 700

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

circle_color = (225,0,0)
# circle_center = (screen_width/2, screen_height/2)
radius = 100
position = Vector2(screen_width/2, screen_height/2)
vel = Vector2(0,0)
acc = Vector2(0,0)
acc.x = 1
acc.y = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    
    # vel.x += acc.x
    # vel.y += acc.y
    vel += acc 
    # position.x += vel.x
    # position.y += vel.y
    position += vel
    circle(screen,circle_color,position,radius)
    acc.x = 0
    acc.y = 0

    # line_color = (0,0,0)
    # line_start = ((screen_width/2)-200,200)
    # line_end = ((screen_width/2)+200,200)
    # width = 10
    # line(screen,line_color,line_start,line_end,width)

    # rect_color = (0,0,0)
    # rect_size = ((screen_width/2) - 125, 100, 250, 100)
    # rect(screen, rect_color, rect_size)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    

pygame.quit()