import numpy as np
class KalmanFilter:
    def __init__(self,process_variance,measurement_variance):
        self.q=process_variance 
        self.r=measurement_variance
        self.p=1.0        
        self.x=0.0                    
        self.k=0.0
    def update(self, measurement):
        self.p=self.p+self.q 
        self.k=self.p/(self.p+self.r)
        self.x=self.x+self.k*(measurement-self.x)
        self.p=(1-self.k)*self.p 
        return self.x
    def reset(self, new_value):
        self.x = float(new_value)
        self.p = 1.0    
        return self.x  