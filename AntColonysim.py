import pygame
from pygame.math import Vector2
import random
from ants import Agent

screen_width = 1270
screen_height = 720

class App:
    def __init__(self):
        print("Application is created")

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.donut = pygame.image.load("Images/pixel_donut.png")
        self.donut = pygame.transform.scale(self.donut, (200,200))
        self.donut_size = self.donut.get_size()

        self.ant_image = pygame.image.load("Images/ant.png")
        self.ant_image = pygame.transform.scale(self.ant_image, (50,50))

        self.obstacle_image = pygame.image.load("Images/antEater.png")
        self.obstacle_width = self.obstacle_image.get_width()
        self.obstacle_height = self.obstacle_image.get_height()

        self.blue_bg = (167, 199, 231)
        # self.bg_img = pygame.image.load("Images/BG.png")
        # self.bg_img = pygame.transform.scale(self.bg_img, (screen_width, screen_height))

        self.ants =[
                    Agent(position = Vector2(screen_width/2,screen_height - 100),
                          ant_image = self.ant_image,
                          vel = Vector2(0,0),
                          acc = Vector2(0,0)),
                    
                    Agent(position = Vector2(screen_width/2,screen_height - 100),
                          ant_image = self.ant_image,
                          vel = Vector2(0,0),
                          acc = Vector2(0,0)),
        
                    Agent(position = Vector2(screen_width/2,screen_height - 100),
                          ant_image = self.ant_image,
                          vel = Vector2(0,0),
                          acc = Vector2(0,0)),
                    
                    Agent(position = Vector2(screen_width/2,screen_height - 100),
                          ant_image = self.ant_image,
                          vel = Vector2(0,0),
                          acc = Vector2(0,0)),

                    Agent(position = Vector2(screen_width/2,screen_height - 100),
                          ant_image = self.ant_image,
                          vel = Vector2(0,0),
                          acc = Vector2(0,0)),

                    Agent(position = Vector2(screen_width/2,screen_height - 100),
                          ant_image = self.ant_image,
                          vel = Vector2(0,0),
                          acc = Vector2(0,0))
        ]
        
        #waypoint system
        self.waypoints = [Vector2(screen_width/2,screen_height + self.donut_size[0]), Vector2(400,700),Vector2(300,600),Vector2(800,500), Vector2(600,700), Vector2(400,400), Vector2(600, 50)]
        # self.current_waypoint_num = 0
        # self.target = self.waypoints[self.current_waypoint_num]
        self.current_waypoint_nums = [0,1,2,3,4,5,6]
        self.targets = [self.waypoints[self.current_waypoint_nums[0]],
                        self.waypoints[self.current_waypoint_nums[1]],
                        self.waypoints[self.current_waypoint_nums[2]],
                        self.waypoints[self.current_waypoint_nums[3]],
                        self.waypoints[self.current_waypoint_nums[4]],
                        self.waypoints[self.current_waypoint_nums[5]],
                        self.waypoints[self.current_waypoint_nums[6]]]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # to detect key pressed
            elif event.type == pygame.KEYDOWN:
                # esc pressed
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_target = Vector2(mouse_x - (self.obstacle_width / 2), mouse_y - (self.obstacle_height / 2))
        
    def update(self, delta_time):
        for i, ant in enumerate(self.ants):
            d = ant.position - self.targets[i]
            dist = d.length()
            if dist < 5:
                # the ant has reach the destination
                self.current_waypoint_nums[i] += 1
                if self.current_waypoint_nums[i] >= len(self.waypoints):
                    self.current_waypoint_nums[i] = 0
                    
                self.targets[i] = self.waypoints[self.current_waypoint_nums[i]]
            
            ant.seek_to(self.targets[i])
            ant.update(delta_time)
            ant.flee_from(self.mouse_target)
            # self.ball.arrive_to(self.target)
    
    def draw(self):
        self.screen.fill((self.blue_bg))
        # self.screen.blit(self.bg_img, (0,0))
        self.screen.blit(self.donut, ((screen_width/2) - (self.donut_size[0]/2), 0))
        for ant in self.ants:
            ant.draw(self.screen)
        self.screen.blit(self.obstacle_image, (self.mouse_target))
        pygame.display.flip()
        
    def run(self):
        while self.running:
            delta_time = self.clock.tick(60)  # limits FPS to 60
            self.handle_input()
            self.update(delta_time)
            self.draw()

        pygame.quit()
    
def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()

