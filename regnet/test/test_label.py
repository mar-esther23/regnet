import sys
sys.path.append("../")

import unittest
import label



class TestSequenceFunctions(unittest.TestCase):

    def test_create_label_functions(self):
        #inputs
        node_names = ['a', 'b', 'c']
        data = """
        none = not a and not b and not c
        ab = a and b
        c = c
        """

        functions = label.create_label_functions(node_names, data)
        self.assertEqual(functions['none']([0,0,0]), True)
        self.assertEqual(functions['ab']([1,1,0]), True)
        self.assertEqual(functions['c']([0,0,1]), True)
        self.assertEqual(functions['none']([1,0,1]), False)


    def test_label_state(self):
        #inputs
        node_names = ['a', 'b', 'c']
        data = """
        none = not a and not b and not c
        ab = a and b
        c = c
        """
        states = ["000", "001", "100", "101", "110", "111"]
        labels = ['none', 'c', '', 'c', 'ab', 'c/ab']

        functions = label.create_label_functions(node_names, data)
        for s, l in zip(states, labels):
            self.assertEqual(label.label_state(s, functions), l)







if __name__ == '__main__':
    unittest.main()