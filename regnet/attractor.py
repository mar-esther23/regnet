import networkx as nx
import numpy as np

#from regnet import RegNet



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

        #check states and order them
        #states are saved as strings





    def __str__(self): 
        """
        Print attractor length, states and basin.
        """
        text = "Attractor " + self.label  + "\n"
        text += "\tLength: "+ str(len(self.attr)) + "\n"
        text += "\tBasin: "+ str(self.basin) + "\n"
        text += "\tWith nodes: "+ ', '.join(self.node_names) + "\n" 
        text += "\tWith states: "
        for a in self.attr: text += " -> " + a
        return text.strip()


    def __len__(self):
        """Return the number of states in attractor. Use the expression 'len(attr)'."""
        return len(self.attr)


    def __iter__(self): 
        """Iterate over the states of attractor. Use the expression 'for n in attr'."""
        return iter(self.attr)

    def __contains__(self,n):
        """Return True if n is a state in the attractor, False otherwise. Use the expression 'n in attr'."""
        for a in self.attr:
            if a == n: return True
        return False