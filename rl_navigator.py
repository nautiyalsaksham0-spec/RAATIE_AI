import numpy as np
import json
class QLearningNavigator:
    def __init__(self):
        self.q_table={}
        self.alpha=0.1
        self.gamma=0.9
        self.epsilon=0.2
    def get_action(self, state):
        if state not in self.q_table:self.q_table[state]=np.zeros(4)
        if np.random.rand()<self.epsilon: return np.random.randint(0, 4)
        return np.argmax(self.q_table[state])
    def learn(self,state,action,reward,next_state):
        if state not in self.q_table: self.q_table[state] = np.zeros(4)
        if next_state not in self.q_table:self.q_table[next_state] = np.zeros(4)
        old_val=self.q_table[state][action]
        next_max=np.max(self.q_table[next_state])
        self.q_table[state][action] += self.alpha *(reward + self.gamma * next_max - old_val)
    def save_brain(self, filename="ucav_brain.json"):
        serializable={str(k): v.tolist() for k, v in self.q_table.items()}
        with open(filename,'w') as f:json.dump(serializable,f)