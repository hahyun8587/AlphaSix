import unittest
import numpy as np
from alphasix.alphasixsimulator import AlphaSixSimulator

class TestAlphaSixSimulator(unittest.TestCase):
    """Test case of `AlphaSixSimulator`.
    """
    
    def setUp(self) -> None:
        self._sim_large = AlphaSixSimulator(19, 5)
        self._sim_small = AlphaSixSimulator(13, 3)


    def test_gen_init_s(self) -> None:
        """Test generating initial state. 
        """
        
        init_s_large = self._sim_large.gen_init_s() 
        
        n_red = np.equal(init_s_large[0], AlphaSixSimulator.RED).sum()
        self.assertLessEqual(n_red, 5)
        
        center = init_s_large[0][init_s_large.shape[1] // 2][init_s_large.shape[2] // 2]
        self.assertEqual(center, AlphaSixSimulator.BLACK)
        
        n_blank = np.equal(init_s_large[0], 0).sum()
        self.assertEqual(n_blank, init_s_large[0].size - n_red - 1)
        
        is_white_turn = np.equal(init_s_large[1], AlphaSixSimulator.WHITE).all()
        self.assertTrue(is_white_turn)
        
        init_s_small = self._sim_small.gen_init_s() 
        
        n_red = np.equal(init_s_small[0], AlphaSixSimulator.RED).sum()
        self.assertLessEqual(n_red, 3)
        
        center = init_s_small[0][init_s_small.shape[1] // 2][init_s_small.shape[2] // 2]
        self.assertEqual(center, AlphaSixSimulator.BLACK)
        
        n_blank = np.equal(init_s_small[0], 0).sum()
        self.assertEqual(n_blank, init_s_small[0].size - n_red - 1)
        
        is_white_turn = np.equal(init_s_small[1], AlphaSixSimulator.WHITE).all()
        self.assertTrue(is_white_turn)
        
    
        