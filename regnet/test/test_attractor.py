import sys
sys.path.append("../")

import unittest
import networkx as nx
from attractor import Attractor



class TestSequenceFunctions(unittest.TestCase):

    def test_create_node_lambda_bool(self):
        #inputs
        states = ['00','11']
        f_type = "lambda_bool"
        node_names = ['a','b']
        basin = 2
        label = "cycle"
        graph = nx.DiGraph(states)

        #declare node
        attr = Attractor(states, f_type, node_names, basin, label, graph)

        # inputs == node
        self.assertEqual( f_type, attrf._type)
        self.assertEqual( node_names, attr.node_names)
        self.assertEqual( basin, attr.basin)
        self.assertEqual( label, attr.label)
        self.assertEqual( graph, attr.graph)






if __name__ == '__main__':
    unittest.main()


