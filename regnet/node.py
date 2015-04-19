from copy import deepcopy

class Node(object):
    """
    Base class for nodes.
    A node is an element of the network with a name and a function
    """

    def __init__(self, name, f_type, index, function=None, str_function="", regulators=None, input_node=False, fixed=False):
        """Initialize a node. A node must have a name, index, function type, and a function; regulators and attributes are optional.

        Parameters
        ----------
        name :      string, name of the node
        f_type :    string, type of node, can be:
            "lambda_bool":  lambda boolean function, evaluate state in function, returns 0 or 1
            "matrix_bool":  interaction matrix, multiply state per node vector, evaluate by threshold, returns 0 or 1
            "table_bool":   transition table, search state of neighbors in table, returns 0 or 1
        index :     index of the node in the graph
            Used to determine position in state vector
        function :  function that regulates the state of the node
        str_function :  string, display for function
        regulators :    list of nodes connected to this node, optional (default=None). This nodes affect the value of the node
        input_node :    (True/False) is node an input?
        fixed:      (True/False) is  node value fixed?

        See Also
        --------

        Examples
        --------
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
        #return node name and function
        return self.name + ' = ' + self.str_function

    def fix_node(self, value):
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
        # the node will return value as the result of the function
        self.fixed = False
        # return original unfixed values
        self.function = self.function_unfixed
        self.str_function = self.str_function_unfixed
        # delete fixed values
        self.function_unfixed = None
        self.str_function_unfixed = None








