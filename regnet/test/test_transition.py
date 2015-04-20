import sys
sys.path.append("../")

import unittest
import transition
from regnet import RegNet



class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        text_functions = """
            a = a
            b = a and not c
            c = c and not b
            """
        self.network = RegNet(text_functions, "lambda_bool", verbose=False)
        self.states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        

    def test_lambda_bool_all_sync(self):
        sol_all_sync = [[0,0,0], [0,0,1], [0,0,0], [0,0,0], [1,1,0], [1,0,1], [1,1,0], [1,0,0] ]
        for s, sol in zip(self.states, sol_all_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes='all') , sol )


    def test_lambda_bool_random_sync(self):
        sol_all_sync = [[0,0,0], [0,0,1], [0,0,0], [0,0,0], [1,1,0], [1,0,1], [1,1,0], [1,0,0] ]
        for s, sol in zip(self.states, sol_all_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes='random') , sol )


    def test_lambda_bool_list_sync(self):
        sol_list_sync = [[0,0,0], [0,0,1], [0,1,0], [0,1,0], [1,0,0], [1,0,1], [1,1,0], [1,1,0] ]
        for s, sol in zip(self.states, sol_list_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes=['a','c']) , sol )


    def test_lambda_bool_node_sync(self):
        sol_node_sync = [[0,0,0], [0,0,1], [0,0,0], [0,0,1], [1,1,0], [1,0,1], [1,1,0], [1,0,1] ]
        for s, sol in zip(self.states, sol_node_sync):
            self.assertEqual( transition.state_transition(s, self.network, method="sync", nodes='b') , sol )



    def test_lambda_bool_all_async(self):
        #supose order: a, b, c
        sol_all_async = [[0,0,0], [0,0,1], [0,0,0], [0,0,1], [1,1,0], [1,0,1], [1,1,0], [1,0,1] ]
        for s, sol in zip(self.states, sol_all_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='all') , sol )


    def test_lambda_bool_list_async(self):
        #supose order: c, b
        sol_list_async = [[0,0,0], [0,0,1], [0,0,0], [0,0,0], [1,1,0], [1,0,1], [1,1,0], [1,1,0] ]
        for s, sol in zip(self.states, sol_list_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes=['c', 'b']) , sol )


    def test_lambda_bool_node_async(self):
        sol_a_async = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1] ]
        sol_b_async = [[0,0,0], [0,0,1], [0,0,0], [0,0,1], [1,1,0], [1,0,1], [1,1,0], [1,0,1] ]
        sol_c_async = [[0,0,0], [0,0,1], [0,1,0], [0,1,0], [1,0,0], [1,0,1], [1,1,0], [1,1,0] ]
        for s, sol in zip(self.states, sol_a_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='a') , sol )
        for s, sol in zip(self.states, sol_b_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='b') , sol )
        for s, sol in zip(self.states, sol_c_async):
            self.assertEqual( transition.state_transition(s, self.network, method="async", nodes='c') , sol )



    def test_get_trajectory_sync(self):
        self.assertEqual( transition.get_trajectory([1,1,1], self.network, "sync", 4), [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0]] )
        self.assertEqual( transition.get_trajectory([1,1,1], self.network, "sync"), [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 1, 0]] )


    def test_get_trajectory_async(self):
        end_states = [[1,1,1], [1,0,1], [1,1,0]]
        self.assertIn( transition.get_trajectory([1,1,1], self.network, "async", 4)[-1] , end_states)
        self.assertIn( transition.get_trajectory([1,1,1], self.network, "async")[-1] , end_states)


    def test_get_trajectory_async_all(self):
        end_states = [[1,0,1], [1,1,0]]
        self.assertIn( transition.get_trajectory([1,1,1], self.network, "async-all", 4)[-1] , end_states)
        self.assertIn( transition.get_trajectory([1,1,1], self.network, "async-all")[-1] , end_states)
        

if __name__ == '__main__':
    unittest.main()

