import numpy as np
class RadarConfidenceTracker:
    def __init__(self):
        self.confidence=0.0
    def update(self,signal_strength,is_stealth_target):
        gain=0.1 if not is_stealth_target else 0.02
        decay=0.05
        self.confidence+=gain*signal_strength
        self.confidence-=decay
        self.confidence=np.clip(self.confidence,0.0,1.0)
        return self.confidence