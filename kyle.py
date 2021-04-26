from api_interaction import *
import pandas as pd
import numpy as np

#10 worlds
#Each is 40x40
    #1600 states x 4 actions for each world
    #save all of these and output to pickle file

#returns the move you should do and updates the pickle file of all the new states
# def q_learning():
    #initialize the q table (number of actions x number of states)
        #all are 0

    #choose and perform an action --> could be random
        #action (a) in the state (s) is chosen based on the Q-Table
         #use epsilon greedy strategy
            #at first random, progressively becomes mroe confident

    #measure reward --> using reward from making move

    #Evaluate --> update the Q(s, a) function based on Bellman Equation
        #New Q value (s, a) = (Current Q values) + (Learning Rate)[(Reward for taking an action in a state) + (Discount rate)(Maximum expected future reward (given current state)) - (Current Q values)] 

#initialize some things
world_num = "0"
x = "10"

labels = []
for i in range(40):
    for j in range(40):
        labels.append(str(i) + "," + str(j))

# q_table = [[0 for col in range(5)] for row in range(10)]

cols = ["position", "left", "right", "up", "down"]
q_table = pd.DataFrame(index = [0], columns = cols).fillna(0)

for label in labels:
    q_table["position"].append(label)

print(q_table.head())

enter_world(world_num)

while(1):
    move = "N"
    make_move(move, world_num)
    
    sleep(1)