import sys
sys.path.append("../")

import unittest
import states


class TestSequenceFunctions(unittest.TestCase):

    def test_base_converters(self):
        self.assertEqual( states.dec_to_base_array(6,5), [0,0,1,1,0] )
        self.assertEqual( states.dec_to_base_array(6,5,3), [0,0,0,2,0])
        self.assertEqual( states.base_array_to_dec([0,0,1,1,0]), 6)
        self.assertEqual( states.base_array_to_dec([0,0,0,2,0],3), 6)

        self.assertEqual( states.dec_to_bin_array(6, 5), [0,0,1,1,0] )
        self.assertEqual( states.bin_array_to_dec([0,0,1,1,0]), 6 )

        self.assertEqual( states.state_to_str([0,11,1,3,0]), '0B130' )
        self.assertEqual( states.str_to_state('0B130'), [0,11,1,3,0] )


    def test_generators(self):
        test_states = [[int(i) for i in bin(j)[2:].zfill(3)] for j in range(8)]
        for i, j in zip(test_states, states.generate_all_base_array_states(3)):
            self.assertEqual(  i, j )
        for j in states.generate_random_base_array_states(5, 3):
            self.assertIn(j, test_states)


    def test_verify_states(self):
        self.assertEqual( states.validate_state([1,1,0], 3), True )
        self.assertEqual( states.validate_state((1,1,0), 3), True )
        self.assertEqual( states.validate_state([1,3,0], 3), False )
        self.assertEqual( states.return_valid_states( ['11010', (0,1,0,0,0)], 5)    ,   [[1,1,0,1,0], [0,1,0,0,0]] )
        self.assertEqual( states.return_valid_states( [0,1,0,0,0], 5)    ,   [[0,1,0,0,0]] )
        with self.assertRaises(TypeError): states.return_valid_states( [0,3], 2)
        with self.assertRaises(TypeError): states.return_valid_states( ['011'], 2)



if __name__ == '__main__':
    unittest.main()
