from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Food:
    def __init__(self, position, fish_food_image):
        # self.color = color
        # self.circle_radius = radius
        self.food_image = fish_food_image
        self.vel = Vector2(0, 0)
        self.position = position
        self.acc = Vector2(0, 0)
        self.mass = 50
        self.EYE_SIGHT = 100
        self.STOP_DIST = 5 #ระยะที่บอลต้องใกล้หยุด
        self.target = Vector2(0,0)
        self.gravity = Vector2(0,0)
        self.center_of_mass = Vector2(0,0)

    def seek_to(self, target_pos):
        self.target = target_pos
        MAXFORCE = 5
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        desired = d.normalize() * MAXFORCE
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)
        self.apply_force(steering)

    # def arrive_to(self, target_pos):
    #     MAXFORCE = 5
    #     d = target_pos - self.position
    #     if d.length_squared() == 0:
    #         return
    #     dist = d.length() #การทำ squareroot จะกินระบบมาก ควรเรียกครั้งเดียว 
    #     if dist < self.STOP_DIST:
    #         desired = Vector2(0,0)
    #     elif dist < self.EYE_SIGHT:
    #         desired = d.normalize() * (MAXFORCE * (dist/self.EYE_SIGHT)) #มองเป็นพลังงาน ระยะมากยิ่งไว
    #     else:
    #         desired = d.normalize() * MAXFORCE
    #     steering = desired - self.vel
    #     if steering.length() > MAXFORCE:
    #         steering.scale_to_length(MAXFORCE)
    #     self.apply_force(steering)

    def flee_form(self, target_pos):
        MAXFORCE = 5
        d = (target_pos - self.position) * -1
        if d.length_squared() == 0:
            return
        dist = d.length()
        if dist > self.EYE_SIGHT:
            desired = self.vel
        else:
            desired = d.normalize() * (MAXFORCE * ((self.EYE_SIGHT - dist)/self.EYE_SIGHT))
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)
        self.apply_force(steering)
    
    # def patrol(self, target_pos):
    #     MAXFORCE = 5
    #     d = Vector2(100,200) - self.position
    #     if d.length_squared() == 0:
    #         return
    #     desired = d.normalize() * MAXFORCE
    #     steering = desired - self.vel
    #     if steering.length() > MAXFORCE:
    #         steering.scale_to_length(MAXFORCE)
        # self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force / self.mass

    def set_gravity(self, gravity):
        self.gravity = gravity

    def get_cohesion_force(self, food):
        # each agent needs to know all food in scene
        center_of_mass = Vector2(0,0)
        count = 0
        for f in food:
            # length_squared is for optimization, so it won't lag
            dist = (f.position - self.position).length_squared()
            if 0 < dist < 400*400:
                center_of_mass += f.position
                count += 1
        if count > 0:
            # center_of_mass /= len(food)
            center_of_mass /= count
            self.center_of_mass = center_of_mass
            d = center_of_mass - self.position
            d.scale_to_length(1)
            return d
        return Vector2()

    def get_separation_force(self, agents):
        s = Vector2()
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            # distance between agent and agent
            # agent without the current agent
            if dist < 60*60 and dist != 0:
                d = self.position - agent.position
                s += d
                count += 1
        if count > 0:
            s.scale_to_length(1)
            return s
        else:
            return Vector2()

    def get_align_force(self, agents):
        a = Vector2()
        count = 0
        # distance between agent and agent
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            # agent without the current agent
            if dist < 500*500 and dist != 0:
                a += agent.vel
                count += 1
        if count > 0 and a != Vector2():
            a /= count
            a.scale_to_length(4)
            return a
        return Vector2()
    
    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc + self.gravity
        self.position = self.position + self.vel
        self.vel *= 0.95
        self.acc = Vector2(0, 0)

    def draw(self, screen):
        screen.blit(self.food_image, (self.position.x, self.position.y))
        #circle(screen, (100,100,0), self.position, self.EYE_SIGHT, width = 1)
        # line(screen,(100,0,0), self.position, self.center_of_mass)
        # circle(screen, self.color, self.position, self.circle_radius)