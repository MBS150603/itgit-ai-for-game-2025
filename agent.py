import pygame
from pygame.draw import circle
from pygame.math import Vector2

class Agent:
    def __init__(self, position, radius, color, vel, acc):
        self.circle_color = color
        self.radius = radius
        self.position = position
        self.vel = vel
        self.acc = acc
        self.mass = 1.0

    def seek_to(self, target_pos):
        MAX_FORCE = 5
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        desired = d.normalize() * MAX_FORCE
        steering = desired - self.vel
        if steering.length() < MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)
        self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self, delta_time):
        self.vel += self.acc
        self.position += self.vel
        self.acc = Vector2(0,0)
    
    def draw(self,screen):
        circle(screen,self.circle_color,self.position,self.radius)
