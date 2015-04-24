from random import shuffle, choice, randint
import networkx as nx

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


def get_transition_graph(network, method="sync", states="all", G=None):
    """
    Obtain transition graph of the network. Only works for Boolean or discrete integer networks.

    Arguments
    ---------
    network (regnet):   network to evaluate.
    method (str):       updating method of nodes.
        "sync" :    synchronous updating of all N nodes simultaneously
        "async":    for each update a node was selected at random and updated
    states: initial states to try
        "all":  all initial states will be used
        int :   n random initial states will be used
        list:   the initial states in the list will be used
    G (nx.Digraph):     previous transition graph.

    Returns
    -------
    G (nx.DiGraph): transition graph of the network.
    """
    # Initialize graph
    if G == None: G = nx.DiGraph()

    #generate states to evaluate
    if states == "all": #generator of all possible states
        states = generate_all_base_array_states(len(network), network.f_base)
    elif type(states) == int: #generator random states
        states = generate_random_base_array_states(states, len(network), network.f_base)
    elif type(states) == list: #use user defined states
        pass #just checking
    else: raise TypeError("Incorrect states option.")

    #Evaluate states
    for s in states:
        if method == "sync":
            new = state_transition(s, network, "sync", "all")
            G.add_edge( array_to_str(s), array_to_str(new) )  #save str to graph
        if method == "async":
            news = {}
            s_str = array_to_str(s)
            for n in network: #evaluate each node
                new = array_to_str( state_transition(s, network, "async", n.name) )
                if new in news: news[new] += 1
                else: news[new] = 1
            if news[s_str] != len(network): del news[s_str] # remove false self-loops
            for n in news: G.add_edge( s_str, array_to_str(n), weight=news[n] )  #save str to graph
    return G


def get_attractors(network, method="sync", states="all"):
    """
    An attractor is a solution of the network such that state(t) = state(t+n).

    Arguments
    ---------
    network (regnet):   network to evaluate.
    method (str):       updating method of nodes.
        "sync" :    synchronous updating of all N nodes simultaneously
        "async":    for each update a node was selected at random and updated
    states:     initial states to try
        "all":  all initial states will be used
        int :   n random initial states will be used
        list:   the initial states in the list will be used

    Returns
    -------
    attrs (list of attractors): list of attractors of the network
    """

    if len(network > 25) and initial_states == "all":
        print "The network has more than 25 nodes, calculating the attractors may take a long time. Consider using a number of random initial states."

    pass



##########################################
#   State generators & Base Conversion   #
##########################################


def generate_all_base_array_states(nodes, base):
    """
    Returns all posible states given a network of n nodes where the state can be discrete with max base.

    Arguments
    ---------
    nodes (int): number of nodes
    base (int):  max value of nodes

    Yields
    ------
    state (list of int)
    """
    c = 0
    while c < base ** nodes :
        if base == 2: state = dec_to_bin_array(c, nodes)
        else: state = dec_to_base_array(c, base, nodes)
        c += 1
        yield state

def generate_random_base_array_states(n, nodes, base):
    """
    Returns n random states given a network of n nodes where the state can be discrete with max base.

    Arguments
    ---------
    n (int):     number of random states to generate
    nodes (int): number of nodes
    base (int):  max value of nodes

    Yields
    ------
    state (list of int)
    """
    while n > 0 :
        c = randint(0, base ** nodes -1)
        if base == 2: state = dec_to_bin_array(c, nodes)
        else: state = dec_to_base_array(c, base, nodes)
        n -= 1
        yield state

def dec_to_base_array(x, base, length):
    """Convert number in decimal to an array in a diferent base."""
    s, i = [0 for i in range(length)], 1
    while x > 0:
        s[-i], x = x%base, x/base
        i += 1
    return s

def base_array_to_dec(s, base):
    """Convert array in a given base to decimal."""
    dec , e = 0 , len(s)
    while e > 0:
        dec += s[-e] * (base ** (e -1))
        e -= 1
    return dec

def dec_to_bin_array(n, padding):
    """Convert number in decimal to a binary array."""
    s = [int(i) for i in bin(n)[2:].zfill(padding) ]
    return s

def bin_array_to_dec(s):
    """Convert binary array to decimal."""
    dec = int(''.join([str(i) for i in s]), 2)
    return dec

def array_to_str(a):
    return ''.join([str(int(i)) for i in a] )

def str_to_array(s):
    return [i for i in s]