import unittest
from alphasix.utils import atoc

class TestUtils(unittest.TestCase):
    
    def test_atoc(self) -> None:
        """Tests converting action into coordinates.
        """
        
        coord1, coord2 = atoc(361, 19)
        self.assertEqual([*coord1, *coord2], [0, 1, 0, 3])
        
        coord1, coord2 = atoc(1076, 19)
        self.assertEqual([*coord1, *coord2], [0, 2, 18, 18])
        
        
        