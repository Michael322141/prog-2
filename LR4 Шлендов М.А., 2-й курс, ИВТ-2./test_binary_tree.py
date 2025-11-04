"""
Unit tests for binary tree generation functions.
"""

import unittest
from collections import deque
from binary_tree import gen_bin_tree, gen_bin_tree_deque, gen_bin_tree_namedtuple, TreeNode


class TestBinaryTree(unittest.TestCase):
    """Test cases for binary tree generation functions."""
    
    def test_gen_bin_tree_default_params(self):
        """Test tree generation with default parameters."""
        tree = gen_bin_tree()
        
        # Check root node
        self.assertEqual(tree['value'], 12)
        self.assertIsInstance(tree, dict)
        self.assertIn('left', tree)
        self.assertIn('right', tree)
    
    def test_gen_bin_tree_custom_params(self):
        """Test tree generation with custom parameters."""
        tree = gen_bin_tree(
            height=3,
            root=5,
            left_leaf=lambda x: x + 1,
            right_leaf=lambda x: x + 2
        )
        
        self.assertEqual(tree['value'], 5)
        self.assertEqual(tree['left']['value'], 6)  # 5 + 1
        self.assertEqual(tree['right']['value'], 7)  # 5 + 2
    
    def test_gen_bin_tree_height_1(self):
        """Test tree generation with height 1."""
        tree = gen_bin_tree(height=1, root=10)
        
        self.assertEqual(tree['value'], 10)
        self.assertIsNone(tree['left'])
        self.assertIsNone(tree['right'])
    
    def test_gen_bin_tree_invalid_height(self):
        """Test tree generation with invalid height."""
        with self.assertRaises(ValueError):
            gen_bin_tree(height=0)
        
        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1)
    
    def test_gen_bin_tree_default_algorithms(self):
        """Test tree generation with default algorithms."""
        tree = gen_bin_tree(height=2, root=2)
        
        # Test default left_leaf: root ^ 3
        self.assertEqual(tree['left']['value'], 8)  # 2^3 = 8
        
        # Test default right_leaf: (root * 2) - 1
        self.assertEqual(tree['right']['value'], 3)  # (2*2)-1 = 3
    
    def test_gen_bin_tree_structure(self):
        """Test the complete tree structure."""
        tree = gen_bin_tree(height=3, root=2)
        
        # Level 1
        self.assertEqual(tree['value'], 2)
        
        # Level 2
        self.assertEqual(tree['left']['value'], 8)   # 2^3
        self.assertEqual(tree['right']['value'], 3)  # (2*2)-1
        
        # Level 3
        self.assertEqual(tree['left']['left']['value'], 512)    # 8^3
        self.assertEqual(tree['left']['right']['value'], 15)    # (8*2)-1
        self.assertEqual(tree['right']['left']['value'], 27)    # 3^3
        self.assertEqual(tree['right']['right']['value'], 5)    # (3*2)-1
    
    def test_gen_bin_tree_deque(self):
        """Test tree generation with deque storage."""
        tree_deque = gen_bin_tree_deque(height=2, root=2)
        
        self.assertIsInstance(tree_deque, deque)
        # Level-order: 2, 8, 3, None, None, None, None
        expected_values = [2, 8, 3, None, None, None, None]
        self.assertEqual(list(tree_deque), expected_values)
    
    def test_gen_bin_tree_namedtuple(self):
        """Test tree generation with namedtuple representation."""
        tree = gen_bin_tree_namedtuple(height=2, root=2)
        
        self.assertIsInstance(tree, TreeNode)
        self.assertEqual(tree.value, 2)
        self.assertEqual(tree.left.value, 8)
        self.assertEqual(tree.right.value, 3)
        self.assertIsNone(tree.left.left)  # Height 2, so no grandchildren
    
    def test_different_leaf_algorithms(self):
        """Test tree generation with various leaf algorithms."""
        # Linear functions
        tree1 = gen_bin_tree(
            height=2,
            root=1,
            left_leaf=lambda x: x * 2,
            right_leaf=lambda x: x * 3
        )
        
        self.assertEqual(tree1['left']['value'], 2)
        self.assertEqual(tree1['right']['value'], 3)
        
        # Constant functions
        tree2 = gen_bin_tree(
            height=2,
            root=1,
            left_leaf=lambda x: 10,
            right_leaf=lambda x: 20
        )
        
        self.assertEqual(tree2['left']['value'], 10)
        self.assertEqual(tree2['right']['value'], 20)
        
        # Complex functions
        tree3 = gen_bin_tree(
            height=2,
            root=3,
            left_leaf=lambda x: x ** 2 + 1,
            right_leaf=lambda x: x * x - 1
        )
        
        self.assertEqual(tree3['left']['value'], 10)  # 3^2 + 1
        self.assertEqual(tree3['right']['value'], 8)  # 3*3 - 1


if __name__ == '__main__':
    unittest.main()
