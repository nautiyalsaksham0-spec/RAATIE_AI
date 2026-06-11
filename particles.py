import random
import pygame
class ParticleEmitter:
    def __init__(self):
        self.particles = []
    def trigger_explosion(self, x, y, color):
        for _ in range(30):
            particle_data = {
                "x": float(x),
                "y": float(y),
                "vx": random.uniform(-4.0, 4.0),
                "vy": random.uniform(-4.0, 4.0),
                "radius": random.randint(2, 5),
                "lifetime": 1.0,
                "decay": random.uniform(0.04, 0.08),
                "color": color
            }
            self.particles.append(particle_data)
    def update_and_render(self, screen):
        for particle in self.particles[:]:
            particle["x"]+=particle["vx"]
            particle["y"]+=particle["vy"]
            particle["lifetime"]-=particle["decay"]

            if particle["lifetime"]<=0:
                self.particles.remove(particle)
            else:
                alpha=max(0,min(255,int(particle["lifetime"]*255)))
                particle_surface = pygame.Surface((particle["radius"] * 2, particle["radius"] * 2), pygame.SRCALPHA)
                r,g,b=particle["color"]
                pygame.draw.circle(particle_surface,(r,g,b,alpha),(particle["radius"],particle["radius"]),particle["radius"])                
                screen.blit(particle_surface, (int(particle["x"] - particle["radius"]), int(particle["y"] - particle["radius"])))        