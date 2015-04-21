import networkx as nx
import numpy as np

from node import Node



class RegNet(object):
    """
    A network of nodes with associated regulatory functions. The edges are defined by which nodes regulate the value of a certain node.

    Attributes
    ----------  
    f_type (str):   type of function in the graph, can be:
        "lambda_bool": lambda boolean function, evaluate state in function, returns 0 or 1
        "matrix_bool": interaction matrix, multiply state per node vector, evaluate by threshold, returns 0 or 1
        "table_bool":  transition table, search state of neighbors in table, returns 0 or 1
        "lambda_discrete": lambda discrete function, evaluate state in function, returns a positive integer
    f_base (int, list):         number of values the nodes can take, if boolean it is 2. If discrete it is max_value + 1. If the nodes have different values the list determines the max value of each node.
    nodes (list of Node(s)):    node objects, nodes have a name, index and function
    graph (networkx DiGraph):   networkx directed graph, edges are defined by which nodes regulate the value of a certain node
    threshold (int, optional): threshold to evaluate network
    adj_matrix (numpy matrix, optional): adjacency matrix
    verbose (Bool, optional)
    """

    def __init__(self,data,f_type="lambda_bool", f_base=2, threshold=1, verbose=True):
        """Initialize a node. A node must have a name, index, function type, and a function; regulators and attributes are optional.

        Arguments
        ---------
        data :          data to initialize network.  If data=None (default) an empty network is generated.  
        f_type (str):   type of function in the graph
        threshold (int, optional), threshold to evaluate network
        adj_matrix (numpy matrix, optional): adjacency matrix
        verbose (Bool, optional)
        """
        
        #The main structure is a networkx directed graph        
        self.f_type = f_type #type of function of the network
        self.graph = nx.DiGraph() #networkx graph (dictionary)
        self.nodes = [] #list of node objects, nodes have a name, index and function
        self.verbose = verbose
        if f_base != 2: raise NotImplementedError
        else: self.f_base = f_base
    
        if self.f_type == "lambda_bool": 
            #data: multiline string with boolean functions
            self.nodes = self.generate_node_lambda_bool(data)
            self.graph = self.node_regulators_to_digraph(self.nodes)

        if self.f_type == "matrix_bool":
            #AAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRGGGGGGGGGGGGGGGG
            raise NotImplementedError
            # #data: adyacency matrix with node names + weights
            # self.adj_matrix = np.array(data[1:])
            # if len(self.adj_matrix) != len(self.adj_matrix): print "Error: non-square matrix" #check that matrix is square
            # self.threshold = threshold
            # self.nodes = self.generate_node_matrix_bool(data[0], self.adj_matrix, threshold)
            # self.graph = self.adj_matrix_to_digraph(data[0], self.adj_matrix)

        if self.f_type == "table_bool":
            #data: [[ node_name, [regulators], [boolean table] ], ... ]
            self.nodes = self.generate_node_table_bool(data)
            self.graph = self.node_regulators_to_digraph(self.nodes)
    	

    	if self.f_type == "lambda_discrete":
    		raise NotImplementedError
            

    def __str__(self): 
        """Print network type and nodes (with rules) """
        text = self.f_type + ":\n"
        for node in self.nodes:
            text += str(node) + '\n'
        return text.strip()


    def __len__(self):
        """Return the number of nodes. Use the expression 'len(G)'."""
        return len(self.nodes)


    def __iter__(self): 
        """Iterate over the nodes. Use the expression 'for n in G'."""
        return iter(self.nodes)

    def __contains__(self,n):
        """Return True if n is a node name, False otherwise. Use the expression 'n in G'."""
        for node in self.nodes:
            if node.name == n: return True
        return False

    def __getitem__(self, n):
        """Return node with name n.  Use the expression 'G[n]'."""
        for node in self.nodes:
            if node.name == n: return node
        return False

    def node_list(self):
        """Return a list of the nodes in the graph."""
        return [n.name for n in self.nodes]



    """

    GENERATE NODES FROM DATA
    
    """

    def generate_node_lambda_bool(self, data):
        """
        Declare nodes with function from a multiline string of boolean functions.

        Arguments
        ---------
        data:  string, in format: node = regulatory function
               each node in newline
               nodes are declared in order of aparition
               functions are lambda functions which return 0 or 1

        Returns
        -------
        List of Node(s) (view class Node)
        """

        nodes = []
        data = data.strip().split('\n')
        data = [x for x in data if not x.strip().startswith('#')] #remove comented lines

        #as the function depends in the position we need to determine the ordered list of nodes first
        nodes_list = []
        for line in data:
            name = line.strip().split('=')[0].strip() #name string
            funct = line.strip().split('=')[1].strip() #function string
            regul = funct.replace(' and ', ' ').replace(' or ',' ').replace( ' not ',' ').split() #regulators list of strings
            nodes_list.append([name, funct, regul])
        nodes_names = [n[0] for n in nodes_list]
        
        #we also determine all regulators to see if there are signalling nodes that where not declared
        input_nodes = []
        for node in nodes_list:
            for r in node[2]:
                if r not in nodes_names:
                    nodes_names.append(r)
                    nodes_list.append([r, r, [r]])
                    if self.verbose: print "Declaring " + r +" as an input with function: " +r +" = " + r
                    input_nodes.append(r)
        
        #generate the nodes
        for index, node in enumerate(nodes_list):
            #generate lambda function
            node_lambda = eval("lambda (" + ','.join(nodes_names) + ') : ' + node[1]) 
            #declare node
            nodes.append(   Node(node[0], self.f_type, index, node_lambda, node[1], node[2])   )
        
        for n in nodes:
            for i in input_nodes:
                if n.name == i: n.input = True

        return nodes

    

    def generate_node_matrix_bool(self, names, matrix, threshold):
        """
        Declare nodes whose state is given by an interaction matrix
            S[i](t+1) = { 1 if \sum_j S_j(t) * a_ij >= threshold
                          0 otherwise

        Arguments
        ---------
        names    :  list with ordered name of nodes
        matrix :  numpy interaction matrix
        threshold:  int (default 1), used to evaluate if node is 1 or 0

        Returns
        ------.
        List of Node(s) (view class Node)

        """

        nodes = []
        if len(matrix) != len(matrix[0]): 
            raise TypeError("Incorrect interaction matrix")

        #transpose interactions to make things easier
        #now a_ij in interaction i->j
        matrix = np.transpose(matrix)

        #nodes(self, name, f_type, index, function=None, str_function="", regulators=None):
        for i in range(len(names)):
            node_name = names[i]
            node_str_function = '[' + ','.join([str(j) for j in matrix[i]]) + ']'
            #declare lambda function
            node_lambda = eval("lambda state: 1 if np.dot( state , "+ node_str_function + ") >= " +str(threshold) +" else 0" )
            #determine regulators
            regulators = [x for x,y in zip(names, matrix[i]) if y != 0]
            #declare node
            nodes.append(   Node(names[i], self.f_type, i, node_lambda,
                node_str_function, regulators))

        return nodes



    def generate_node_table_bool(self, data):
        """
        Declare nodes where the function is represented as a table. The next state is a position in the table that depends on ints regulators

        Arguments
        ---------
        data:  array, where [  [name, [regulators], [table]]  , ... ]

        Returns
        -------
        List of Node(s) (view class Node)

        Examples
        --------
        If:
        a(t) c(t) | b(t+1)
         0    0   |   0
         0    1   |   0
         1    0   |   1
         1    1   |   0
        Then:
        data = [   ['b', ['a','c'], [0,0,1,0]]   ]

        """
        nodes = []

        #as the function depends in the position we need to determine the ordered list of nodes first
        nodes_names = [n[0] for n in data]
        
        #we also determine all regulators to see if there are signalling nodes that where not declared
        for node in data:
            for r in node[1]:
                if r not in nodes_names:
                    nodes_names.append(r)
                    data.append([r, [r], [0,1]])
                    print r +" is an input with table: [0,1]"
        
        #generate the nodes
        for index, node in enumerate(data):
            node_str_function = ','.join(node[1]) +" : " + str(node[2])
            # generate lambda function
            # the lambda function receives the whole state,
            # however, it only uses its regulators to determine the correct position in the table
            # for example, if ['b', ['a', 'c'], [0,0,1,0]], 
            #    (which is equivalent to b = a and not c)
            # this becomes lambda (a,b,c) : [0,0,1,0][b*2**1 + c*2**0]
            position = [node[1][i] + '*2**' + str(len(node[1])-i-1) for i in range(len(node[1]))]
            node_lambda = eval(   "lambda (" +','.join(nodes_names) +") : " +str(node[2]) +'[' +'+'.join(position) +']'   )
            #declare node
            nodes.append(   Node(node[0], self.f_type, index, node_lambda, node_str_function, node[1])   )

        return nodes



    """

    GENERATE DIGRAPHS

    """

    def node_regulators_to_digraph(self, nodes):
        """
        Declare a networkx directed graph from a list of nodes using its regulators
        """
        G = nx.DiGraph()
        for n in nodes:
        	for r in n.regulators:
        		G.add_edge(r, n.name)
        return G

    def interaction_matrix_to_digraph(self, names, adyacency):
        """
        Declare a networkx directed graph with node names from adyacency matrix. a_ij is the effect of node j -> i
        """
        G = nx.DiGraph()
        for i in range(len(adyacency)):
            for j in range(len(adyacency[0])):
                if adyacency[i][j] != 0:
                    G.add_edge(names[j], names[i], weight=adyacency[i][j])
        return G
