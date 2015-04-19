import regnet as rn
import networkx as nx

text_functions = """
	a = a
    b = a and not c
    c = c and not b
    """

interaction_matrix = [
	['a', 'b', 'c'],
    [ 1,  1,  0 ],
    [ 0,  0, -1 ],
    [ 0, -1,  1 ]
    ]

table_bool = [
 	['a', ['a'], [0,1]]
 	['b', ['a', 'c'], [0,0,1,0]], 
 	['c', ['b', 'c'], [0,1,0,0]]
 	]

state = [1,1,1]

example_functions = rn.RegNet(text_functions)
print example_functions
print state, rn.state_transition(state, example_functions, method="sync", nodes="all")
print

example_interact = rn.RegNet(interaction_matrix, "interact_bool")
print example_interact
print state, rn.state_transition(state, example_interact)
print

example_table = rn.RegNet(table_bool, "table_bool")
print example_table
print state, rn.state_transition(state, example_table)
print