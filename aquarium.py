import pygame
import pygame_gui
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from fish_agent import Agent
from fish_food import Food
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
        
        self.fish_1_image = pygame.image.load("Images/fish_1.png")
        self.fish_2_image = pygame.image.load("Images/fish_2.png")
        self.fish_3_image = pygame.image.load("Images/fish_3.png")
        self.seahorse_image = pygame.image.load("Images/seahorse.png")
        self.jellyfish_image = pygame.image.load("Images/jellyfish.png")

        self.coralP_image = pygame.image.load("Images/coral_pink.png")
        self.coralG_image = pygame.image.load("Images/coral_green.png")
        self.coralB_image = pygame.image.load("Images/coral_blue.png")
        self.coralR_image = pygame.image.load("Images/coral_red.png")

        self.fish_food_image = pygame.image.load("Images/fish_food.png")
        self.fish_food_2_image = pygame.image.load("Images/fish_food_2.png")
        self.fish_food_3_image = pygame.image.load("Images/fish_food_3.png")

        self.agents = []
        self.agents_2 = []
        self.agents_3 = []
        self.seahorses = []
        self.jellyfishes = []
        self.avoid_targets = []

        self.food = []
        self.food_2 = []
        self.food_3 = [
                    Food(position = Vector2(80,600), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(300,400), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(700,600), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(750,300), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(1000,500), 
                        fish_food_image = self.fish_food_3_image)
                    ]
        self.food_gravity = Vector2(0,0.1)
        self.isFood = False
        self.isFood2 = False
        self.isFood3 = True

        self.f1_hunger_cooldown = 0
        self.f2_hunger_cooldown = 0
        self.f3_hunger_cooldown = 0
        self.f2_pos_timer = 0
        self.seahorse_give_food_timer = 0
        self.food3_respawn_timer = 0

        # self.agents[0].mass = 10
        # self.agents[1].mass = 10
        # self.agents[2].mass = 10

        for i in range(10):
            agent = Agent(position=Vector2(random.randint(100,screen_width) , random.randint(100,screen_height)),
                          fish_image = self.fish_1_image,
                          hungry = False)
            agent.mass = 50
            self.agents.append(agent)

        for i in range(5):
            agent = Agent(position=Vector2(random.randint(100,screen_width) , random.randint(500,screen_height)),
                          fish_image = self.fish_2_image,
                          hungry = False)
            agent.mass = 50
            self.agents_2.append(agent)

        for i in range(15):
            agent = Agent(position=Vector2(random.randint(100,screen_width) , random.randint(500,screen_height)),
                          fish_image = self.fish_3_image,
                          hungry = False)
            agent.mass = 50
            self.agents_3.append(agent)
        
        for i in range(7):
            agent = Agent(position=Vector2(random.randint(-10,screen_width/2) , random.randint(-10,screen_height-500)),
                          fish_image = self.seahorse_image,
                          hungry = False)
            agent.mass = 50
            self.seahorses.append(agent)

        for i in range(9):
            agent = Agent(position=Vector2(random.randint(10,screen_width) , random.randint(10,screen_height)),
                          fish_image = self.jellyfish_image,
                          hungry = False)
            agent.mass = 50
            agent.set_gravity(Vector2(random.uniform(-0.01,0.1),-0.1))
            self.jellyfishes.append(agent)

        #Way point
        # self.waypoints = [Vector2(200,200), Vector2(400,600), Vector2(600,300), Vector2(800, 700), Vector2(1000, 50)]

        # self.current_waypoints = [0, 1, 2, 3, 4]
        # self.targets = [
        #     self.waypoints[self.current_waypoints[random.randint(0,4)]],
        #     self.waypoints[self.current_waypoints[random.randint(0,4)]],
        #     self.waypoints[self.current_waypoints[random.randint(0,4)]],
        #     self.waypoints[self.current_waypoints[random.randint(0,4)]],
        #     self.waypoints[self.current_waypoints[random.randint(0,4)]],
        #     self.waypoints[self.current_waypoints[random.randint(0,4)]],
        #     self.waypoints[self.current_waypoints[random.randint(0,4)]]
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

    # def get_food_position(self, food_pos):
    #     self.food_position.append(food_pos)

    def handle_input(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.target = Vector2(mouse_x,mouse_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # to detect key pressed
            elif event.type == pygame.KEYDOWN:
                # esc pressed
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 1 == left button
                    print("Food1")
                    self.isFood = True
                    self.food += [Food(position = self.target + Vector2(random.randint(-10,10) , random.randint(-10,10)),
                                fish_food_image = self.fish_food_image)]
                if event.button == 3: # 3 == right button
                    print("Food2")
                    self.isFood2 = True
                    self.food_2 += [Food(position = self.target + Vector2(random.randint(-10,10) , random.randint(-10,10)),
                                fish_food_image = self.fish_food_2_image)]

    def update(self, delta_time_s):
        self.f1_hunger_cooldown += delta_time_s
        self.f2_hunger_cooldown += delta_time_s
        self.f3_hunger_cooldown += delta_time_s
        self.seahorse_give_food_timer += delta_time_s

        if self.isFood == True:
            for f in self.food:
                f_cohe = f.get_cohesion_force(self.food)
                f.apply_force(f_cohe)

                f_sep = f.get_separation_force(self.food)
                f.apply_force(f_sep)

                # f_align = f.get_align_force(self.food)
                # f.apply_force(f_align)

                if math.floor(f.position.y) >= (screen_height - 50):
                    self.food.remove(f)
                    # print("Gone")
                if self.food == []:
                    self.isFood = False

                f.set_gravity(self.food_gravity)
                f.update(delta_time_s)
                # print(self.food)

        if self.isFood2 == True:
            for f in self.food_2:
                f_cohe = f.get_cohesion_force(self.food_2)
                f.apply_force(f_cohe)

                f_sep = f.get_separation_force(self.food_2)
                f.apply_force(f_sep)

                # f_align = f.get_align_force(self.food_2)
                # f.apply_force(f_align)

                if math.floor(f.position.y) >= (screen_height - 50):
                    self.food_2.remove(f)
                    # print("Gone")
                if self.food_2 == []:
                    self.isFood2 = False

                f.set_gravity(self.food_gravity)
                f.update(delta_time_s)
                # print(self.food)

        for agent in self.agents:
            if self.f1_hunger_cooldown >= 5:
                agent.hungry = True

            target = (agent.position - agent.center_of_mass)
            target.y = random.randint(50, screen_height/2)

            if self.isFood == True and agent.hungry == True:
                for s in self.food:
                    target = s.position
                    distance = (agent.position - target).length()
                    if distance < 20:
                        # print(s.position)
                        self.food.remove(s)
                        self.f1_hunger_cooldown = 0
                        agent.hungry = False

            cohesion_f = agent.get_cohesion_force(self.agents)
            agent.apply_force(cohesion_f)

            # target = self.target
            separation_f = agent.get_separation_force(self.agents)
            agent.apply_force(separation_f)

            align_f = agent.get_align_force(self.agents)
            agent.apply_force(align_f)

            agent.seek_to(target)
            agent.update(delta_time_s)
            self.bound_check(agent)

            for i,jelly in enumerate(self.jellyfishes):
                agent.flee_from(self.jellyfishes[i].position)

            for i,agent in enumerate(self.agents_2):
                agent.flee_from(self.agents_2[i].center_of_mass)

            for i,agent in enumerate(self.agents_3):
                agent.flee_from(self.agents_3[i].center_of_mass)

            for i,seahorse in enumerate(self.seahorses):
                agent.flee_from(self.seahorses[i].center_of_mass)

            for i,f in enumerate(self.food_3):
                agent.flee_from(self.food_3[i].position)

        # self.manager.update(delta_time_s)

        self.f2_pos_timer += delta_time_s
        for agent in self.agents_2:
            if self.f2_hunger_cooldown >= 7:
                agent.hungry = True
            # print(agent.hungry)

            target = agent.position - agent.center_of_mass
            target.y = random.randint(300, screen_height-100)
            # if self.f2_pos_timer >= 15:
            #     target = Vector2(200,screen_height - 100)
            #     if self.f2_pos_timer >= 16:
            #         self.f2_pos_timer = 0

            cohesion_f = agent.get_cohesion_force(self.agents_2)
            agent.apply_force(cohesion_f)

            separation_f = agent.get_separation_force(self.agents_2)
            agent.apply_force(separation_f)

            # align_f = agent.get_align_force(self.agents_2)
            # agent.apply_force(align_f)


            if self.isFood3 == True and agent.hungry == True:
                for i, s in enumerate(self.food_3):
                    target = s.position
                    distance = (agent.position - target).length()
                    if distance < 10:
                        print("hit")
                        self.food_3.remove(s)
                        self.f2_hunger_cooldown = 0
                        agent.hungry = False
            if self.food_3 == []:
                self.food3_respawn_timer += delta_time_s
                self.isFood3 = False

            if self.food3_respawn_timer >= 5 and self.isFood3 == False:
                self.food_3 = [
                    Food(position = Vector2(80,600), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(300,400), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(700,600), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(750,300), 
                        fish_food_image = self.fish_food_3_image),
                    Food(position = Vector2(1000,500), 
                        fish_food_image = self.fish_food_3_image)
                ]
                self.isFood3 = True
                self.food3_respawn_timer = 0
            print(self.food3_respawn_timer)
            print(self.isFood3)

            agent.seek_to(target)
            agent.update(delta_time_s)
            self.bound_check(agent)

            for i,jelly in enumerate(self.jellyfishes):
                agent.flee_from(self.jellyfishes[i].position)

            # for i,agent in enumerate(self.agents_3):
            #     agent.flee_from(self.agents_3[i].center_of_mass)

            # for i,seahorse in enumerate(self.seahorses):
            #     seahorse.flee_from(self.seahorses[i].center_of_mass)

        for agent in self.agents_3:
            if self.f3_hunger_cooldown >= 15:
                agent.hungry = True
            # print(agent.hungry)

            target = (agent.center_of_mass + agent.position)
            target.y = random.randint(screen_height/2, screen_height-10)

            if self.isFood2 == True and agent.hungry == True:
                for s in self.food_2:
                    target = s.position
                    distance = (agent.position - target).length()
                    if distance < 20:
                        # print(s.position)
                        self.food_2.remove(s)
                        self.f3_hunger_cooldown = 0
                        agent.hungry = False

            cohesion_f = agent.get_cohesion_force(self.agents_3)
            agent.apply_force(cohesion_f)

            # target = self.target
            separation_f = agent.get_separation_force(self.agents_3)
            agent.apply_force(separation_f)

            align_f = agent.get_align_force(self.agents_3)
            agent.apply_force(align_f)

            agent.seek_to(target)
            agent.update(delta_time_s)
            self.bound_check(agent)

            for i,jelly in enumerate(self.jellyfishes):
                agent.flee_from(self.jellyfishes[i].position)

            for i,seahorse in enumerate(self.seahorses):
                seahorse.flee_from(self.seahorses[i].center_of_mass)

            for i,f in enumerate(self.food_3):
                agent.flee_from(self.food_3[i].position)
        # self.manager.update(delta_time_s)

        for seahorse in self.seahorses:
            target = (seahorse.center_of_mass + seahorse.position)
            # target.x = random.randint(0, screen_width-50)

            if self.seahorse_give_food_timer >= 2:
                self.isFood = True
                seahorse_food = Food(position = seahorse.center_of_mass + Vector2(random.randint(-100,30) , random.randint(-30,300)),
                                fish_food_image = self.fish_food_image)
                self.food.append(seahorse_food)
                self.seahorse_give_food_timer = 0

            cohesion_f = seahorse.get_cohesion_force(self.seahorses)
            seahorse.apply_force(cohesion_f)

            # target = self.target
            separation_f = seahorse.get_separation_force(self.seahorses)
            seahorse.apply_force(separation_f)

            align_f = seahorse.get_align_force(self.seahorses)
            seahorse.apply_force(align_f)

            seahorse.arrive_to(target)
            seahorse.update(delta_time_s)
            self.bound_check(seahorse)
            
            for i,jelly in enumerate(self.jellyfishes):
                seahorse.flee_from(self.jellyfishes[i].position)

            for i,f in enumerate(self.food_3):
                seahorse.flee_from(self.food_3[i].position)

        for jelly in self.jellyfishes:
            # jelly.target = Vector2(random.randint(-(screen_width/2),screen_width) , random.randint(-(screen_height/2),screen_height))
            # target = jelly.position - jelly.vel
            # jelly.target = target

            target = (jelly.center_of_mass + jelly.position)
            target.x = random.randint(-50, 0)

            cohesion_f = jelly.get_cohesion_force(self.jellyfishes)
            jelly.apply_force(cohesion_f)

            # target = self.target
            separation_f = jelly.get_separation_force(self.jellyfishes)
            jelly.apply_force(separation_f)

            align_f = jelly.get_align_force(self.jellyfishes)
            jelly.apply_force(align_f)

            jelly.seek_to(target)
            jelly.update(delta_time_s)
            self.bound_check(jelly)
    
            for i,f in enumerate(self.food_3):
                jelly.flee_from(self.food_3[i].position)
        # self.manager.update(delta_time_s)

    def draw(self):
        self.screen.fill((32, 35, 84))
        self.screen.blit(self.coralR_image, (-10, screen_height - 500))
        self.screen.blit(self.coralG_image, (10, screen_height - 400))
        self.screen.blit(self.coralG_image, (800, screen_height - 400))
        self.screen.blit(self.coralG_image, (400, screen_height - 200))
        self.screen.blit(self.coralB_image, (250, screen_height - 300))
        self.screen.blit(self.coralB_image, (600, screen_height - 250))
        self.screen.blit(self.coralP_image, (200, screen_height - 200))
        self.screen.blit(self.coralP_image, (600, screen_height - 200))
        self.screen.blit(self.coralR_image, (700, screen_height - 600))
        self.screen.blit(self.coralB_image, (1000, screen_height - 300))

        for agent in self.agents:
            agent.draw(self.screen)
        for agent in self.agents_2:
            agent.draw(self.screen)
        for agent in self.agents_3:
            agent.draw(self.screen)
        for seahorse in self.seahorses:
            seahorse.draw(self.screen)
        for jelly in self.jellyfishes:
            jelly.draw(self.screen)

        if self.isFood == True:
            for f in self.food:
                f.draw(self.screen)
        if self.isFood2 == True:
            for f in self.food_2:
                f.draw(self.screen)
        if self.isFood3 == True:
            for f in self.food_3:
                f.draw(self.screen)
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