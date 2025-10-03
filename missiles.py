import pygame
import pygame_gui
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from missile_agent import Agent
from m_bullets_agent import Reload

import random, math

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.timer = 0
        self.lock_in_timer = 0

        #self.manager = pygame_gui.UIManager((800, 600))

        # self.ball = Agent(position=Vector2(screen_width//2, screen_height//2), 
        #                   radius=50, 
        #                   color=(255,0,0)) #เรียกและส่งหน้าจอไปยังไฟล์ agent
        self.is_pressed = False


        self.agents = []
        self.bullet_gauge = [
            Reload(position=Vector2(screen_width-200, screen_height-40), 
                    radius=20, 
                    color=(255,0,0)),
            Reload(position=Vector2(screen_width-160, screen_height-40), 
                    radius=20, 
                    color=(255,0,0)),
            Reload(position=Vector2(screen_width-120, screen_height-40), 
                    radius=20, 
                    color=(255,0,0)),
            Reload(position=Vector2(screen_width-80, screen_height-40), 
                    radius=20, 
                    color=(255,0,0)),
            Reload(position=Vector2(screen_width-40, screen_height-40), 
                    radius=20, 
                    color=(255,0,0))
        ]
        #Way point
        self.waypoint = [Vector2(10,700)]

        self.current_waypoints = [0, 0, 0]
        self.targets = [
            self.waypoint[self.current_waypoints[0]]
        ] 

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # to detect key pressed
            elif event.type == pygame.KEYDOWN:
                # esc pressed
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.bullet_gauge != []:
                    if event.key == pygame.K_SPACE:
                        self.is_pressed = True
                        self.agents += [
                            Agent(position=Vector2(screen_width/2, screen_height-10), 
                                    radius=10, 
                                    color=(255,0,0)),
                            Agent(position=Vector2(screen_width/2-10, screen_height), 
                                    radius=10, 
                                    color=(255,0,0)),
                            Agent(position=Vector2(screen_width/2-10, screen_height-10), 
                                    radius=10, 
                                    color=(255,0,0))
                        ]
                        # for agent in self.agents:
                        #     agent.apply_force(Vector2(0,3))
                        b = 0
                        self.bullet_gauge.remove(self.bullet_gauge[b])
                        b += 1
                elif self.bullet_gauge == []:
                    if event.key == pygame.K_r:
                        self.bullet_gauge = [
                            Reload(position=Vector2(screen_width-200, screen_height-40), 
                                    radius=20, 
                                    color=(255,0,0)),
                            Reload(position=Vector2(screen_width-160, screen_height-40), 
                                    radius=20, 
                                    color=(255,0,0)),
                            Reload(position=Vector2(screen_width-120, screen_height-40), 
                                    radius=20, 
                                    color=(255,0,0)),
                            Reload(position=Vector2(screen_width-80, screen_height-40), 
                                    radius=20, 
                                    color=(255,0,0)),
                            Reload(position=Vector2(screen_width-40, screen_height-40), 
                                    radius=20, 
                                    color=(255,0,0))
                        ]
                # elif self.is_pressed == True:
                for agent in self.agents:
                    agent.vel = Vector2(0,-0.5)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.target = Vector2(mouse_x,mouse_y)

    def update(self, delta_time_s):
        center_of_mass = Vector2(0,0)
        if self.agents:
            if self.is_pressed == True:
                self.timer += delta_time_s
                self.lock_in_timer += delta_time_s
                for i, agent in enumerate(self.agents): #
                    target = agent.position + (agent.vel.normalize() * 100)
                    if self.timer > 2:
                        theta = random.randint(-50,50)
                        target += Vector2(math.cos(theta), math.sin(theta)) * 50
                    elif self.lock_in_timer >= 2:
                        agent.apply_force(Vector2(0,3))
                        target = self.target
                        agent.MAXFORCE = 5

                    if agent.destroy == True:
                        self.agents.remove(agent)
                        agent.destroy = False
                    # print(agent.destroy)
                    if self.agents == []:
                        self.is_pressed = False
                        self.lock_in_timer = 0
                        agent.MAXFORCE = 2
                    agent.seek_to(target)
                    agent.update(delta_time_s)

                if self.timer > 2:
                    self.timer = 0         

    def draw(self):
        self.screen.fill("grey")
        # if self.is_pressed == True:
        for agent in self.agents:
            agent.draw(self.screen)
        for bullet in self.bullet_gauge:
            bullet.drawBullet(self.screen)
        circle(self.screen, (100,50,100), Vector2(screen_width/2, screen_height), 100)
        #self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:        
            delta_time_s = self.clock.tick(60) / 1000
            self.handle_input()
            self.update(delta_time_s)
            self.draw()

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()