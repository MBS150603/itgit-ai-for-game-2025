# import pygame
# from pygame.draw import circle
# from pygame.math import Vector2
# from agent import Agent
# import pygame_gui
# import random
# import math

# screen_width = 1270
# screen_height = 720

# class App:
#     def __init__(self):
#         print("Application is created")

#         # pygame setup
#         pygame.init()

#         self.screen = pygame.display.set_mode((screen_width, screen_height))
#         self.clock = pygame.time.Clock()

#         self.manager = pygame_gui.UIManager((800,600))
#         # self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350,275),(100,50)),
#         #                                             text = "Say Hello",
#         #                                             manager = self.manager)
#         # self.horizontal_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((200,50),(300,50)),
#         #                                             start_value = 200, value_range = (200,400),
#         #                                             manager = self.manager)

#         self.running = True

#         self.timer  = 0

#         self.agents =[
#                     Agent(position = Vector2(screen_width/2,screen_height/4),
#                           radius = 30,
#                           color = (100,50,225),
#                           vel = Vector2(0,0),
#                           acc = Vector2(0,0)),
                    
#                     Agent(position = Vector2(screen_width/2,screen_height/2),
#                           radius = 70,
#                           color = (100,50,225),
#                           vel = Vector2(0,0),
#                           acc = Vector2(0,0)),
        
#                     Agent(position = Vector2(screen_width/2,screen_height/6),
#                           radius = 50,
#                           color = (100,50,225),
#                           vel = Vector2(0,0),
#                           acc = Vector2(0,0))
#         ]

#         for agent in self.agents:
#             agent.vel = Vector2(1,0)
        
#         #waypoint system
#         self.waypoints = [Vector2(100,0), Vector2(1000,100),Vector2(0,800)]
#         # self.current_waypoint_num = 0
#         # self.target = self.waypoints[self.current_waypoint_num]
#         self.current_waypoint_nums = [0,1,2]
#         self.targets = [self.waypoints[self.current_waypoint_nums[0]],
#                         self.waypoints[self.current_waypoint_nums[1]],
#                         self.waypoints[self.current_waypoint_nums[2]]]

#     def handle_input(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#             # to detect key pressed
#             elif event.type == pygame.KEYDOWN:
#                 # esc pressed
#                 if event.key == pygame.K_ESCAPE:
#                     self.running = False
#             # elif event.type == pygame_gui.UI_BUTTON_PRESSED:
#             #     if event.ui_element == self.hello_button:
#             #         print("Hello!")
                    
#             # self.manager.process_events(event)
#         # mouse_x, mouse_y = pygame.mouse.get_pos()
#         # self.target = Vector2(mouse_x, mouse_y)

#     def update(self, delta_time_s):

#         self.timer += delta_time_s

#         for i, agent in enumerate(self.agents):
#             target = agent.position + (agent.vel.normalize() * 100)
#             if self.timer > 1:
#                 #random the angle
#                 theta = random.randint(-100,100)
#                 #dont * theta or it'll move in circle
#                 target += Vector2(math.cos(theta), math.sin(theta)) * 50
#             agent.seek_to(target)
#             agent.update(delta_time_s)
#             # agent.free_from(self.target)
#             # self.ball.arrive_to(self.target)

#         if self.timer > 1:
#             self.timer = 0
        
#         self.manager.update(delta_time_s)
        
    
#     def draw(self):

#         self.screen.fill("white")

#         for agent in self.agents:
#             agent.draw(self.screen)

#         self.manager.draw_ui(self.screen)

#         pygame.display.flip()
        
#     def run(self):
#         while self.running:
#             delta_time = self.clock.tick(60)  # limits FPS to 60
#             self.handle_input()
#             self.update(delta_time)
#             self.draw()

#         pygame.quit()
    
# def main():
#     app = App()
#     app.run()

# if __name__ == "__main__":
#     main()

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
        self.timer = 0
        #self.manager = pygame_gui.UIManager((800, 600))

        self.ball = Agent(position=Vector2(screen_width//2, screen_height//2), 
                          radius=50, 
                          color=(255,0,0)) #เรียกและส่งหน้าจอไปยังไฟล์ agent

        self.agents = [
            Agent(position=Vector2(100, screen_height//2), 
                    radius=50, 
                    color=(255,0,0)),
            Agent(position=Vector2(500, screen_height//2), 
                    radius=30, 
                    color=(242,127,0)),
            Agent(position=Vector2(screen_width//2, 300), 
                    radius=10, 
                    color=(0,75,100))
        ]

        for agent in self.agents:
            agent.vel = Vector2(1, 0)

        #Way point
        self.waypoint = [Vector2(100,100), Vector2(100,600), Vector2(1000,600), Vector2(1000, 100)]

        self.currant_waypoints = [0, 0, 0]
        self.targets = [
            self.waypoint[self.currant_waypoints[0]],
            self.waypoint[self.currant_waypoints[1]],
            self.waypoint[self.currant_waypoints[2]]
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
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_x,mouse_y)


    def update(self, delta_time_s):
        self.timer += delta_time_s

        for i,agent in enumerate(self.agents): #
            target = agent.position + (agent.vel.normalize() * 100)
            if self.timer > 1:
                theta = random.randint(-100,100)
                target += Vector2(math.cos(theta), math.sin(theta)) * 50

            agent.seek_to(target)
            agent.update(delta_time_s)

        if self.timer > 1:
            self.timer = 0

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