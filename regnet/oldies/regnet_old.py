from random import shuffle, randint
from collections import OrderedDict
import matplotlib.pyplot as plt
#from itertools import zip
import networkx as nx
import numpy as np
import re

class regNet(object):
    def __init__(self,data,f_type="lambda_bool", threshold=1):
        
        #The main structure is a networkx directed graph        
        self.graph = nx.DiGraph() #networkx graph (dictionary)
        self.f_type = f_type #type of function of the network
        self.nodes = () #ordered dict with node names in aparition order
        #self.functions = () #ordered tuple with lambda functions in aparition order
        #self.f_text = () #ordered tuple with text of functions in aparition order for printing
        #self.weight_bool = np.array() #matrix with weight of interactions
    
        if self.f_type == "lambda_bool":
            #receives a text in format: node = regulatory function
            #each node in newline
            #nodes are declared in order of aparition
            #functions are lambda functions which return 0 or 1
            
            self.functions = []
            self.f_text = []
            
            #declare nodes and f_text
            for line in data.strip().split('\n'):
                self.nodes.append(line.split('=')[0].strip())
                self.f_text.append(line.split('=')[1].strip())
            self.nodes = tuple(self.nodes)
            self.f_text = tuple(self.f_text)
            
            #declare functions as numpy matrix to multiply state
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
            #TODO declare weight_bool
            self.weight_bool = nx.to_numpy_matrix(self.graph, nodelist=self.nodes)
            self.threshold = threshold
    
    
        elif self.f_type == "weight_bool":
            #receives a weight matrix and a threshold
            #the first line of the array is the ordered name of the nodes
            #the rest is a square matrix with weight numbers
            #the result is always boolean
            
            self.functions = []
            self.f_text = []
            
            #declare nodes, matrix and f_text
            self.nodes = tuple(data[0])
            self.weight_bool =  np.asmatrix(data[1::])
            self.threshold = threshold
            for i in range(len(self.weight_bool)): #things are printed as a tuple
                self.f_text.append(str(   tuple(map(int,self.weight_bool[:,i]))   ))
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
                #n_i(t+1) = {1 if \sum (state * weights) >= threshold
                #            0 else
                #node is 1 if there are more activators
                self.functions.append(eval('lambda state, threshold: 1 if sum(state * np.array(' + f + ')) >= threshold else 0')) #eval to declare as f()
            self.functions = tuple(self.functions)
        else: print "Incorrect function type"



    def __str__(self): #print network rules
        text = self.f_type + '\n'
        for (n, f) in zip(self.nodes, self.f_text):
            text += '%s = %s\n' % (n, f)
        return text.strip()
    
    
    
    
    
    #EVALUATE NETWORK
    def stateTransition(self, state, method="sync", eval_order=None):
        #takes a states and iterates the network once
        #returns new state vector
        
        #format state to numpy array
        if type(state)==int: state = self.int2bin(state)
        state = np.array(state)
        
        if self.f_type == "lambda_bool": #each node has lambda function that return 0 or 1
            
            if method == "sync":  #eval all nodes at the same time
                new_state = [0]*len(state) #create new vector for sync eval
                for i in range(len(state)): 
                    new_state[i] = int(self.functions[i](state))
                return new_state
            
            elif method == "async": #eval nodes asynchronous
                if eval_order == None: #if we are not given a node order
                    eval_order = [i for i in range(len(state))] #randomly evaluate all nodes 
                    shuffle(eval_order)
                for i in eval_order: #eval with lambda functions
                    state[i] = int(self.functions[i](state))
                return state
            
            
        elif self.f_type == "weight_bool":
            
            if method == "sync":  #eval all nodes at the same time
                #print np.shape(state),  np.shape(self.weight_bool)
                new_state = np.array(state) * self.weight_bool
                new_state = np.squeeze(np.asarray(new_state)) #reshape into 1D vector
                new_state = [1 if n>=self.threshold else 0 for n in new_state] #threshold
                return new_state
            
            elif method == "async": #eval nodes asynchronous
                #we can do this because each node has all the necessary operations defined
                if eval_order == None: #if we are not given a node order
                    eval_order = [i for i in range(len(state))] #randomly evaluate all nodes 
                    shuffle(eval_order)
                for i in eval_order: #eval with lambda functions
                    state[i] = int(self.functions[i](state))
                return state
                
                
                
    def getTransitionGraph(self, method="sync", initial_states=0, iter_steps=1):  #TODO make sure it receives non bool networks
        #takes the network
        #if int we suposse it is a boolean state
        #return a networkx graph with transitions
        self.transitionGraph = nx.DiGraph()
        if method=="sync":
            for i in range(2**len(self.nodes)): #generate initial states
                self.transitionGraph.add_edge(i, self.bin2int(self.stateTransition(i)))
        if method=="async":
            for i in range(2**len(self.nodes)): #generate initial states
                for j in range(len(self.nodes)): #evaluate each node one by one
                    self.transitionGraph.add_edge(i, self.bin2int(self.stateTransition(i, "async", [j])))
        if method=="random":
            for ns in range(initial_states):
                for ni in range(iter_steps):
                    i = randint(0, 2**len(self.nodes)-1)
                    j = self.bin2int(self.stateTransition(i))
                    self.transitionGraph.add_edge(i, j)
                    if i == j: break
                    else: i = j
        return self.transitionGraph
    
    def getSteadyStates(self, method="all", n_states=0): #TODO add cycles
        #calculates steady states, useful for big boolean networks
        try: self.attractors
        except AttributeError: self.attractors = {}
        if method == "all": #prove all initial states
            i = 0
            while i < 2**len(self.nodes):
                #print i, self.stateTransition(i)
                if i == self.bin2int(self.stateTransition(i)):
                    self.attractors[i] = None
                i += 1
            return self.attractors
        if method == "random":
            for ns in range(n_states): #number of iterations
                i = randint(0, 2**len(self.nodes)-1)
                if i == self.bin2int(self.stateTransition(i)):
                    self.attractors[i] = None
            return self.attractors
    
    def getAttractors(self): #TODO check cycles
        #return a dictionary of solutions (including cycles) and sizes of basin of attraction
        try: self.transitionGraph #search for the transitionGraph
        except AttributeError: self.getTransitionGraph()
        try: self.attractors #declare attractors dictionary
        except AttributeError: self.attractors = {}
        solutions = list(nx.simple_cycles(self.transitionGraph)) #determine solutions with nx
        #print solutions
        for s in solutions:
            #calculate basin size of solutions
            #s[0] to get only one item from each cycles
            #+1 to count itself
            #print s
            if len(s) == 1: self.attractors[s[0]] = len(nx.ancestors(self.transitionGraph,s[0]))+1
            if len(s) > 1: self.attractors[tuple(s)] = len(nx.ancestors(self.transitionGraph,s[0]))+1
        return self.attractors



    #MATH FUNCTIONS
    def int2bin(self, i, size=None): #takes int, return array
        if size is None: size = len(self.nodes)
        form = '{0:0'+str(size)+'b}'
        return [int(n) for n in form.format(i)]
    
    def bin2int(self, binA): #takes array with boolean, returns int
        n = 0
        for i in range(len(binA)): n += binA[i]*2**(len(binA)-i-1)
        return int(n) # int(''.join(str(i) for i in binA),2)


    #GRAPHS
    def plotAttractors(self,name="Attractors"):
        #data is attractor dictionary
        #   attr:basin OR (cycle):basin
        
        data = self.attractors.items() #convierte a array por orden
        #print self.nodes #yticks
        #print self.attractors.keys() #xticks down
        #print self.attractors.values() #xticks up
        
        #tomar cada attractor y convertirlo en dos arrays
        #el primero es en booleano el numero de estados, checa si tuple
        #el segundo es la cuenca
        #aqui es donde tienes que pensar como contar si es ciclo o no
        
        #luego manda heatmap con lineas extra
        
    
    
    #plt.clf()
    #fig = plt.figure()
    #ax = fig.gca()
    ##delete top and right axis
    ##ax.spines['top'].set_visible(False)
    ##ax.spines['right'].set_visible(False)
    #ax.get_xaxis().tick_bottom()
    #ax.get_yaxis().tick_left()
    ### put the major ticks at the middle of each cell
    #ax.set_xticks(np.arange(data.shape[1]), minor=False)
    #ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ### want a more natural, table-like display
    ###ax.invert_yaxis()
    ###ax.xaxis.tick_top()
    #ax.set_xticklabels(x_tick_labels, minor=False)
    #ax.set_yticklabels(y_tick_labels, minor=False)
    ##set colorbar
    #cdict = {'red':   [(0,.7,.7),(1,0,0)],
             #'green': [(0,0,0),(1,1,1)],
             #'blue':  [(0,0,0),(1,0,0)]}
    #my_cmap=colors.LinearSegmentedColormap('my_colormap',cdict,256)
    ##heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    #heatmap = ax.pcolor(data, cmap=my_cmap, vmin=0, vmax=1,edgecolors='k', lw=.25)
    #cbar = plt.colorbar(heatmap)
    #plt.title(name)
    #plt.xlabel(x_label)
    #plt.ylabel(y_label)
    #plt.plot()
    ##grid to separeate states
    #grid = ['-','-','None']
    #for i in range(len(grid)):
        #plt.axvline(x=i+1, lw=2, ls=grid[i], color='k')
    
    
    ##save plot
    #f_format = name.split('.')[-1]
    #name = name.split('.')[0]
    #plt.savefig(name+'.'+f_format, format=f_format, bbox_inches='tight')
    ##plt.show()




# HELPER FUNCTIONS

def boolnet2regnet(file_name): #takes file name of boolnet rules and formats
    with open(file_name,'r') as f: data = f.read()
    data = data[data.index('\n')::] #remove first line
    data = data.replace(',',' =').replace('&','and').replace('|','or').replace('!','not') #change operands
    return data.strip()

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

def bipartite2weight(): #TODO
    pass




"""

M   M     AA  III  N   N
MM MM    A A   I   NN  N
M M M   A  A   I   N N N
M   M  AAAAA   I   N  NN
M   M A    A  III  N   N

"""

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


example = regNet(text_functions)
#matrix = tab2array(text_matrix)
#example = regNet(matrix,"weight_bool")

# f = open('PlantGrasshopperMatrix.dat', 'r')
# matrix = []
# for line in f:
#     line = line.strip().split()
#     try: line = [int(l) for l in line]
#     except ValueError: pass 
#     matrix.append(line)
# #print matrix[0]
# #print len(matrix), len(matrix[0]), len(matrix[1])
# example = regNet(matrix,"weight_bool")

print 'red'
print example
print 'numero de nodos'
print len(example.nodes)


example.getSteadyStates()
print 'attractors'
print example.attractors

example.getTransitionGraph()
print 'transitionGraph'
print example.transitionGraph.edges()

example.getAttractors()
print 'attractors'
print example.attractors

nx.draw(example.transitionGraph)
plt.show()

#example.plotAttractors()