import pygame
from pygame.draw import circle
from pygame.math import Vector2


class Agent:
    def __init__(self):
        self.circle_color = (100,50,225)
        self.radius = 100
        self.position = Vector2(0, 0)
        self.vel = Vector2(0,0)
        self.acc = Vector2(2,2)

    def update(self):
        self.vel += self.acc
        self.position += self.vel
        self.acc = Vector2(0,0)
    
    def draw(self,screen):
        circle(screen,self.circle_color,self.position,self.radius)
