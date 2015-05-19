import networkx as nx
import numpy as np

#from regnet import RegNet
from states import *


class Attractor(object):
    """
    An attractor is a solution of the network such that state(t) = state(t+n).

    Attributes
    ----------
    f_type (str):   function type.
    attr (list of lists):  states that constitute the attractor, begining from the smallest one.
    label (str, optional): label of the attractor
    """

    def __init__(self, states, f_type, node_names, basin=None, label="", graph=None):
        """
        An attractor is a solution of the network such that state(t) = state(t+n).

        Arguments
        ---------
        states (list of lists):       states that constitute the attractor
        f_type (str):               function type of the network
        node_names (list of str):   names of nodes in attractor.
        basin (int, optional):      number of states that end in the attractor.
        label (str, optional):      label of the attractor
        graph (DiGraph, optional):  transition graph of states that end in attractor.
        """
        
        self.f_type = f_type
        self.node_names = node_names
        self.basin = basin
        self.label = label
        self.graph = graph
        self.states = states



    def get_states(self):
        return self._states

    def set_states(self, states):
        states = return_valid_states(states, len(self.node_names))
        #search for duplicates
        if states[0] == states[-1]: states.pop()
        for i in range(len(states)): #search for repeated
            if states[i] in states[i+1:]: 
                print "Repeated state: " + str(states[i])
        #order from min
        i = states.index(min(states))
        self._states = states[i:] + states[:i]

    states = property(get_states,set_states)



    def __str__(self): 
        """
        Print attractor length, states and basin.
        """
        text = "Attractor " + self.label  + "\n"
        text += "\tLength: "+ str(len(self.states)) + "\n"
        text += "\tBasin: "+ str(self.basin) + "\n"
        text += "\tWith nodes: "+ ', '.join(self.node_names) + "\n" 
        text += "\tWith states: "
        for a in self.states: text += " -> " + state_to_str(a)
        return text.strip()


    def __len__(self):
        """Return the number of states in attractor. Use the expression 'len(attr)'."""
        return len(self.states)


    def __iter__(self): 
        """Iterate over the states of attractor. Use the expression 'for n in attr'."""
        return iter(self.states)

    def __contains__(self,n):
        """Return True if n is a state in the attractor, False otherwise. Use the expression 'n in attr'."""
        for a in self.states:
            if a == n: return True
        return False