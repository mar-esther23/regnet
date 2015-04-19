import sys
sys.path.append("../")

import unittest
import transition
from regnet import RegNet



class TestSequenceFunctions(unittest.TestCase):

    def test_lambda_bool_all_sync(self):
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        sol_all_sync = [[0,0,0], [0,0,1], [0,0,0], [0,0,0], [1,1,0], [1,0,1], [1,1,0], [1,0,0] ]
        
        for s, sol in zip(states, sol_all_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes='all') , sol )


    def test_lambda_bool_random_sync(self):
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        sol_all_sync = [[0,0,0], [0,0,1], [0,0,0], [0,0,0], [1,1,0], [1,0,1], [1,1,0], [1,0,0] ]
        
        for s, sol in zip(states, sol_all_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes='random') , sol )


    def test_lambda_bool_list_sync(self):
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        sol_list_sync = [[0,0,0], [0,0,1], [0,1,0], [0,1,0], [1,0,0], [1,0,1], [1,1,0], [1,1,0] ]
        
        for s, sol in zip(states, sol_list_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes=['a','c']) , sol )


    def test_lambda_bool_node_sync(self):
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        sol_node_sync = [[0,0,0], [0,0,1], [0,0,0], [0,0,1], [1,1,0], [1,0,1], [1,1,0], [1,0,1] ]
        
        for s, sol in zip(states, sol_node_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes='b') , sol )



    def test_lambda_bool_all_async(self):
        pass
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        #supossed order: a, b, c

        sol_all_async = [[0,0,0], [0,0,1], [0,0,0], [0,0,1], [1,1,0], [1,0,1], [1,1,0], [1,0,1] ]
        
        for s, sol in zip(states, sol_all_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='all') , sol )


    def test_lambda_bool_random_async(self):
        pass


    def test_lambda_bool_list_async(self):
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        #supossed order: c, b
        sol_list_async = [[0,0,0], [0,0,1], [0,0,0], [0,0,0], [1,1,0], [1,0,1], [1,1,0], [1,1,0] ]
        
        for s, sol in zip(states, sol_list_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes=['c', 'b']) , sol )


    def test_lambda_bool_node_async(self):
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        sol_a_async = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1] ]
        sol_b_async = [[0,0,0], [0,0,1], [0,0,0], [0,0,1], [1,1,0], [1,0,1], [1,1,0], [1,0,1] ]
        sol_c_async = [[0,0,0], [0,0,1], [0,1,0], [0,1,0], [1,0,0], [1,0,1], [1,1,0], [1,1,0] ]
        
        for s, sol in zip(states, sol_a_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='a') , sol )
        for s, sol in zip(states, sol_b_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='b') , sol )
        for s, sol in zip(states, sol_c_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='c') , sol )



if __name__ == '__main__':
    unittest.main()

