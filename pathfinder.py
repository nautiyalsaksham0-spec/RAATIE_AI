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
        start_node = (int(start[0]//self.grid_size)*self.grid_size, 
                      int(start[1]//self.grid_size)*self.grid_size)
        target_node = (int(target[0]//self.grid_size)*self.grid_size, 
                     int(target[1]//self.grid_size)*self.grid_size)              
        open_set = {start_node}