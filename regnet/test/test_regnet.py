import sys
sys.path.append("../")

import unittest
from regnet import RegNet



class TestSequenceFunctions(unittest.TestCase):

    def test_lambda_bool_nodes(self):
        text_functions = """
            b = a and not c
            c = c and not b
            """
        network = RegNet(text_functions, "lambda_bool", verbose=False)

        self.assertEqual("lambda_bool", network.f_type)
        self.assertIn("a", network)
        self.assertIn("b", network)
        self.assertIn("c", network)
        self.assertNotIn("and", network)
        self.assertNotIn("or", network)
        self.assertNotIn("not", network)


    def test_lambda_bool_graph(self):
        text_functions = """
            b = a and not c
            c = c and not b
            """
        network = RegNet(text_functions, "lambda_bool", verbose=False)

        edges = [ ('a','a'), ('a','b'), ('c','b'), ('c','c'), ('b','c') ]
        for e in edges:
            self.assertIn(e, network.graph.edges())


    def test_lambda_bool_input_nodes(self):
        text_functions = """
            b = a and not c
            c = c and not b
            """
        network = RegNet(text_functions, "lambda_bool", verbose=False)

        self.assertEqual(network['a'].input, True)
        self.assertEqual(network['b'].input, False)
        self.assertEqual(network['c'].input, False)



    # def test_matrix_bool_nodes(self):
    #     interaction_matrix = [ 
    #       ['a', 'b', 'c'],
    #         [ 1,  1,  0 ],
    #         [ 0,  0, -1 ],
    #         [ 0, -1,  1 ] ]
    #     network = RegNet(interaction_matrix, "matrix_bool", verbose=False)

    #     self.assertEqual("matrix_bool", network.f_type)
    #     self.assertIn("a", network)
    #     self.assertIn("b", network)
    #     self.assertIn("c", network)
    #     self.assertNotIn("and", network)
    #     self.assertNotIn("or", network)
    #     self.assertNotIn("not", network)


    # def test_graph_matrix_bool(self):
    #     interaction_matrix = [ 
    #       ['a', 'b', 'c'],
    #         [ 1,  1,  0 ],
    #         [ 0,  0, -1 ],
    #         [ 0, -1,  1 ] ]
    #     network = RegNet(interaction_matrix, "matrix_bool", verbose=False)

    #     edges = [ ('a','a'), ('a','b'), ('c','b'), ('c','c'), ('b','c') ]
    #     for e in edges:
    #         self.assertIn(e, network.graph.edges())



    def test_table_bool_nodes(self):
        table_bool = [
             ['a', ['a'], [0,1]],
             ['b', ['a', 'c'], [0,0,1,0]], 
             ['c', ['b', 'c'], [0,1,0,0]] ]
        network = RegNet(table_bool, "table_bool", verbose=False)

        self.assertEqual("table_bool", network.f_type)
        self.assertIn("a", network)
        self.assertIn("b", network)
        self.assertIn("c", network)
        self.assertNotIn("and", network)
        self.assertNotIn("or", network)
        self.assertNotIn("not", network)


    def test_table_bool_graph(self):
        table_bool = [
             ['a', ['a'], [0,1]], 
             ['b', ['a', 'c'], [0,0,1,0]], 
             ['c', ['b', 'c'], [0,1,0,0]] ]
        network = RegNet(table_bool, "table_bool", verbose=False)

        edges = [ ('a','a'), ('a','b'), ('c','b'), ('c','c'), ('b','c') ]
        for e in edges:
            self.assertIn(e, network.graph.edges())



if __name__ == '__main__':
    unittest.main()











