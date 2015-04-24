import sys
sys.path.append("../")

import unittest
from node import Node



class TestSequenceFunctions(unittest.TestCase):

    def test_create_node_lambda_bool(self):
    	#inputs
        name = "c"
        f_type = "lambda_bool"
        f_base = 2
        index = 0
        function = lambda b , c : c and not b
        str_function = "c = c and not b"
        regulators = ["b", "c"]

        #declare node
        node = Node(name, f_type, f_base, index, function, str_function, regulators)

        # inputs == node
        self.assertEqual( node.name, name )
        self.assertEqual( node.f_type, f_type )
        self.assertEqual( node.f_base, f_base )
        self.assertEqual( node.index, index )
        self.assertEqual( node.function, function )
        self.assertEqual( node.str_function, str_function )
        self.assertEqual( node.regulators, regulators )

    def test_node_fix_value(self):
        name = "c"
        f_type = "lambda_bool"
        f_base = 2
        index = 0
        function = lambda b , c : c and not b
        str_function = "c = c and not b"
        regulators = ["b", "c"]

        #declare node
        node = Node(name, f_type, f_base, index, function, str_function, regulators)

        #fix value
        value = 2
        node.fix_node(value)
        self.assertEqual( node.fixed, True)
        self.assertEqual( node.function([0,0]), value )
        self.assertEqual( node.str_function, "c = " + str(value) )

        #unfix value
        node.unfix_node()
        self.assertEqual( node.fixed, False)
        self.assertEqual( node.function, function )
        self.assertEqual( node.str_function, str_function )



if __name__ == '__main__':
    unittest.main()


