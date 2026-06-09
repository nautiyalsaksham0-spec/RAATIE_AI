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
Colour_target=(255,215,0)
Colour_vector=(0,180,255)
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
            {"x": 380,  "y": 280, "radius": 150},
            {"x": 950,  "y": 200, "radius": 180},  
            {"x": 640,  "y": 550, "radius": 130}   
        ]
        self.active_risk_per=0.0
        self.target_x = 100
        self.target_y = 100
        self.target_speed_x = 2.0 
        self.target_speed_y = 1.5
        self.target_speed_inkmh=1200
        self.target_rcs_size = 5.5
        self.target_priority = "LOW"
        self.planner=AStarPlanner(Window_width, Window_height, Grid_size)
        self.calculated_flight=[]
    def cal_threat(self):
        max_risk=0.0
        for radar in self.radar_zones:
            distance=math.sqrt((self.drone_x-radar["x"])**2+(self.drone_y-radar["y"])**2)
            if distance<radar["radius"]:
               current_risk=(1-(distance/radar["radius"]))*100
               if current_risk>max_risk:
                    max_risk=current_risk
        return round(max_risk,1)      
    def evaluate_target(self,distance_to_target):
           if distance_to_target <300 or self.target_speed_inkmh > 2000:
              return"CRITICAL THREAT"
           elif distance_to_target < 600 and self.target_rcs_size > 2.0:
              return"TACTICAL ENGANGEMENT"
           else:
            return"LOW PRIORITY"  
    def update_target_kinematics(self):
        self.target_x += self.target_speed_x
        self.target_y += self.target_speed_y  
        if self.target_x <= 30 or self.target_x>=Window_width-30:
            self.target_speed_x *= -1  
        if self.target_y <= 30 or self.target_y>=Window_height-30:
            self.target_speed_y *= -1      
    def run(self):
            while self.is_running:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        self.is_running=False
                    elif event.type==pygame.KEYDOWN:
                            if event.key==pygame.K_ESCAPE:
                                self.is_running=False
            self.update_target_kinematics()
            distance_to_target=math.sqrt((self.drone_x - self.target_x)**2 + (self.drone_y - self.target_y)**2)
            self.target_priority=self.evaluate_target(distance_to_target)
            self.calculated_flight=self.planner.compute_flight_path(
                (self.drone_x,self.drone_y), 
                (self.target_x,self.target_y), 
                self.radar_zones
            )
            is_accelerating = False
            if self.calculated_flight:
                next_waypoint=self.calculated_flight[0]
                is_accelerating=True
                dx=next_waypoint[0]-self.drone_x
                dy=next_waypoint[1]-self.drone_y
                step_distance=math.sqrt(dx**2+dy**2)
                if step_distance>0:
                    self.drone_x+=(dx/step_distance)*self.drone_speed
                    self.drone_y+=(dy/step_distance)*self.drone_speed                
                            
              
                
                      
                self.drone_x=max(20,min(self.drone_x,Window_width-20))
                self.drone_y=max(20,min(self.drone_y,Window_height-20))
                self.active_risk_per=self.cal_threat()
                self.update_target_kinematics()
                distance_to_target = math.sqrt((self.drone_x - self.target_x)**2 + (self.drone_y - self.target_y)**2)
                self.target_priority=self.evaluate_target(distance_to_target)
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
                pygame.draw.line(self.screen,Colour_vector,(self.drone_x,self.drone_y),(self.target_x,self.target_y),1)
                target_diamond_points = [
                (self.target_x, self.target_y - 12),
                (self.target_x + 12, self.target_y),  
                (self.target_x, self.target_y + 12),  
                (self.target_x - 12, self.target_y)   ]
                pygame.draw.polygon(self.screen, Colour_target, target_diamond_points, 2)
                pygame.draw.rect(self.screen, Colour_alert, (self.target_x - 3, self.target_y - 3, 6, 6))
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
                pygame.draw.rect(self.screen, (5, 8, 12), (15, 15, 340, 140))
                pygame.draw.rect(self.screen, Colour_grid, (15, 15, 340, 140), 1)
                txtpos=f"Ucav Coords x:[{int (self.drone_x)}] y:[{int(self.drone_y)}]"
                txtrisk=f"Threat level:{self.active_risk_per}%"
                txt_tgt_dist=f"TARGET DISTANCE:{int(distance_to_target)}px"
                txt_targt=f"TARGET EVALUATION:{self.target_priority}"
                if self.active_risk_per>0:
                 txt_status = "SYSTEM STATUS: WARNING - RADAR LOCK DETECTED"
                 status_color = Colour_alert
                else:
                 txt_status = "SYSTEM STATUS: AIRSPACE CLEAR"
                 status_color = Colour_drone
                if self.target_priority=="CRITICAL THREAT":
                 priority_color = Colour_alert
                elif self.target_priority=="TACTICAL ENGAGEMENT":
                 priority_color = Colour_target
                else:
                 priority_color = Colour_vector
                self.screen.blit(self.font.render(txtpos, True, Colour_text), (25, 25))
                self.screen.blit(self.font.render(txtrisk, True, status_color), (25, 50))
                self.screen.blit(self.font.render(txt_status, True, status_color), (25, 75))
                self.screen.blit(self.font.render(txt_tgt_dist, True, Colour_text), (25, 100))
                self.screen.blit(self.font.render(txt_targt, True, priority_color), (25, 125))
                pygame.display.flip()
                self.clock.tick(60)
            pygame.quit()
            sys.exit()

if __name__=="__main__":
    engine=tacticalengine()
    engine.run()