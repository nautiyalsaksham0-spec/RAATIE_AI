import numpy as np
class BVRMissile:
    def __init__(self,start_pos,target_pos,target_vel,speed=15.0):
        self.pos=np.array(start_pos,dtype=float)
        self.velocity_vector=np.array([speed, 0.0],dtype=float) 
        self.speed=speed
        self.target_pos=np.array(target_pos,dtype=float)
        self.target_vel=np.array(target_vel,dtype=float)
        self.active=True
        self.n=3.5
    def update(self,current_target_pos):
        if not self.active: return "INACTIVE"
        self.target_pos=np.array(current_target_pos,dtype=float)
        direction=self.target_pos - self.pos
        distance=np.linalg.norm(direction)
        if distance<15.0:
            self.active=False
            return "EXPLODE"
        relative_vel=self.target_vel-self.velocity_vector
        los_rate=np.cross(direction,relative_vel)/(distance**2)
        acceleration=self.n*self.speed*los_rate
        angle=acceleration*0.1
        rotation_matrix = np.array([[np.cos(angle),-np.sin(angle)], 
                                    [np.sin(angle),np.cos(angle)]])
        self.velocity_vector=np.dot(rotation_matrix,self.velocity_vector)
        self.pos += self.velocity_vector
        return "FLYING"