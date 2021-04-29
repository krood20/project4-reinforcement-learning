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
import math as m


world = '2'
# api.enter_world(world)
def qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward):
    
    # Percept - the agents perceptual inputs at any given instant
    # Persistent - Global variables that outlive a single function call
    # qTable = pickle.load(open('qTable0.pkl', 'rb'))
    
    # Set learning rate (alpha)
    gamma = 0.7
    alpha = 0.7
    
    # Terminal Condition
    if currentState is None:
        qTable[previousState[0]][previousState[1]][None] = currentReward
        # print('Dumping Q table to pickle file.')
        pickle.dump(qTable, open('qTable'+world+'.pkl', 'wb'))
        # print('Dump completed successfully.')
        return None, None
    
    
    # print('Updating Q table')
    
    qTable[previousState[0]][previousState[1]][previousAction] = (qTable[previousState[0]][previousState[1]][previousAction]
       + alpha*(currentReward + gamma*np.max(qTable[currentState[0]][currentState[1]][:]) 
       - qTable[previousState[0]][previousState[1]][previousAction]))
    
    # Q(s,a) <- (1-alpha)*Q(s,a) + alpha*(r + gamma*maxQ(s',a'))
    
    # qTable[previousState[0]][previousState[1]][previousAction] = ((1-alpha)*qTable[previousState[0]][previousState[1]][previousAction]
    #     + alpha*(previousReward + gamma*np.max(qTable[currentState[0]][currentState[1]][:])))
    
    # print('Dumping Q table to pickle file.')
    pickle.dump(qTable, open('qTable'+world+'.pkl', 'wb'))
    # print('Dump completed successfully.')
        
    nextAction = np.argmax(qTable[currentState[0]][currentState[1]][:])
    return nextAction , qTable[currentState[0]][currentState[1]][:]
   

def selectMove(previousAction, epsilon, currentRewards):
    
    r = random.uniform(0, 1)
  
    newSquare = False
    #print('Moving agent.')
    time.sleep(5)
    if(r < epsilon):
        # explore pick random more and explore instead
        choices = range(0, 4)
        if( currentRewards is not None):
            newChoices = []
            for i in choices:
                if(currentRewards[i] == 0):
                    newChoices.append(i)
            if(len(newChoices) >= 1):                
                newSquare = True
                choices = newChoices
        previousAction = random.choice(choices)

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
        stateX = int(state['newState']['x'])
        stateY = int(state['newState']['y'])
        reward = state['reward']
        currentState = [stateX, stateY]
        currentReward = reward
    
    else:
        print('Fell into exit State.')
        currentState = state['newState']
        reward = state['reward']
        currentReward = reward
    
    return (currentState, currentReward, newSquare)

if __name__ == "__main__":
    
    try:
        print('Checking for pickle file')
        qTable = pickle.load(open('qTable'+world+'.pkl', 'rb'))
        print('Pickle file found.')
    except (OSError, IOError, EOFError) as e:
        print('No pickle file found. Creating now.')
        # Initialize Q-Values -> 3-dimensional array with x,y coordinates and action
        qTable = np.array(np.zeros([40,40,4]))
        
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
        previousAction = 0
        (currentState, currentReward, newSquare) = selectMove(previousAction,1, None)
        
        
        explore = True
        print('Beginning Q-Learning sequence.')
        lastMove =  api.get_last_x_moves("1")
        lastMove = json.loads(lastMove.decode())
        exploreCount = 0
        interationCount = 100
        while exploreCount < 5:
            # Determine the next action
            # print('Determining next action.')
            action, currentRewards = qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward)
            
            epsilon = 1 / (1 + m.exp( (interationCount - 3000) / 800) )
            print(epsilon, interationCount)
            if action is not None:
                # Update the variable values
                previousState = currentState
                previousReward = currentReward
                previousAction = action

                (currentState, currentReward, newSquare) = selectMove(previousAction, epsilon, currentRewards)
                if(newSquare):
                    interationCount += 1
            else:
                print('Not in any world.')
                api.enter_world(world)
                
                exploreCount += 1
                (currentState, currentReward, newSquare) = selectMove(previousAction,1, None)


