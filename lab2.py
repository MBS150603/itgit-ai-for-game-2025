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
        screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.running = True

        self.ball = Agent()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # to detect key pressed
            elif event.type == pygame.KEYDOWN:
                # esc pressed
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass
    
    def draw(self):
        self.screen.fill("white")
        self.ball.draw(self.screen)
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()
    
def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()

