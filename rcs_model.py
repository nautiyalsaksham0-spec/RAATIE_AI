import math
class StealthModel:
    def __init__(self):
        self.base_rcs_nose=0.01
        self.base_rcs_side=0.50
    def calculate_aspect_rcs(self, drone_pos, target_pos, radar_pos):
        flight_dx = target_pos[0] - drone_pos[0]
        flight_dy = target_pos[1] - drone_pos[1]
        flight_angle = math.atan2(flight_dy, flight_dx)  
        radar_dx = radar_pos["x"] - drone_pos[0]
        radar_dy = radar_pos["y"] - drone_pos[1]
        radar_angle = math.atan2(radar_dy, radar_dx)
        relative_angle = abs(flight_angle - radar_angle) % (2 * math.pi)  
        if relative_angle > math.pi:
            relative_angle=(2*math.pi)-relative_angle
        exposure_factor = abs(math.sin(relative_angle))
        current_rcs = self.base_rcs_nose + (self.base_rcs_side - self.base_rcs_nose) * exposure_factor
        return round(current_rcs, 3)    