import numpy as np
import pygame
import sys
import math
import random
from pathfinder import A_star
from particles import ParticleEmitter 
from rcs_model import StealthModel
from target_classifier import RadarContactClassifier
from kalman_fusion import KalmanFilter
from radar_intelligence import RadarConfidenceTracker
from evasion_agent import EvasionAgent
from rl_navigator import QLearningNavigator
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
        self.target_x=100.0
        self.target_y=100.0
        self.frame_count=0
        self.target_speed_x = 2.0 
        self.target_speed_y = 1.5
        self.target_speed_inkmh=1200
        self.target_rcs_size = 5.5
        self.target_priority = "LOW"
        self.planner=A_star(Window_width, Window_height, Grid_size)
        self.calculated_flight=[]
        self.emitter=ParticleEmitter()
        self.stealth_system=StealthModel()
        self.iff_classifier=RadarContactClassifier()
        self.target_x = 100.0
        self.target_y = 100.0
        self.kalman_x=KalmanFilter(process_variance=0.1,measurement_variance=10.0)
        self.kalman_x.x = self.target_x
        self.kalman_y=KalmanFilter(process_variance=0.1,measurement_variance=10.0)
        self.kalman_y.x=self.target_y
        self.ucav_brain=QLearningNavigator()
        self.enemy_brain = EvasionAgent()
        self.radar_tracker = RadarConfidenceTracker() 
        self.launch_threshold = 10
        self.last_radar_radius = 60
        self.state = "NAVIGATING"
    def cal_threat(self):
        max_risk=0.0
        for radar in self.radar_zones:
            distance=math.sqrt((self.drone_x-radar["x"])**2+(self.drone_y-radar["y"])**2)
            if distance<radar["radius"]:
               current_risk=(1-(distance/radar["radius"]))*100
               if current_risk>max_risk:
                    max_risk=current_risk
        return round(max_risk,1)        
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
            visual_x = self.kalman_x.update(self.target_x)
            visual_y = self.kalman_y.update(self.target_y)
            distance_to_target=math.sqrt((self.drone_x-self.target_x)**2+(self.drone_y-self.target_y)**2)
            self.target_priority = self.iff_classifier.classify_contact(
                rcs_size=self.target_rcs_size,
                speed_kmh=self.target_speed_inkmh,
                distance_px=distance_to_target 
            )
            signal=1.0-(distance_to_target / 1200) 
            conf=self.radar_tracker.update(signal_strength=max(0, signal))
            state=(int(self.drone_x//Grid_size),int(self.drone_y//Grid_size))
            self.active_risk_per = self.cal_threat()
            if self.active_risk_per > 80:
                self.state = "NAVIGATING"
            elif distance_to_target < 100 and self.target_priority == "HOSTILE":
                self.state = "ENGAGING"
            else:
                self.state = "NAVIGATING"
            is_accelerating=False
            if self.state=="NAVIGATING":
             self.frame_count+=1    
             if self.frame_count%5==0:
               self.calculated_flight=self.planner.compute_flight_path(
                 (self.drone_x,self.drone_y), 
                 (self.target_x,self.target_y), 
                 self.radar_zones
                )
             if self.calculated_flight:
                    next_waypoint = self.calculated_flight[0]
                    is_accelerating = True
                    dx = next_waypoint[0] - self.drone_x
                    dy = next_waypoint[1] - self.drone_y
                    step_distance = math.sqrt(dx**2 + dy**2)
                    if step_distance > 5:
                        self.drone_x += (dx / step_distance) * self.drone_speed
                        self.drone_y += (dy / step_distance) * self.drone_speed 
                    else:
                        self.calculated_flight.pop(0)
            elif self.state == "ENGAGING":           
             self.calculated_flight = []
             distance_to_target = math.sqrt((self.drone_x - self.target_x)**2 + (self.drone_y - self.target_y)**2)  
             if distance_to_target > 45:
                is_accelerating = True
                dx = self.target_x - self.drone_x
                dy = self.target_y - self.drone_y
                step_distance = math.sqrt(dx**2 + dy**2)
                if step_distance > 0: 
                        self.drone_x += (dx / step_distance) * self.drone_speed
                        self.drone_y += (dy / step_distance) * self.drone_speed
            else:
                is_accelerating = False                          
            self.drone_x=max(20,min(self.drone_x,Window_width-20))
            self.drone_y=max(20,min(self.drone_y,Window_height-20))
            if distance_to_target < 50 and self.target_priority == "HOSTILE":
                pygame.draw.line(self.screen, (255, 0, 0), (self.drone_x, self.drone_y), (self.target_x, self.target_y), 3)
                self.emitter.trigger_explosion(int(self.target_x),int(self.target_y),Colour_target)
                new_x=random.randint(80,Window_width-80)
                new_y=random.randint(80,Window_height-80)
                self.target_x = self.kalman_x.reset(new_x)
                self.target_y = self.kalman_y.reset(new_y) 
                self.target_speed_x=random.choice([-2.5, -2.0, 2.0, 2.5])
                self.target_speed_y=random.choice([-1.8, -1.2, 1.2, 1.8])
                self.target_speed_inkmh=random.randint(100, 2400)
                self.target_rcs_size=random.uniform(0.01, 25.0)
            self.screen.fill(Colour_bg)
            for x in range(0,Window_width,Grid_size):
                pygame.draw.line(self.screen,Colour_grid,(x,0),(x,Window_height),1)
            for y in range(0,Window_height,Grid_size):  
                pygame.draw.line(self.screen,Colour_grid,(0,y),(Window_width,y),1)
            for radar in self.radar_zones:
                current_rcs = self.stealth_system.calculate_aspect_rcs(
                    (self.drone_x, self.drone_y),
                    (self.target_x, self.target_y),
                    radar
                )
                target_radius = int(radar["radius"] * (current_rcs / 0.50))
                self.last_radar_radius = int(self.last_radar_radius * 0.9 + target_radius * 0.1)
                dynamic_radius = max(40, min(self.last_radar_radius, 200))
                surface_size=dynamic_radius*2
                radar_sur=pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
                pygame.draw.circle(radar_sur, (255, 50, 50, 45), (dynamic_radius, dynamic_radius), dynamic_radius)
                pygame.draw.circle(radar_sur, (255, 50, 50, 120), (dynamic_radius, dynamic_radius), dynamic_radius, 1)
                self.screen.blit(radar_sur, (radar["x"] - dynamic_radius, radar["y"] - dynamic_radius))
                pygame.draw.circle(self.screen, Colour_alert, (radar["x"], radar["y"]), 3)
            if len(self.calculated_flight) > 1:
                for i in range(len(self.calculated_flight) - 1):
                    p1 = self.calculated_flight[i]
                    p2 = self.calculated_flight[i+1]
                    pygame.draw.line(self.screen, Colour_vector, p1, p2, 2)
            if visual_x is not None and visual_y is not None:
                pygame.draw.line(self.screen, Colour_vector, (self.drone_x, self.drone_y), (int(visual_x), int(visual_y)), 1)
            else:
                pygame.draw.line(self.screen, Colour_vector, (self.drone_x, self.drone_y), (int(self.target_x), int(self.target_y)), 1)
            target_diamond_points = [
                (int(visual_x), int(visual_y) - 12),
                (int(visual_x) + 12, int(visual_y)),  
                (int(visual_x), int(visual_y) + 12),  
                (int(visual_x) - 12, int(visual_y)) 
            ]
            self.emitter.update_and_render(self.screen)
            pulse_speed=0.05
            pulse_val=(math.sin(pygame.time.get_ticks()*pulse_speed)+1)/2 
            if self.target_priority=="HOSTILE":
                draw_width=2+int(pulse_val*4)
            else:
                draw_width=2
            pygame.draw.polygon(self.screen, Colour_target, target_diamond_points, draw_width)
            pygame.draw.rect(self.screen, Colour_alert, (int(visual_x) - 3, int(visual_y) - 3, 6, 6))
            if is_accelerating:
                thrust_points=[
                    (self.drone_x-15,self.drone_y+10),
                    (self.drone_x-30,self.drone_y),
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
                txt_status = "SYSTEM STATUS: WARNING - RADAR LOCK DETECTED" if self.active_risk_per > 0 else "SYSTEM STATUS: AUTONOMOUS FLIGHT ACTIVE"
                status_color = Colour_alert if self.active_risk_per > 0 else Colour_drone
            else:
                txt_status="SYSTEM STATUS: AUTONOMOUS FLIGHT ACTIVE"
                status_color=Colour_drone
            if self.target_priority=="HOSTILE":
                priority_color=Colour_alert
            elif self.target_priority=="BOGEY(UNKNOWN)":
                priority_color=Colour_target
            else:
                priority_color=Colour_vector
            self.screen.blit(self.font.render(txtpos, True, Colour_text), (25, 25))
            self.screen.blit(self.font.render(txtrisk, True, status_color), (25, 50))
            self.screen.blit(self.font.render(txt_status, True, status_color), (25, 75))
            self.screen.blit(self.font.render(txt_tgt_dist, True, Colour_text), (25, 100))
            self.screen.blit(self.font.render(txt_targt, True, priority_color), (25, 125))
            if self.frame_count % 100 == 0:
                print(f"UCAV Brain: {len(self.ucav_brain.q_table)} states learned.")
                print(f"Enemy Brain: {len(self.enemy_brain.q_table)} evasion tactics learned.")
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__=="__main__":
    engine=tacticalengine()
    engine.run()