import pygame
from pygame.draw import circle
from pygame.math import Vector2
import random
from agent import Agent

screen_width = 1270
screen_height = 720

class App:
    def __init__(self):
        print("Application is created")

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.ball = Agent(position = Vector2(screen_width/2,screen_height/2),
                          radius = 100,
                          color = (100,50,225),
                          vel = Vector2(0,0),
                          acc = Vector2(0,0))

        self.target = Vector2(0,0)

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
        self.target = Vector2(mouse_x, mouse_y) 

    def update(self, delta_time):
        self.ball.seek_to(self.target)
        self.ball.update(delta_time)
    
    def draw(self):
        self.screen.fill("white")
        self.ball.draw(self.screen)
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

