import networkx as nx
import numpy as np

#from regnet import RegNet



class Attractor(object):
    """
    Base class for an attractor.

    An attractor is a stable state from a network such that S(t) = S(t+n).
    """

    def __init__(self,data,f_type="lambda_bool"):
        """Initialize an attractor. A attractor has one or more states.

        Parameters
        ----------
        f_type :    string, type of function in the graph.
        attractor:  states that constitute the attractor, begining from the smallest one.
        label :     (optional) label of the attractor

        See Also
        --------
        
        Examples
        --------
        """

        self.f_type = f_type #type of function of the network
        self.attractor = []
        
        pass