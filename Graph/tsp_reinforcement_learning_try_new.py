# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 16:22:47 2022

@author: HP
"""
import numpy as np
def eps_greedy_action(proposed_action, eps, actions, state):    
    p = np.random.random()    
    if p < (1 - eps) and proposed_action is not None:        
        return proposed_action    
    else:        
        return np.random.choice(actions[state])
    
def trip(states,available_actions,rewards, proposed_action,
          eps,returns,V,Q):
    start = 'Turin'
    end = 'Turin'
    state = start
    history = []
    non_visited_cities = states[1:]
    while state != end or non_visited_cities != []:
        action = eps_greedy_action(proposed_action[state], eps,
                                   available_actions, state)
        history.append((state,action))
        if rewards[(state,action)]!=-10:
            new_state = action
        else:
            new_state = state
        state = new_state
        if new_state in non_visited_cities:
            non_visited_cities.remove(new_state)
    G = 200
    for (state,action) in list(reversed(history))[1:]:
        G = G + rewards[(state,action)]
        t = history.index((state,action))
        if state not in [h[0] for h in history][:t]:
            returns[state].append(G)
            V[state] = np.average(returns[state])
        Q[(state,action)]=V[action if rewards[(state,action)]!=-10
                                else state]+rewards[(state,action)]
    return Q

for t in range(10000):    
    Q = trip(available_actions,rewards,proposed_action,0.7,returns,
               V,Q)    
    for state in states:        
        actions_rewards = {}        
        for a in available_actions[state]:            
            actions_rewards[a] = Q[(state,a)]        
        proposed_action[state] = max_dict(actions_rewards)[0]