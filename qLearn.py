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

def qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward):
    
    # Percept - the agents perceptual inputs at any given instant
    # Persistent - Global variables that outlive a single function call
    qTable = pickle.load(open('qTable0.pkl', 'rb'))
    
    # Set learning rate (alpha)
    gamma = 0.9
    alpha = 0.9 
    
    # Terminal Condition
    if currentState is None:
        qTable[previousState[0]][previousState[1]][None] = currentReward
        print('Dumping Q table to pickle file.')
        pickle.dump(qTable, open('qTable0.pkl', 'wb'))
        print('Dump completed successfully.')
        return None
    
    
    print('Updating Q table')
    
    #qTable[previousState[0]][previousState[1]][previousAction] = (qTable[previousState[0]][previousState[1]][previousAction]
    #    + alpha*(previousReward + gamma*np.max(qTable[currentState[0]][currentState[1]][:]) 
    #    - qTable[previousState[0]][previousState[1]][previousAction]))
    
    # Q(s,a) <- (1-alpha)*Q(s,a) + alpha*(r + gamma*maxQ(s',a'))
    qTable[previousState[0]][previousState[1]][previousAction] = ((1-alpha)*qTable[previousState[0]][previousState[1]][previousAction]
        + alpha*(previousReward + gamma*np.max(qTable[currentState[0]][currentState[1]][:])))
    
    print('Dumping Q table to pickle file.')
    pickle.dump(qTable, open('qTable0.pkl', 'wb'))
    print('Dump completed successfully.')
        
    nextAction = np.argmax(qTable[currentState[0]][currentState[1]][:])
    return nextAction
   

def selectMove(previousAction):
    
    #print('Moving agent.')
    if previousAction == 0:
        direction = 'North'
        nextState = api.make_move('N', '0')
    elif previousAction == 1:
        direction = 'East'
        nextState = api.make_move('E', '0')
    elif previousAction == 2:
        direction = 'South'
        nextState = api.make_move('S', '0')
    elif previousAction == 3:
        direction = 'West'
        nextState = api.make_move('W', '0')
        
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
    
    return (currentState, currentReward)

if __name__ == "__main__":
    
    try:
        print('Checking for pickle file')
        qTable = pickle.load(open('qTable0.pkl', 'rb'))
        print('Pickle file found.')
    except (OSError, IOError, EOFError) as e:
        print('No pickle file found. Creating now.')
        # Initialize Q-Values -> 3-dimensional array with x,y coordinates and action
        qTable = np.array(np.zeros([40,40,4]))
        
        pickle.dump(qTable, open('qTable0.pkl', 'wb'))
        print('File created successfully.')
    
    # Check what world we are in
    print('Locating agent.')
    presentStatus = api.locate_me()
    presentStatus = json.loads(presentStatus.decode())
    world = int(presentStatus['world'])
    
    time.sleep(15)
    if world != -1:
        print('Agent found in world ' + str(world) + '.')
        print('Getting present state of agent in world ' + str(world) + '.')
        
        # Get 'previous state' for Q-Learning
        state = api.make_move('', '0')
        state = json.loads(state.decode())
        stateX = int(state['newState']['x'])
        stateY = int(state['newState']['y'])
        reward = state['reward']
    
        previousState = [stateX, stateY]
        previousReward = reward
        
        time.sleep(15)
        # By default lets pick a random action at first to get a history of
        # actions in this program instance.
        print('Moving agent.')
        previousAction = random.choice(range(0,4))
        
        (currentState, currentReward) = selectMove(previousAction)
        
        time.sleep(15)
        explore = True
        print('Beginning Q-Learning sequence.')
        
        exploreCount = 0
        while exploreCount < 5:
        
            # Determine the next action
            print('Determining next action.')
            action = qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward)
            
            if action is not None:
                # Update the variable values
                previousState = currentState
                previousReward = currentReward
                previousAction = action
            
                (currentState, currentReward) = selectMove(previousAction)
                time.sleep(15)
            
            else:
                print('Not in any world.')
                world = input("Enter desired world number:")
                api.enter_world(world)
                
                exploreCount += 1
                time.sleep(15)
    
            