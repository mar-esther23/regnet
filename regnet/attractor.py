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

    def __init__(self, f_type, attr, label=""):
        """
        An attractor is a solution of the network such that state(t) = state(t+n).

        Arguments
        ---------
        f_type (str):   function type of the network
        attr (list of lists):  states that constitute the attractor
        label (str, optional): label of the attractor
        """

        self.f_type = f_type #type of function of the network
        self.attr = attr
        self.label = label
        






    # def __str__(self): 
    #     """
    #     Print network type and nodes (with rules)
    #     """
    #     text = self.f_type + ":\n"
    #     for node in self.nodes:
    #         text += str(node) + '\n'
    #     return text.strip()


    # def __len__(self):
    #     """Return the number of nodes. Use the expression 'len(G)'."""
    #     return len(self.nodes)


    # def __iter__(self): 
    #     """Iterate over the nodes. Use the expression 'for n in G'."""
    #     return iter(self.nodes)

    # def __contains__(self,n):
    #     """Return True if n is a node name, False otherwise. Use the expression 'n in G'."""
    #     for node in self.nodes:
    #         if node.name == n: return True
    #     return False

    # def __getitem__(self, n):
    #     """Return node with name n.  Use the expression 'G[n]'."""
    #     for node in self.nodes:
    #         if node.name == n: return node
    #     return False

    # def node_list(self):
    #     """Return a list of the nodes in the graph."""
    #     return [n.name for n in self.nodes]