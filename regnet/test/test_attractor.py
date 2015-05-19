import sys
sys.path.append("../")

import unittest
import networkx as nx
from attractor import Attractor



class TestSequenceFunctions(unittest.TestCase):

    def test_create_attr(self):
        #inputs
        states = ['00','11']
        f_type = "lambda_bool"
        node_names = ['a','b']
        basin = 4
        label = "cycle"
        graph = nx.DiGraph(states)
        sol = [[0,0], [1,1]] 

        #declare attr
        attr = Attractor(states, f_type, node_names, basin, label, graph)

        # inputs == attr
        self.assertEqual( f_type, attr.f_type)
        self.assertEqual( node_names, attr.node_names)
        self.assertEqual( basin, attr.basin)
        self.assertEqual( label, attr.label)
        self.assertEqual( graph, attr.graph)
        self.assertEqual( sol, attr.states)


    def test_modify_attr(self):
        #inputs
        old_states = ['11','00']
        new_states = ['11','10', '00', '01', '11']
        f_type = "lambda_bool"
        node_names = ['a','b']
        old_sol = [[0,0], [1,1]] 
        new_sol = [[0,0], [0,1], [1,1], [1,0]] 

        #declare attr
        attr = Attractor(old_states, f_type, node_names)
        self.assertEqual( old_sol, attr.states)
        #modify states
        attr.states = new_states
        self.assertEqual( new_sol, attr.states)






if __name__ == '__main__':
    unittest.main()


