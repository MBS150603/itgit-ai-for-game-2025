from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Reload:
    def __init__(self, position, radius, color):
        self.color = color
        self.circle_radius = radius
        self.position = position
        self.destroy = False
        # self.collide = False

    def drawBullet(self, screen):
        circle(screen, self.color, self.position, self.circle_radius)
