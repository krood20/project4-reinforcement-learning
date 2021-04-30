#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:19:17 2021

@author: kingrice
"""

import json
import api_interaction as api
import numpy as np
import pickle
import time 
import random
import math


world = '1'
api.enter_world(world)

# checks is api move to expected square
def checkUnexpectedMovement(previousState, previousAction, currentState):
    if previousAction == 0:
        if(previousState[1] + 1 == currentState[1] and previousState[1]!= 39):
            return False
    elif previousAction == 1:
        if(previousState[0] + 1 == currentState[0] and previousState[0]!= 39):
            return False
    elif previousAction == 2:
        if(previousState[1] - 1 == currentState[1] and previousState[1]!= 0):
            return False
    elif previousAction == 3:
        if(previousState[0] - 1 == currentState[0] and previousState[0]!= 0):
            return False
    return True

def qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward, epsilon):
    
    # Percept - the agents perceptual inputs at any given instant
    # Persistent - Global variables that outlive a single function call
    # qTable = pickle.load(open('qTable0.pkl', 'rb'))
    
    # Set learning rate (alpha)
    gamma = 0.7
    alpha = 0.9
    
    # Terminal Condition
    if currentState is None:
        qTable[previousState[0]][previousState[1]][None] = currentReward
        # print('Dumping Q table to pickle file.')
        pickle.dump(qTable, open('qTable'+world+'.pkl', 'wb'))
        # print('Dump completed successfully.')
        return None
    
    # print('Updating Q table')
    
    # qTable[previousState[0]][previousState[1]][previousAction] = (qTable[previousState[0]][previousState[1]][previousAction]
    #    + alpha*(currentReward + gamma*np.max(qTable[currentState[0]][currentState[1]][:]) 
    #    - qTable[previousState[0]][previousState[1]][previousAction]))
    
    # Q(s,a) <- (1-alpha)*Q(s,a) + alpha*(r + gamma*maxQ(s',a'))

    qTable[previousState[0]][previousState[1]][previousAction] = ((1-alpha)*qTable[previousState[0]][previousState[1]][previousAction]
        + alpha*(currentReward + gamma*np.max(qTable[currentState[0]][currentState[1]][:])))
    
    # print('Dumping Q table to pickle file.')
    pickle.dump(qTable, open('qTable'+world+'.pkl', 'wb'))
    # print('Dump completed successfully.')

    
    r = random.uniform(0, 1)
    if( r < epsilon):
        # explore instead of pick current best move

        # prioritize unvisited squares
        choices = []
        if(currentState[0] != 0):
            val = np.amax(qTable[currentState[0] - 1][currentState[1]][:])
            if(val == 0):
                choices.append(3)
        if(currentState[0] != 39):
            val = np.amax(qTable[currentState[0] + 1][currentState[1]][:])
            if(val == 0):
                choices.append(1)
        if(currentState[1] != 39):
            val = np.amax(qTable[currentState[0] ][currentState[1]+1][:])
            if(val == 0):
                choices.append(0)
        if(currentState[1] != 0):
            val = np.amax(qTable[currentState[0] ][currentState[1]-1][:])
            if(val == 0):
                choices.append(2)
        if(len(choices) >=1):
            return random.choice(choices)
        
        # if none go to unvisted direction
        choices = range(0, 4)
        validChoices =[]
        newChoices =[]
        for i in choices:
            if( qTable[currentState[0]][currentState[1]][i] == 0 ):
                newChoices.append(i)
            if( len(newChoices) >= 1):
                return random.choice(newChoices)
            if( qTable[currentState[0]][currentState[1]][i] != -math.inf ):
                validChoices.append(i)
        # make completely random move
        if(r < .5):
            return random.choice(validChoices)

    #pick best move base on learning
    nextAction = np.argmax(qTable[currentState[0]][currentState[1]][:])
    return nextAction 
   
def backFillReward(currentState, currentReward):

    if currentReward > 0 :
        gamma = 0.9
        alpha = 0.9
    else :
        gamma = 0.2
        alpha = 0.2

    for i in range(0 , 4):
        qTable[currentState[0]][currentState[1]][i] = currentReward
    # update rewards moving out from exit state going N E S W
    # reward decays as you move out
    # potential update update rewards radially
    for i in range(0, currentState[0] - 1):
        qTable[currentState[0]-i-1][currentState[1]][1] = (1-alpha)*qTable[currentState[0]-i-1][currentState[1]][1] + alpha*( gamma*np.max(qTable[currentState[0] - i][currentState[1]][:]))
    for i in range(currentState[0], 38):
        qTable[i+1][currentState[1]][3] = (1-alpha)*qTable[i+1][currentState[1]][3] + alpha*( gamma*np.max(qTable[i][currentState[1]][:]))
    for i in range(0, currentState[1]-1):
        qTable[currentState[0]][currentState[1]-i-1][2] = (1-alpha)*qTable[currentState[0]][currentState[1]-i-1][1] + alpha*( gamma*np.max(qTable[currentState[0]][currentState[1]-i][:]))
    for i in range(currentState[1], 38):
        qTable[currentState[0]][i+1][0] = (1-alpha)*qTable[currentState[0]][i+1][0] + alpha*( gamma*np.max(qTable[currentState[0]][i][:]))

def selectMove(previousAction):
    
    if previousAction == 0:
        direction = 'North'
        nextState = api.make_move('N', world)
    elif previousAction == 1:
        direction = 'East'
        nextState = api.make_move('E', world)
    elif previousAction == 2:
        direction = 'South'
        nextState = api.make_move('S', world)
    elif previousAction == 3:
        direction = 'West'
        nextState = api.make_move('W', world)
        
    print('Moved agent ' + direction + '.')
    state = json.loads(nextState.decode())
    print(state)
    if state['newState'] != None:
        #have to check for unpexted movement
        stateX = int(state['newState']['x'])
        stateY = int(state['newState']['y'])
        reward = state['reward']
        currentState = [stateX, stateY]
        currentReward = reward
    
    else:
        print('Fell into exit State.')
        # need to progate out
        currentState = state['newState']
        reward = state['reward']
        currentReward = reward
    
    return currentState, currentReward 

if __name__ == "__main__":
    
    try:
        print('Checking for pickle file')
        qTable = pickle.load(open('qTable'+world+'.pkl', 'rb'))
        pickle.dump(qTable, open('qTable'+world+'.pkl', 'wb'))

        print('Pickle file found.')
    except (OSError, IOError, EOFError) as e:
        print('No pickle file found. Creating now.')
        # Initialize Q-Values -> 3-dimensional array with x,y coordinates and action

        # setting impossible directions at edges to infinity
        qTable = np.array(np.zeros([40,40,4]))
        for item in qTable[:,0]:
            item[2] = -math.inf
        for item in qTable[:,39]:
            item[0] = -math.inf
        for item in qTable[0,:]:
            item[3] = -math.inf
        for item in qTable[39, :]:
            item[1] = -math.inf
        pickle.dump(qTable, open('qTable'+world+'.pkl', 'wb'))
        
        print('File created successfully.')
    
    # Check what world we are in
    print('Locating agent.')
    presentStatus = api.locate_me()
    presentStatus = json.loads(presentStatus.decode())
    
    time.sleep(1)
    if world != -1:
        # print('Agent found in world ' + str(world) + '.')
        # print('Getting present state of agent in world ' + str(world) + '.')
        
        # Get 'previous state' for Q-Learning
        state = api.make_move('', world)
        state = json.loads(state.decode())
        stateX = int(state['newState']['x'])
        stateY = int(state['newState']['y'])
        reward = state['reward']
    
        previousState = [stateX, stateY]
        previousReward = reward
        
        
        # By default lets pick a random action at first to get a history of
        # actions in this program instance.
        print('Moving agent.')
        previousAction =  random.choice(range(0,4))
        currentState , currentReward = selectMove(previousAction)
        
        
        explore = True
        print('Beginning Q-Learning sequence.')
        lastMove =  api.get_last_x_moves("1")
        lastMove = json.loads(lastMove.decode())

        # number of time we found exit states across all runs
        exploreCount = 0

        # number of move we made in current run
        moves = 0

        while exploreCount < 8:

            
            # set epsilon value to determine chance to exploring
            epsilon = ( (8 - exploreCount) / 8 ) * .9
            if moves < 1000 :
                epsilon += .1

            action = qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward, epsilon)
            moves += 1 
            
            if action is not None:
                # Update the variable values
                previousState = currentState
                previousReward = currentReward
                previousAction = action

                currentState, currentReward = selectMove(previousAction)

                # update reward values across map if exit state is found
                if(currentState is None):
                    #saying find a good state is better than bad
                    if(currentReward < 0):
                        exploreCount += 1
                    else:
                        exploreCount += 2
                    moves = 0
                    backFillReward(previousState, currentReward)

            else:
                print('Not in any world.')

                if ( exploreCount >= 8):
                    exit()
                # re enter world to try again
                api.enter_world(world)
                time.sleep(15)
                
                state = api.make_move('', world)
                state = json.loads(state.decode())
                stateX = int(state['newState']['x'])
                stateY = int(state['newState']['y'])
                reward = state['reward']
                previousAction =  random.choice(range(0,4))
                previousState = [stateX, stateY]
                previousReward = reward
                currentState, currentReward = selectMove(previousAction)

