import unittest
from alphasix.utils import atoc

class TestUtils(unittest.TestCase):
    
    def test_atoc(self) -> None:
        """Tests converting an action into the corresponding coordinates.
        """
        
        self.assertRaises(ValueError, atoc, -1, 13)
        self.assertRaises(ValueError, atoc, 64980, 19)
        
        coords = atoc(361, 19)
        self.assertEqual(coords, ((0, 1), (0, 3)))
        
        coords = atoc(1076, 19)
        self.assertEqual(coords, ((0, 2), (18, 18)))
        
        
        