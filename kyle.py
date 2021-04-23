from api_interaction import *

#10 worlds
#Each is 40x40
    #1600 states x 4 actions for each world
    #save all of these and output to pickle file

#returns the move you should do and updates the pickle file of all the new states
def q_learning():
    #initialize the q table (number of actions x number of states)
        #all are 0

    #choose an action

    #perform an action

    #action (a) in the state (s) is chosen based on the Q-Table
    
    #update the Q-values for the action using the Bellman equation 
        #Q(s, a) = (Expected Discounted cumulative reward)
        #use epsilon greedy strategy
            #at first random, progressively becomes mroe confident

    #measure reward --> using reward from 

    #Evaluate --> update the Q(s, a) function
        #New Q value (s, a) = (Current Q values) + (Learning Rate)[(Reward for taking an action in a state) + (Discount rate)(Maximum expected future reward) - (Current Q values)] 

world_num = "0"
x = "10"

enter_world(world_num)

while(1):
    move = "N"
    make_move(move, world_num)
    
    sleep(1)