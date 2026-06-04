import numpy as np
import pygame
import sys
Window_width=1280
Window_height=720
Grid_size=40
Colour_bg=(10,15,20)
Colour_grid=(20,42,35)
Colour_drone=(0,255,150)
Colour_thrust=(255,150,0)
class tacticalengine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((Window_width,Window_height))
        self.clock=pygame.time.Clock()
        self.is_running=True
        self.drone_x=Window_width//2
        self.drone_y=Window_height//2
        self.drone_speed=5
    def run(self):
            while self.is_running:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        self.is_running=False
                    elif event.type==pygame.KEYDOWN:
                            if event.key==pygame.K_ESCAPE:
                                self.is_running=False
                            
                keys=pygame.key.get_pressed()
                is_accelerating=False
                if keys[pygame.K_LEFT]:
                    self.drone_x-=self.drone_speed
                    is_accelerating=True
                if keys[pygame.K_RIGHT]:
                    self.drone_x+=self.drone_speed
                    is_accelerating=True 
                if keys[pygame.K_UP]:
                    self.drone_y-=self.drone_speed
                    is_accelerating=True
                if keys[pygame.K_DOWN]:
                    self.drone_y+=self.drone_speed
                    is_accelerating=True  
                self.drone_x=max(20,min(self.drone_x,Window_width-20))
                self.drone_y=max(20,min(self.drone_y,Window_height-20))
                self.screen.fill(Colour_bg)
                for x in range(0,Window_width,Grid_size):
                    pygame.draw.line(self.screen,Colour_grid,(x,0),(x,Window_height),1)
                for y in range(0,Window_height,Grid_size):  
                    pygame.draw.line(self.screen,Colour_grid,(0,y),(Window_width,y),1)
                if is_accelerating:
                   thrust_points=[
                    (self.drone_x-15,self.drone_y+10),
                    (self.drone_x-30,self.drone_y+20),
                    (self.drone_x-15,self.drone_y-10)
                   ]
                   pygame.draw.polygon(self.screen,Colour_thrust,thrust_points)
                ucav_points=[
                    (self.drone_x + 25, self.drone_y),  
                    (self.drone_x + 10, self.drone_y + 10), 
                    (self.drone_x - 15, self.drone_y + 20),  
                    (self.drone_x - 10, self.drone_y + 5),  
                    (self.drone_x - 15, self.drone_y),     
                    (self.drone_x - 10, self.drone_y - 5), 
                    (self.drone_x - 15, self.drone_y - 20), 
                    (self.drone_x + 10, self.drone_y - 10)   
                ]      
                pygame.draw.polygon(self.screen,Colour_drone,ucav_points,2)
                pygame.display.flip()
                self.clock.tick(60)
            pygame.quit()
            sys.exit()

if __name__=="__main__":
    engine=tacticalengine()
    engine.run()