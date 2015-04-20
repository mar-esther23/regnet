from random import shuffle,  choice

from regnet import RegNet
from node import Node


def state_transition(state, net, method="sync", nodes="all"):
    """
    Calculate state in t+1 from state in t.

    Arguments
    ---------
    state (list):   state of all nodes in t
    net (regnet):   regulatory network
    method (str):   type of evaluation
        "sync"   (default) all nodes at the same time
        "async"  nodes are evaluated one by one
    nodes (*):      node(s) to evaluate
        "all"    (default) evaluate all nodes in declared order
        "random" evaluate all nodes in random order
        [list]   evaluate only the nodes in the list in that order
        node     evaluate only this node, receives node name

    Returns
    -------
    state : state of all nodes in t+1, if some nodes where not updated their value is the same as in t.
    """

    if not isinstance(net, RegNet): raise TypeError("Invalid network")
    if len(state) != len(net): raise TypeError("Invalid state")

    #determine order on nodes to update
    if nodes == "all": 
        nodes = [n.name for n in net]
    elif nodes == "random":
        nodes = [n.name for n in net]
        shuffle(nodes) #mix mix
    elif nodes in net: #only one node
        nodes = [nodes] #transform into list
    elif type(nodes) == list: #nlist of nodes
        pass
    else: raise TypeError("Invalid node list")

    #evaluate nodes
    if method == "sync":
        new_state = list(state)
        for n in nodes:
            #actualize new state using old as base
            new_state[ net[n].index ] =  net[n].function(state)
        return new_state

    if method == "async":
        new_state = list(state)
        for n in nodes:
            #actualize new state using last updated new_state of list in order
            new_state[ net[n].index ] =  net[n].function(new_state)
        return new_state


def get_trajectory(state, network, method="sync", time=None):
    """
    Evaluates network until an attractor is reached or for a certain number of updates.

    Arguments
    ---------

    state (list) :      initial state of trajectory
    network (regnet):   network to evaluate
    method (str):       updating method of nodes
        "sync" :    synchronous updating of all N nodes simultaneously
        "async":    for each update a node was selected at random and updated
        "async-all": the N nodes were updated in a randomly ordered sequence, before each sequence a new random ordering of the nodes is made
    time (int | None) : number of updates, if None the network is updated until an attractor is found

    Returns
    -------
    Trajectory (list):  list of states beginning form original state
    """

    trajectory = [state]
    while time > 0 or time == None:
        if method == "sync":
            state = state_transition(state, network, "sync", "all")
        if method == "async":
            state = state_transition(state, network, "async", choice(network.node_list()) )
        if method == "async-all":
            state = state_transition(state, network, "async", "random" )
        trajectory.append(state)
        # verify if attractor
        if time == None:
            if state in trajectory[:-1]: 
                return trajectory
        else: time = time - 1
    return trajectory



def get_attractors(network, method="sync", nodes="all"):
    pass
