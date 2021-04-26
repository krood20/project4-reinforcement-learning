from api_interaction import *
import pandas as pd
import numpy as np
import pickle


#10 worlds
#Each is 40x40
    #1600 states x 4 actions for each world
    #save all of these and output to pickle file

#returns the move you should do and updates the pickle file of all the new states
def choose_move():
    #qlearning
    #load qtable from pkl file
    q_table = pickle.load(open('q_table.pkl', 'rb'))

    #choose and perform an action --> could be random
        #action (a) in the state (s) is chosen based on the Q-Table
         #use epsilon greedy strategy
            #at first random, progressively becomes mroe confident

    #measure reward --> using reward from making move

    #Evaluate --> update the Q(s, a) function based on Bellman Equation
        #New Q value (s, a) = (Current Q values) + (Learning Rate)[(Reward for taking an action in a state) + (Discount rate)(Maximum expected future reward (given current state)) - (Current Q values)] 

    #output initially to pkl file
    #dump embeddings into output file
    with open('q_table.pkl', 'wb') as p:
        pickle.dump(q_table, p)
        print('done with dump')

    move = "N"
    return move

#initialize some things
world_num = "0"
x = "10"

labels = []
for i in range(40):
    for j in range(40):
        labels.append(str(i) + "," + str(j))

cols = ["position", "left", "right", "up", "down"]
q_table = pd.DataFrame(index = [0], columns = cols).fillna(0)

for i in range(len(labels)):
    q_table.loc[i] = [labels[i], 0, 0, 0, 0]


print(q_table.head())

#output initially to pkl file
#dump embeddings into output file
with open('q_table_initial.pkl', 'wb') as p:
    pickle.dump(q_table, p)
    print('done with dump')

enter_world(world_num)

while(1):
    # move = "N"
    move = choose_move()
    make_move(move, world_num)
    
    sleep(1)