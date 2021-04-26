#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:19:17 2021

@author: kingrice
"""
#import http.client
#import mimetypes
#from codecs import encode
import json
import api_interaction as api
#import pandas as pd
import numpy as np
import pickle
import time 
import random

def qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward):
    
    # Percept - the agents perceptual inputs at any given instant
    # Persistent - Global variables that outlive a single function call
    qTable = pickle.load(open('qTable0.pkl', 'rb'))
    
    # Set learning rate (alpha)
    gamma = 0.75
    alpha = 0.9 
    
    # Terminal Condition
    if previousState is None:
        return 
    
    if currentState:
        print('Updating Q table')
        qTable[previousState[0]][previousState[1]][previousAction] = (qTable[previousState[0]][previousState[1]][previousAction]
            + alpha*(previousReward + gamma*np.max(qTable[currentState[0]][currentState[1]][:]) 
            - qTable[previousState[0]][previousState[1]][previousAction]))
        
        print('Dumping Q table to pickle file.')
        pickle.dump(qTable, open('qTable0.pkl', 'wb'))
        print('Dump completed successfully.')
            
        nextAction = int(np.max(qTable[currentState[0]][currentState[1]][:]))
        return nextAction

if __name__ == "__main__":
    
    try:
        print('Checking for pickle file')
        qTable = pickle.load(open('qTable0.pkl', 'rb'))
        print('Pickle file found.')
    except (OSError, IOError, EOFError) as e:
        print('No pickle file found. Creating now.')
        # Initialize Q-Values -> 3-dimensional array with x,y coordinates and action
        qTable = np.array(np.zeros([400,400,4]))
        pickle.dump(qTable, open('qTable0.pkl', 'wb'))
        print('File created successfully.')
    
    # Check what world we are in
    print('Locating agent.')
    presentStatus = api.locate_me()
    presentStatus = json.loads(presentStatus.decode())
    world = int(presentStatus['world'])
    print('Agent found in world ' + str(world) + '.')
    
    time.sleep(15)
    if world != -1:
        
        print('Getting present state of agent in world ' + str(world) + '.')
        state = api.make_move('', '0')
        state = json.loads(state.decode())
        stateX = int(state['newState']['x'])
        stateY = int(state['newState']['y'])
        reward = int(state['reward'])
    
        previousState = [stateX, stateY]
        previousReward = reward
        time.sleep(15)
        
        # By default lets pick a random action at first to get a history of
        # actions in this program instance.
        print('Moving agent.')
        previousAction = random.choice(range(0,4))
        if previousAction == 0:
            nextState = api.make_move('N', '0')
        elif previousAction == 1:
            nextState = api.make_move('E', '0')
        elif previousAction == 2:
            nextState = api.make_move('S', '0')
        elif previousAction == 3:
            nextState = api.make_move('W', '0')
        
        state = json.loads(nextState.decode())
        print(state)
        
        stateX = int(state['newState']['x'])
        stateY = int(state['newState']['y'])
        reward = int(state['reward'])
        currentState = [stateX, stateY]
        currentReward = reward
            
        time.sleep(15)
        explore = True
        print('Beginning Q-Learning sequence.')
        while explore:
            
            # Determine the next action
            print('Determining next action.')
            action = qLearningAgent(previousState, previousReward, previousAction, currentState, currentReward)
            
            # Update the variable values
            previousState = currentState
            previousReward = currentReward
            previousAction = action
            
            print('Moving agent.')
            # For actions, 'N' is index 0, 'E' is index 1, 'S' is index 2, and 'W' is index 3.
            if action == 0:
                nextState = api.make_move('N', '0')
            elif action == 1:
                nextState = api.make_move('E', '0')
            elif action == 2:
                nextState = api.make_move('S', '0')
            elif action == 3:
                nextState = api.make_move('W', '0')
           
            
            state = json.loads(nextState.decode())
            print(state)
            stateX = int(state['newState']['x'])
            stateY = int(state['newState']['y'])
            reward = int(state['reward'])
            currentState = [stateX, stateY]
            currentReward = reward
            
            time.sleep(15)
    
    else:
        print('Not in any world')