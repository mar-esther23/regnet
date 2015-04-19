from random import shuffle

from regnet import RegNet
from node import Node


def state_transition(state, net, method="sync", nodes="all"):
    """
    Calculate S(t+1) from S(t)

    Parameters
    ----------
    state : state of all nodes in t
    net   : regulatory network
    method: type of evaluation
                "sync"   (default) all nodes at the same time
                "async"  nodes are evaluated one by one
    nodes :  node(s) to evaluate
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

