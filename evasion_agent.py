import numpy as np
class EvasionAgent:
    def __init__(self):
        self.q_table={}
        self.lr=0.1
        self.gamma=0.9
    def get_action(self, state):
        if state not in self.q_table: self.q_table[state]=np.zeros(3)
        return np.argmax(self.q_table[state])
    def learn(self,state,action,reward,next_state):
        if state not in self.q_table:self.q_table[state]=np.zeros(3)
        old_val=self.q_table.get(state, np.zeros(3))[action]
        next_max=np.max(self.q_table.get(next_state,np.zeros(3)))
        self.q_table[state][action]+=self.lr*(reward+self.gamma*next_max-old_val)