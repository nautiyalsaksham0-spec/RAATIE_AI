import numpy as np
from kalman_fusion import KalmanFilter
class BVRMissile:
    def __init__(self, start_pos, target_pos, target_vel):
        self.pos = np.array(start_pos, dtype=float)
        self.vel = np.array(target_vel, dtype=float)
        self.kf_x = KalmanFilter(0.1, 10.0)
        self.kf_y = KalmanFilter(0.1, 10.0) 
        self.n = 5.0  
        self.speed = 1.0
        self.active = True
        self.age = 0
    def update(self, target_pos,target_type):
        if not self.active: 
            return "INACTIVE"
        if target_type == "FRIENDLY":
           self.active = False
           return "INACTIVE"
        self.age += 1
        if self.age > 500: 
            self.active = False
            return "INACTIVE"
        tx, ty = float(target_pos[0]), float(target_pos[1])
        pred_x = self.kf_x.update(tx)
        pred_y = self.kf_y.update(ty)
        predicted_pos = np.array([pred_x, pred_y])
        direction = predicted_pos - self.pos
        dist = np.linalg.norm(direction)
        
        if dist < 50.0:
            self.active = False
            return "EXPLODE"
        los_rate = np.cross(direction, self.vel) / (dist**2)
        accel = self.n * self.speed * los_rate
        angle = accel * 0.1
        rot = np.array([[np.cos(angle), -np.sin(angle)], 
                        [np.sin(angle), np.cos(angle)]])
        
        self.vel = np.dot(rot, self.vel)
        self.pos += self.vel
        speed_magnitude = np.linalg.norm(self.vel)
        self.vel = (self.vel / speed_magnitude) * self.speed
        return "FLYING"
        