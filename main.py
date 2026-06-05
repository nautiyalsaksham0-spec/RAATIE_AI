import numpy as np
import pygame
import sys
import math
Window_width=1280
Window_height=720
Grid_size=40
Colour_bg=(10,15,20)
Colour_grid=(20,42,35)
Colour_drone=(0,255,150)
Colour_thrust=(255,150,0)
Colour_text=(255, 255, 255) 
Colour_alert=(255, 50, 50)
class tacticalengine:
    def __init__(self):
        pygame.font.init()
        pygame.init()
        self.screen=pygame.display.set_mode((Window_width,Window_height))
        self.clock=pygame.time.Clock()
        self.is_running=True
        self.drone_x=Window_width//2
        self.drone_y=Window_height//2
        self.drone_speed=5
        pygame.display.set_caption("RAATIE_AI:flight and threat engine")
        self.font=pygame.font.SysFont("Consolas",16)
        self.alert_font=pygame.font.SysFont("Consolas",20,bold=True)        
        self.radar_zones = [
            {"x": 300,  "y": 250, "radius": 150},
            {"x": 950,  "y": 200, "radius": 180},  
            {"x": 640,  "y": 550, "radius": 130}   
        ]
        self.active_risk_per=0.0
    def cal_threat(self):
        max_risk=0.0
        for radar in self.radar_zones:
            distance=math.sqrt((self.drone_x-radar["x"])**2+(self.drone_y-radar["y"])**2)
            if distance<radar["radius"]:
               current_risk=(1-(distance/radar["radius"]))*100
               if current_risk>max_risk:
                    max_risk=current_risk
        return round(max_risk,1)      
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
                self.active_risk_per=self.cal_threat()
                self.screen.fill(Colour_bg)
                for x in range(0,Window_width,Grid_size):
                    pygame.draw.line(self.screen,Colour_grid,(x,0),(x,Window_height),1)
                for y in range(0,Window_height,Grid_size):  
                    pygame.draw.line(self.screen,Colour_grid,(0,y),(Window_width,y),1)
                for radar in self.radar_zones:
                    surface_size=radar["radius"]*2
                    radar_sur=pygame.Surface((surface_size,surface_size),pygame.SRCALPHA)
                    pygame.draw.circle(radar_sur,(255,50,50,45),(radar['radius'],radar["radius"]),radar["radius"])
                    pygame.draw.circle(radar_sur, (255, 50, 50, 120), (radar["radius"], radar["radius"]), radar["radius"], 1)
                    self.screen.blit(radar_sur, (radar["x"] - radar["radius"], radar["y"] - radar["radius"]))
                    pygame.draw.circle(self.screen,Colour_alert,(radar["x"],radar["y"]),3)
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
                current_drone_color = Colour_alert if self.active_risk_per > 0 else Colour_drone    
                pygame.draw.polygon(self.screen,current_drone_color,ucav_points,2)
                pygame.draw.rect(self.screen, (5, 8, 12), (15, 15, 300, 100))
                pygame.draw.rect(self.screen, Colour_grid, (15, 15, 300, 100), 1)
                txtpos=f"Ucav Coords x:[{int (self.drone_x)}] y:[{int(self.drone_y)}]"
                txtrisk=f"Threat level:{self.active_risk_per}%"
                if self.active_risk_per > 0:
                 txt_status = "SYSTEM STATUS: WARNING - RADAR LOCK DETECTED"
                 status_color = Colour_alert
                else:
                 txt_status = "SYSTEM STATUS: AIRSPACE CLEAR"
                 status_color = Colour_drone
                self.screen.blit(self.font.render(txtpos, True, Colour_text), (25, 25))
                self.screen.blit(self.font.render(txtrisk, True, status_color), (25, 50))
                self.screen.blit(self.font.render(txt_status, True, status_color), (25, 75))
                pygame.display.flip()
                self.clock.tick(60)
            pygame.quit()
            sys.exit()

if __name__=="__main__":
    engine=tacticalengine()
    engine.run()