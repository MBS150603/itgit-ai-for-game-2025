import pygame
import pygame_gui
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from agent import Agent
import random, math

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True

        # self.manager = pygame_gui.UIManager((800,600))

        self.agents = []
        # self.agents[0].mass = 10
        # self.agents[1].mass = 10
        # self.agents[2].mass = 10

        for i in range(50):
            agent = Agent(position=Vector2(random.randint(100,screen_width) , random.randint(100,screen_height)),
                          radius=10,
                          color=(random.randint(0,255),0,0))
            agent.mass = 10
            agent.vel = Vector2(-1,0)
            self.agents.append(agent)
        

        # self.agents[0].apply_force(Vector2(0,3))
        # self.agents[1].apply_force(Vector2(0,3))
        # self.agents[2].apply_force(Vector2(0,3))

        #Way point
        # self.waypoint = [Vector2(100,100), Vector2(100,600), Vector2(1000,600), Vector2(1000, 100)]

        # self.currant_waypoints = [0, 0, 0]
        # self.targets = [
        #     self.waypoint[self.currant_waypoints[0]],
        #     self.waypoint[self.currant_waypoints[1]],
        #     self.waypoint[self.currant_waypoints[2]]
        # ]

    def bound_check(self, agent):
        if agent.position.x < -10:
            agent.position.x = screen_width + 30
        elif agent.position.x > screen_width + 34:
            agent.position.x = -5
        elif agent.position.y < -10:
            agent.position.y = screen_height + 30
        elif agent.position.y > screen_height + 34:
            agent.position.y = -5

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # to detect key pressed
            elif event.type == pygame.KEYDOWN:
                # esc pressed
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_x,mouse_y)

    def update(self, delta_time_s):
        for agent in self.agents:
            cohesion_f = agent.get_cohesion_force(self.agents)
            agent.apply_force(cohesion_f)

            separation_f = agent.get_separation_force(self.agents)
            agent.apply_force(separation_f)

            align_f = agent.get_align_force(self.agents)
            agent.apply_force(align_f)
            agent.update(delta_time_s)
            self.bound_check(agent)

        # self.manager.update(delta_time_s)

    def draw(self):
        self.screen.fill("grey")
        for agent in self.agents:
            agent.draw(self.screen)

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