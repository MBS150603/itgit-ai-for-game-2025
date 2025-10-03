from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Agent:
    def __init__(self, position, radius, color):
        self.color = color
        self.circle_radius = radius
        self.vel = Vector2(0,-0.5)
        self.position = position
        self.acc = Vector2(0,0)
        self.mass = 1.0
        self.hit_box = 20
        self.STOP_DIST = 5 #ระยะที่บอลต้องใกล้หยุด
        self.target = Vector2(0,0)
        self.MAXFORCE = 2
        self.destroy = False
        self.gravity = Vector2(0,0)

    def seek_to(self, target_pos):
        self.target = target_pos
        d = target_pos - self.position
        dist = d.length()
        if d.length_squared() == 0:
            return
        desired = d.normalize() * self.MAXFORCE
        steering = desired - self.vel
        if steering.length() > self.MAXFORCE:
            steering.scale_to_length(self.MAXFORCE)
        if dist <= self.hit_box:
            self.destroy = True

        self.apply_force(steering)
        
        
    # def arrive_to(self, target_pos):
    #     MAXFORCE = 5
    #     d = target_pos - self.position
    #     if d.length_squared() == 0:
    #         return
        
    #     dist = d.length() #การทำ squareroot จะกินระบบมาก ควรเรียกครั้งเดียว 
    #     if dist < self.STOP_DIST:
    #         desired = Vector2(0,0)
    #     elif dist < self.hit_box:
    #         desired = d.normalize() * (MAXFORCE * (dist/self.hit_box)) #มองเป็นพลังงาน ระยะมากยิ่งไว
    #     else:
    #         desired = d.normalize() * MAXFORCE
        
    #     steering = desired - self.vel
    #     if steering.length() > MAXFORCE:
    #         steering.scale_to_length(MAXFORCE)

    #     self.apply_force(steering)
        
    # def patrol(self, target_pos):
        
    #     MAXFORCE = 5
    #     d = Vector2(100,200) - self.position
    #     if d.length_squared() == 0:
    #         return
    
    #     desired = d.normalize() * MAXFORCE
    #     steering = desired - self.vel
    #     if steering.length() > MAXFORCE:
    #         steering.scale_to_length(MAXFORCE)

    #     self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force/ self.mass

    def set_gravity(self, gravity):
        self.gravity = gravity

    def get_cohesion_force(self, agents):
        # each agent needs to know all agents in scene
        center_of_mass = Vector2(0,0)
        for agent in agents:
            center_of_mass += agent.position
        center_of_mass /= len(agents)

        d = center_of_mass - self.position
        d.scale_to_length(1)
        return d

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc + self.gravity
        self.position = self.position + self.vel
        self.acc = Vector2(0, 0)

    def draw(self, screen):
        # circle(screen, (100,100,0), self.position, self.hit_box, width = 1)
        # line(screen,(100,0,0), self.position, self.target)
        circle(screen, self.color, self.position, self.circle_radius)
        # if self.destroy == True:
        #     return