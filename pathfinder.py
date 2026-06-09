import math
class A_star:
    def __init__(self,width,height,grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
    def get_neighbors(self,node):
        x,y=node
        neighbors=[]
        moves=[(-self.grid_size,0),(self.grid_size,0),(0,-self.grid_size),(0,self.grid_size),(-self.grid_size,-self.grid_size),(-self.grid_size,self.grid_size),(self.grid_size,-self.grid_size),(self.grid_size,self.grid_size)]
        for dx,dy in moves:
            nx,ny=x+dx,y+dy
            if 0<=nx<self.width and 0<=ny<self.height:
                neighbors.append((nx,ny))
        return neighbors
    def calc_heuristic(self,node,target):
        return math.sqrt((node[0]-target[0])**2+(node[1]-target[1])**2)
    def compute_flight_path(self,start,target,radar_zones):
        start_node=(int(start[0]//self.grid_size)*self.grid_size, 
                      int(start[1]//self.grid_size)*self.grid_size)
        target_node=(int(target[0]//self.grid_size)*self.grid_size, 
                     int(target[1]//self.grid_size)*self.grid_size)              
        open_set={start_node}
        came_from={}
        g_score={start_node: 0.0}
        f_score={start_node: self.calc_heuristic(start_node, target_node)}
        while open_set:
            current = min(open_set, key=lambda node: f_score.get(node, float('inf')))
            if current==target_node:
                path=[]
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            open_set.remove(current)
            for neighbor in self.get_neighbors(current):
                step_cost = self.calculate_heuristic(current, neighbor)
                threat_penalty = 0.0
                for radar in radar_zones:
                    dx=neighbor[0]-radar["x"]
                    dy=neighbor[1]-radar["y"]
                    dist_to_radar=math.sqrt(dx**2 + dy**2)
                    if dist_to_radar<radar["radius"]:
                        intensity_gradient=(1.0-(dist_to_radar/radar["radius"]))
                        threat_penalty+=intensity_gradient*5000.0
            tentative_g_score=g_score[current]+step_cost+threat_penalty
                if tentative_g_score<g_score.get(neighbor, float('inf')):
                    came_from[neighbor]=current
                    g_score[neighbor]=tentative_g_score
                    f_score[neighbor]=tentative_g_score+self.calculate_heuristic(neighbor, goal_node)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return []              