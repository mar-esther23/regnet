from random import shuffle, randint
import matplotlib.pyplot as plt
#from itertools import zip
import networkx as nx
import numpy as np
import re

class regNet(object):
    def __init__(self,data,f_type="lambda_bool", threshold=None):
        #TODO change "f_text" for "data" and add capability to accept matrix or tabtext
        #TODO receive node names?
        
        #The main structure is a networkx directed graph        
        self.graph = nx.DiGraph() #networkx graph (dictionary)
        self.f_type = f_type #type of function of the network
        self.nodes = () #ordered tuple with node names in aparition order
        #self.functions = () #ordered tuple with lambda functions in aparition order
        #self.f_text = () #ordered tuple with text of functions in aparition order for printing
        #self.weight_matrix = np.array() #matrix with weight of interactions
    
        if self.f_type == "lambda_bool":
            #receives a text in format: node = regulatory function
            #each node in newline
            #nodes are declared in order of aparition
            #functions are lambda functions which return 0 or 1
            
            self.nodes = []
            self.functions = []
            self.f_text = []
            
            #declare nodes and f_text
            for line in data.strip().split('\n'):
                self.nodes.append(line.split('=')[0].strip())
                self.f_text.append(line.split('=')[1].strip())
            self.nodes = tuple(self.nodes)
            self.f_text = tuple(self.f_text)
            
            #declare lambda functions
            n_text = '('+','.join(self.nodes)+')' #initial vector text to keep node names
            for f in self.f_text:
                self.functions.append(eval("lambda " + n_text + ' : ' + f)) #eval to declare as f()
            self.functions = tuple(self.functions)
            
            #declare networkx graph
            #TODO make this a separate function that depends only of data
            for n,f in zip(self.nodes, self.f_text):
                f=f.replace('and','').replace('or','').replace('not','')
                f = f.split() #list of regulators
                for i in f: self.graph.add_edge(i,n)
            
            #declare adjacency matrix 
            #TODO declare weight_matrix
            self.weight_matrix = nx.to_numpy_matrix(self.graph, nodelist=self.nodes)
            
    
    
        elif self.f_type == "weight_matrix":
            #receives a weight matrix and a threshold
            #the first line of the array is the ordered name of the nodes
            #the rest is a square matrix with weight numbers
            
            self.functions = []
            self.f_text = []
            
            #declare nodes, matrix and f_text
            self.nodes = tuple(data[0])
            self.weight_matrix =  np.asmatrix(data[1::])
            for i in range(len(self.weight_matrix)): #things are printed as a tuple
                self.f_text.append(str(   tuple(map(int,self.weight_matrix[:,i]))   ))
            self.f_text = tuple(self.f_text)
            
            #declare networkx graph
            #TODO make this a function that depends only from data
            nodes = data[0] #node names
            data = zip(*data[1::]) #transpose weight matrix to make things easy  
            for n, reg in zip(nodes, data):
                #if weight is != 0 the node is a regulator
                reg = [n2 for n2,r in zip(nodes,reg) if r!=0 ]
                for r in reg: self.graph.add_edge(r,n) #declare edges
            
            #declare lambda functionsText
            for f in self.f_text:
                self.functions.append(eval('lambda state, threshold: [1 if x*y>threshold else 0 for x,y in zip(state,' + f + ' )]')) #eval to declare as f()
            self.functions = tuple(self.functions)
    
        else: print "Incorrect function type"
    
    #def stateTransition(self, state, method="sync", eval_order=None):
        ##takes a states and iterates the network once
        ##returns new state vector
        #if type(state)==int: state = self.int2bin(state)
        #if method == "sync":  
            #new_state = [0]*self.size
            #for i in range(self.size): #eval with lambda functions
                #new_state[i] = float(self.functions[i](state))
            #return new_state
        #if method == "async":
            #if eval_order == None: eval_order = [i for i in range(self.size)] #evaluate all nodes
            #shuffle(eval_order) #random order of evaluation
            #for i in eval_order: #eval with lambda functions
                #state[i] = float(self.functions[i](state))
            #return state
            
            ##What we will do is multiply vectors
            ##c=[i*j for i,j in zip(a,b)]
            ##And evaluate threshold
            ##d = [1 if x>0 else 0 for x in c]
            ##Minimal boolean version: c=[1 if i*j>t else 0 for i,j in zip(a,b)]
            
    #def getTransitionGraph(self, method="sync", initial_states=0, iter_steps=1):
        ##takes the boolean network
        ##return a networkx graph
        #self.transitionGraph = nx.DiGraph()
        #if method=="sync":
            #for i in range(2**self.size): #generate initial states
                #self.transitionGraph.add_edge(i, self.bin2int(self.stateTransition(i)))
        #if method=="async":
            #for i in range(2**self.size): #generate initial states
                #for j in range(self.size): #evaluate each node one by one
                    #self.transitionGraph.add_edge(i, self.bin2int(self.stateTransition(i, "async", [j])))
        #if method=="random":
            #for ns in range(initial_states):
                #for ni in range(iter_steps):
                    #i = randint(0, 2**self.size-1)
                    #j = self.bin2int(self.stateTransition(i))
                    #self.transitionGraph.add_edge(i, j)
                    #if i == j: break
                    #else: i = j
        #return self.transitionGraph
    
    #def getSteadyStates(self, method="all", n_states=0):
        ##calculates steady states, useful for big boolean networks
        #try: self.attractors
        #except AttributeError: self.attractors = {}
        #if method == "all": #prove all initial states
            #for i in range(2**self.size):
                #if i == self.bin2int(self.stateTransition(i)):
                    #self.attractors[i] = None
            #return self.attractors
        #if method == "random":
            #for ns in range(n_states):
                #i = randint(0, 2**self.size-1)
                #if i == self.bin2int(self.stateTransition(i)):
                    #self.attractors[i] = None
            #return self.attractors
    
    #def getAttractors(self):
        ##return a dictionary of solutions (including cycles) and sizes of basin of attractio
        #try: self.transitionGraph
        #except AttributeError: self.getTransitionGraph()
        #try: self.attractors
        #except AttributeError: self.attractors = {}
        #solutions = list(nx.simple_cycles(self.transitionGraph))
        #for s in solutions:
            ##calculate basin size of solutions
            ##s[0] to get only one item from each cycles
            ##+1 to count itself
            #if len(s) == 1: self.attractors[s[0]] = len(nx.ancestors(self.transitionGraph,s[0]))+1
            #if len(s) > 1: self.attractors[tuple(s)] = len(nx.ancestors(self.transitionGraph,s[0]))+1
        #return self.attractors
        
        
    
    #def int2bin(self, i, size=None): #takes int, return array
        #if size is None: size = self.size
        #form = '{0:0'+str(size)+'b}'
        #return [int(n) for n in form.format(i)]
    
    #def bin2int(self, binA): #takes array with boolean, returns int
        #n = 0
        #for i in range(len(binA)): n += binA[i]*2**(len(binA)-i-1)
        #return int(n) # int(''.join(str(i) for i in binA),2)
    
    #def __str__(self): #print network rules TODO
        #text = ''
        #for (i, j) in zip(self.nodesID, self.functionsText):
            #text += '%s = %s\n' % (i, j)
        #return text.strip()
        
def boolnet2regnet(): #TODO including where
    pass

def tab2array(text): #receives text in tabular format and converts it to array
    #first line is ordered node names
    #the rest is the weight between interactions
    text = text.strip().split('\n')
    matrix = []
    for t in text:
        try: matrix.append(  map(int, t.strip().split())  )
        except: matrix.append( t.strip().split() )
    #for m in matrix: print m
    return matrix

#Main
text_functions = """
    a = a
    b = a and not c
    c = c and not b
    """
text_matrix = """
    a\tb\tc
    1\t1\t0
    0\t0\t-1
    0\t-1\t1
    """

#example_functions = regNet(text_functions)

matrix = tab2array(text_matrix)
example_matrix = regNet(matrix,"weight_matrix")

#example.getSteadyStates()
#print example.attractors

#example.getTransitionGraph()
#print example.transitionGraph.edges()
#example.getAttractors()
#print example.attractors