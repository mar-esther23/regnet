from copy import deepcopy

class Node(object):
    """
    A node is an element of the network with a name and a function.

    Attributes
    ----------
    name (str):     name of node
    f_type (str):   function type
    index (str):    index of nodes
    function (lambda):  lambda function that updates the state of the node
    str_function (str): function readable display
    regulators (list):  nodes that regulate current node
    input (Bool):       is node an input?
    fixed (Bool):       is the value of the node fixed?
    """

    def __init__(self, name, f_type, index, function, str_function, regulators=None, input_node=False, fixed=False):
        """
        A node must have a name, index, function type, and a function; regulators and attributes are optional.

        Arguments
        ----------
        name (str):     name of the node
        f_type (str):   function type of node
        index (int):    index of the node in the graph
            Used to determine position in state vector
        function (lambda):  function that regulates the state of the node
        str_function (str): display for function
        regulators (list, optional):  nodes that regulate current node
        input_node (Bool, optional):  is node an input?
        fixed (Bool, optional):       is node value fixed?
        """


        self.name = name #name of node str
        self.f_type = f_type #function type, can be:
        self.index = index  #index of position in regnet.nodes

        self.function = function #lambda function that updates the state of the node
        self.str_function = str_function #string to print function
        self.regulators = regulators  # regulators list

        self.input = input_node #(True/False) is node an input?
        self.fixed = fixed #(True/False) is  node value fixed?


    def __str__(self):
        """
        Readable node name + function
        """
        return self.name + ' = ' + self.str_function

    def fix_node(self, value):
        """
        Fix the function of the node so that it always returns value.

        Arguments
        ---------
        Value (int, float): new value of the function
        """
        # the node will return value as the result of the function
        self.fixed = True
        # save original unfixed values
        self.function_unfixed = self.function
        self.str_function_unfixed = self.str_function
        # set fixed values
        value = deepcopy(value) #avoid array horrors
        self.function = lambda *a: value
        self.str_function = self.name + ' = ' + str(value)

    def unfix_node(self):
        """
        Unfix the function of the node so that it always returns its original lambda function.
        """
        # the node will return value as the result of the function
        self.fixed = False
        # return original unfixed values
        self.function = self.function_unfixed
        self.str_function = self.str_function_unfixed
        # delete fixed values
        self.function_unfixed = None
        self.str_function_unfixed = None








