import pygame
from pygame.draw import circle
from pygame.math import Vector2

class Agent:
    def __init__(self, position, ant_image, vel, acc):
        self.ant_image = ant_image
        self.position = position
        self.vel = vel
        self.acc = acc
        self.mass = 2.0
        self.EYE_SIGHT = 100
        self.STOP_DIST = 50 #pixels
        self.MAX_FORCE = 3

    def seek_to(self, target_pos):
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        desired = d.normalize() * self.MAX_FORCE
        steering = desired - self.vel
        if steering.length() > self.MAX_FORCE:
            steering.scale_to_length(self.MAX_FORCE)
        self.apply_force(steering)

    def arrive_to(self, target_pos):
        d = target_pos - self.position
        if d.length_squared() == 0:
           return
        dist = d.length() # sqrt is expensive in games
        # if dist <= self.STOP_DIST:
        #     desired = Vector2(0,0)
        if dist < self.EYE_SIGHT:
            desired = d.normalize() * (self.MAX_FORCE * (dist/self.EYE_SIGHT))
        else:
            desired = d.normalize() * self.MAX_FORCE
        steering = desired - self.vel
        if steering.length() > self.MAX_FORCE:
            steering.scale_to_length(self.MAX_FORCE)
        self.apply_force(steering)

    def flee_from(self, target_pos):
        d = -(target_pos - self.position)
        if d.length_squared() == 0:
            return
        dist = d.length()
        if dist > self.EYE_SIGHT or dist <= self.STOP_DIST:
            desired = Vector2(0,0)
        else:
            # desired = d.normalize() * (self.MAX_FORCE * ((self.EYE_SIGHT- dist)/self.EYE_SIGHT))
            desired = d.normalize() * self.MAX_FORCE
        steering = desired - self.vel
        if steering.length() > self.MAX_FORCE:
            steering.scale_to_length(self.MAX_FORCE)
        self.apply_force(steering)

        

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self, delta_time):
        self.vel += self.acc
        self.position += self.vel
        self.acc = Vector2(0,0)
    
    def draw(self,screen):
        screen.blit(self.ant_image, (self.position.x, self.position.y))
        # circle(screen, (100,100,0), self.position, self.EYE_SIGHT, width=1)
        # circle(screen,self.circle_color,self.position,self.ant_image)
        # circle(screen, (100,0,0), self.position, self.STOP_DIST)

