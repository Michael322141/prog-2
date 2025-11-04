"""
Module for generating binary trees using non-recursive approach.

This module provides functionality to create binary trees with customizable
node generation algorithms and different data structures for storage.
"""

from collections import deque, namedtuple
from typing import Any, Callable, Optional, Dict, Union


# Named tuple for tree node representation using collections
TreeNode = namedtuple('TreeNode', ['value', 'left', 'right'])


def gen_bin_tree(
    height: int = 4,
    root: int = 12,
    left_leaf: Optional[Callable[[int], int]] = None,
    right_leaf: Optional[Callable[[int], int]] = None
) -> Dict[str, Any]:
    """
    Generate a binary tree using non-recursive approach.
    
    This function creates a binary tree with specified height and root value,
    using provided algorithms for generating left and right children.
    
    Args:
        height: The height of the tree (default: 4)
        root: The value of the root node (default: 12)
        left_leaf: Function to calculate left child value (default: root ^ 3)
        right_leaf: Function to calculate right child value (default: (root * 2) - 1)
    
    Returns:
        A dictionary representing the binary tree structure with keys:
        'value', 'left', 'right'.
    
    Raises:
        ValueError: If height is less than 1
        
    Example:
        >>> tree = gen_bin_tree(height=3, root=5)
        >>> isinstance(tree, dict)
        True
    """
    if height < 1:
        raise ValueError("Height must be at least 1")
    
    # Set default algorithms if not provided
    if left_leaf is None:
        left_leaf = lambda x: x ** 3  # root ^ 3
        
    if right_leaf is None:
        right_leaf = lambda x: (x * 2) - 1  # (root * 2) - 1
    
    # Initialize the tree with root node
    tree = {'value': root, 'left': None, 'right': None}
    
    if height == 1:
        return tree
    
    # Use queue for level-order tree construction (non-recursive)
    queue = deque()
    queue.append((tree, root, 1))  # (node, parent_value, current_level)
    
    while queue:
        current_node, parent_val, level = queue.popleft()
        
        if level < height:
            # Create left child
            left_value = left_leaf(parent_val)
            current_node['left'] = {'value': left_value, 'left': None, 'right': None}
            queue.append((current_node['left'], left_value, level + 1))
            
            # Create right child
            right_value = right_leaf(parent_val)
            current_node['right'] = {'value': right_value, 'left': None, 'right': None}
            queue.append((current_node['right'], right_value, level + 1))
    
    return tree


def gen_bin_tree_deque(
    height: int = 4,
    root: int = 12,
    left_leaf: Optional[Callable[[int], int]] = None,
    right_leaf: Optional[Callable[[int], int]] = None
) -> deque:
    """
    Generate a binary tree using collections.deque for storage.
    
    This implementation uses deque for efficient level-order traversal
    and storage of tree nodes.
    
    Args:
        height: The height of the tree (default: 4)
        root: The value of the root node (default: 12)
        left_leaf: Function to calculate left child value (default: root ^ 3)
        right_leaf: Function to calculate right child value (default: (root * 2) - 1)
    
    Returns:
        A deque containing tree nodes in level-order.
    """
    if height < 1:
        raise ValueError("Height must be at least 1")
    
    if left_leaf is None:
        left_leaf = lambda x: x ** 3
        
    if right_leaf is None:
        right_leaf = lambda x: (x * 2) - 1
    
    tree_deque = deque()
    tree_dict = gen_bin_tree(height, root, left_leaf, right_leaf)
    
    # Convert dictionary tree to deque using level-order traversal
    queue = deque([tree_dict])
    while queue:
        node = queue.popleft()
        if node:
            tree_deque.append(node['value'])
            queue.append(node.get('left'))
            queue.append(node.get('right'))
        else:
            tree_deque.append(None)
    
    return tree_deque


def gen_bin_tree_namedtuple(
    height: int = 4,
    root: int = 12,
    left_leaf: Optional[Callable[[int], int]] = None,
    right_leaf: Optional[Callable[[int], int]] = None
) -> Optional[TreeNode]:
    """
    Generate a binary tree using collections.namedtuple for node representation.
    
    This implementation uses namedtuple for more readable and structured
    node representation.
    
    Args:
        height: The height of the tree (default: 4)
        root: The value of the root node (default: 12)
        left_leaf: Function to calculate left child value (default: root ^ 3)
        right_leaf: Function to calculate right child value (default: (root * 2) - 1)
    
    Returns:
        A TreeNode namedtuple representing the tree structure.
    """
    if height < 1:
        raise ValueError("Height must be at least 1")
    
    if left_leaf is None:
        left_leaf = lambda x: x ** 3
        
    if right_leaf is None:
        right_leaf = lambda x: (x * 2) - 1
    
    def _build_namedtree(current_height: int, current_root: int) -> Optional[TreeNode]:
        """Helper function to build tree using namedtuple recursively."""
        if current_height > height:
            return None
            
        left_child = _build_namedtree(current_height + 1, left_leaf(current_root))
        right_child = _build_namedtree(current_height + 1, right_leaf(current_root))
        
        return TreeNode(value=current_root, left=left_child, right=right_child)
    
    return _build_namedtree(1, root)


def print_tree_structure(tree: Union[Dict, TreeNode], level: int = 0) -> None:
    """
    Print the tree structure in a readable format.
    
    Args:
        tree: The tree to print (dict or TreeNode)
        level: Current level for indentation (used internally)
    """
    if tree is None:
        return
        
    if isinstance(tree, dict):
        value = tree['value']
        left = tree.get('left')
        right = tree.get('right')
    else:  # TreeNode
        value = tree.value
        left = tree.left
        right = tree.right
    
    indent = "  " * level
    print(f"{indent}{value}")
    
    if left:
        print(f"{indent}L:", end="")
        print_tree_structure(left, level + 1)
    
    if right:
        print(f"{indent}R:", end="")
        print_tree_structure(right, level + 1)


if __name__ == "__main__":
    # Example usage
    print("Default tree (dict representation):")
    tree1 = gen_bin_tree()
    print_tree_structure(tree1)
    
    print("\nTree with deque storage:")
    tree2 = gen_bin_tree_deque(height=3)
    print(f"Level-order: {list(tree2)}")
    
    print("\nTree with namedtuple representation:")
    tree3 = gen_bin_tree_namedtuple(height=3)
    print_tree_structure(tree3)
