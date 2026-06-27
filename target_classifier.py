import numpy as np
from sklearn.tree import DecisionTreeClassifier

class RadarContactClassifier:
    def __init__(self):
        np.random.seed(42)
        X_train=[]
        y_train=[]
        self.class_labels = {0:"FRIENDLY",1:"BOGEY(UNKNOWN)", 2:"HOSTILE"}
        for _ in range(200):
            X_train.append([np.random.uniform(10.0,30.0),np.random.uniform(700, 950),np.random.uniform(400, 1000)])
            y_train.append(0)
            X_train.append([np.random.uniform(0.01,0.5),np.random.uniform(50, 150),np.random.uniform(200, 800)])
            y_train.append(1)
            X_train.append([np.random.uniform(1.0,8.0),np.random.uniform(1500, 2500),np.random.uniform(0, 350)])
            y_train.append(2)
        self.X_data=np.array(X_train)
        self.y_data=np.array(y_train)
        self.model=DecisionTreeClassifier(max_depth=3,random_state=42)
        self.model.fit(self.X_data,self.y_data)
    def classify_contact(self,rcs_size,speed_kmh,distance_px):
        sample=np.array([[rcs_size,speed_kmh,distance_px]])
        predicted_idx=self.model.predict(sample)[0]
        return self.class_labels[predicted_idx]