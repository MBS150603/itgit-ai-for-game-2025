import pygame
from pygame.draw import circle, polygon, rect
from pygame.math import Vector2
import random

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

        self.circle_color = (100,50,225)
        self.radius = 100
        self.position = Vector2(screen_width/2, screen_height/2)
        self.vel = Vector2(0,0)
        self.acc = Vector2(2,2)

    def handle_input(self):
        self.running = False

    def update(self):
        self.vel += self.acc
        self.position += self.vel
        self.acc = Vector2(0,0)
    
    def draw(self):
        self.screen.fill("white")
        circle(self.screen,self.circle_color,self.position,self.radius)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # to detect key pressed
                elif event.type == pygame.KEYDOWN:
                    # esc pressed
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # fill the screen with a color to wipe away anything from last frame

            # RENDER YOUR GAME HERE

            if (self.position.x + self.radius) >= screen_width:
                self.acc.x = -1
                self.acc.y = random.randrange(0,1)

            if (self.position.y + self.radius) >= screen_height:
                self.acc.x = random.randrange(0,1)
                self.acc.y = -1

            if (self.position.x - self.radius) <= 0:
                self.acc.x = 1
                self.acc.y = random.randrange(0,1)

            if (self.position.y - self.radius) <= 0:
                self.acc.x = random.randrange(0,1)
                self.acc.y = 1            

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()
    
def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()

