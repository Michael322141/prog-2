from typing import Union, Optional, Dict, Any
import unittest


def gen_bin_tree(height: int = 3, root: int = 1) -> Optional[Dict[str, Any]]:
    """
    Рекурсивно генерирует бинарное дерево в виде словаря.
    
    Для номера в группе 11:
    - Левый потомок: root^2 (root во второй степени)
    - Правый потомок: 2 + root^2 (2 плюс root во второй степени)
    - Высота по умолчанию: 3
    - Корень по умолчанию: 1
    
    Args:
        height (int): Высота дерева. Должна быть положительным целым числом.
        root (int): Значение корневого узла.
    
    Returns:
        Optional[Dict[str, Any]]: Словарь, представляющий бинарное дерево, 
        или None если высота <= 0.
    
    Raises:
        ValueError: Если высота отрицательная.
    
    Example:
        >>> tree = gen_bin_tree(2, 5)
        >>> print(tree)
        {
            'root': 5,
            'left': {
                'root': 25,
                'left': None,
                'right': None
            },
            'right': {
                'root': 27,
                'left': None,
                'right': None
            }
        }
    """
    if height < 0:
        raise ValueError("Высота дерева не может быть отрицательной")
    
    # Базовый случай: если высота <= 0, возвращаем None
    if height <= 0:
        return None
    
    # Вычисляем потомков согласно варианту №11
    left_child = root ** 2  # root^2
    right_child = 2 + root ** 2  # 2 + root^2
    
    # Рекурсивно строим левое и правое поддеревья
    left_subtree = gen_bin_tree(height - 1, left_child)
    right_subtree = gen_bin_tree(height - 1, right_child)
    
    # Возвращаем дерево в виде словаря
    return {
        'root': root,
        'left': left_subtree,
        'right': right_subtree
    }


class TestGenBinTree(unittest.TestCase):
    """Тесты для функции gen_bin_tree"""
    
    def test_default_parameters(self):
        """Тест с параметрами по умолчанию (высота=3, корень=1)"""
        tree = gen_bin_tree()
        
        # Проверяем структуру дерева
        self.assertEqual(tree['root'], 1)
        self.assertEqual(tree['left']['root'], 1)  # 1^2 = 1
        self.assertEqual(tree['right']['root'], 3)  # 2 + 1^2 = 3
        
        # Проверяем листья
        self.assertEqual(tree['left']['left']['root'], 1)  # 1^2 = 1
        self.assertEqual(tree['left']['right']['root'], 3)  # 2 + 1^2 = 3
        self.assertEqual(tree['right']['left']['root'], 9)  # 3^2 = 9
        self.assertEqual(tree['right']['right']['root'], 11)  # 2 + 3^2 = 11
    
    def test_custom_height_and_root(self):
        """Тест с пользовательскими параметрами"""
        tree = gen_bin_tree(height=2, root=2)
        
        expected = {
            'root': 2,
            'left': {
                'root': 4,  # 2^2 = 4
                'left': None,
                'right': None
            },
            'right': {
                'root': 6,  # 2 + 2^2 = 6
                'left': None,
                'right': None
            }
        }
        
        self.assertEqual(tree, expected)
    
    def test_height_zero(self):
        """Тест с высотой 0"""
        tree = gen_bin_tree(height=0, root=5)
        self.assertIsNone(tree)
    
    def test_height_one(self):
        """Тест с высотой 1 (только корень)"""
        tree = gen_bin_tree(height=1, root=10)
        
        expected = {
            'root': 10,
            'left': None,
            'right': None
        }
        
        self.assertEqual(tree, expected)
    
    def test_negative_height(self):
        """Тест с отрицательной высотой (должен вызывать ошибку)"""
        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1, root=5)
    
    def test_large_tree_structure(self):
        """Тест структуры большого дерева"""
        tree = gen_bin_tree(height=3, root=3)
        
        # Проверяем, что дерево имеет правильную структуру
        self.assertIsInstance(tree, dict)
        self.assertIn('root', tree)
        self.assertIn('left', tree)
        self.assertIn('right', tree)
        
        # Проверяем типы потомков
        self.assertIsInstance(tree['left'], (dict, type(None)))
        self.assertIsInstance(tree['right'], (dict, type(None)))
    
    def test_calculation_correctness(self):
        """Тест правильности вычислений потомков"""
        # Проверяем вычисления для корня = 4
        tree = gen_bin_tree(height=2, root=4)
        
        # Левый потомок: 4^2 = 16
        self.assertEqual(tree['left']['root'], 16)
        
        # Правый потомок: 2 + 4^2 = 18
        self.assertEqual(tree['right']['root'], 18)


# Альтернативные реализации с использованием других структур данных

from collections import namedtuple, deque
from dataclasses import dataclass
from typing import List, Tuple


# Реализация с использованием namedtuple
TreeNodeNamedTuple = namedtuple('TreeNode', ['root', 'left', 'right'])

def gen_bin_tree_namedtuple(height: int = 3, root: int = 1) -> Optional[TreeNodeNamedTuple]:
    """
    Генерирует бинарное дерево с использованием namedtuple.
    
    Args:
        height (int): Высота дерева.
        root (int): Значение корневого узла.
    
    Returns:
        Optional[TreeNodeNamedTuple]: Дерево в виде namedtuple.
    """
    if height <= 0:
        return None
    
    left_child = root ** 2
    right_child = 2 + root ** 2
    
    left_subtree = gen_bin_tree_namedtuple(height - 1, left_child)
    right_subtree = gen_bin_tree_namedtuple(height - 1, right_child)
    
    return TreeNodeNamedTuple(root, left_subtree, right_subtree)


# Реализация с использованием dataclass
@dataclass
class TreeNodeDataClass:
    """Узел бинарного дерева с использованием dataclass"""
    root: int
    left: Optional['TreeNodeDataClass'] = None
    right: Optional['TreeNodeDataClass'] = None

def gen_bin_tree_dataclass(height: int = 3, root: int = 1) -> Optional[TreeNodeDataClass]:
    """
    Генерирует бинарное дерево с использованием dataclass.
    
    Args:
        height (int): Высота дерева.
        root (int): Значение корневого узла.
    
    Returns:
        Optional[TreeNodeDataClass]: Дерево в виде dataclass.
    """
    if height <= 0:
        return None
    
    left_child = root ** 2
    right_child = 2 + root ** 2
    
    left_subtree = gen_bin_tree_dataclass(height - 1, left_child)
    right_subtree = gen_bin_tree_dataclass(height - 1, right_child)
    
    return TreeNodeDataClass(root, left_subtree, right_subtree)


# Реализация с использованием списков (как в некоторых алгоритмах)
def gen_bin_tree_list(height: int = 3, root: int = 1) -> Optional[List]:
    """
    Генерирует бинарное дерево в виде списка [root, left, right].
    
    Args:
        height (int): Высота дерева.
        root (int): Значение корневого узла.
    
    Returns:
        Optional[List]: Дерево в виде списка.
    """
    if height <= 0:
        return None
    
    left_child = root ** 2
    right_child = 2 + root ** 2
    
    left_subtree = gen_bin_tree_list(height - 1, left_child)
    right_subtree = gen_bin_tree_list(height - 1, right_child)
    
    return [root, left_subtree, right_subtree]


class TestAlternativeImplementations(unittest.TestCase):
    """Тесты для альтернативных реализаций"""
    
    def test_namedtuple_implementation(self):
        """Тест реализации с namedtuple"""
        tree = gen_bin_tree_namedtuple(height=2, root=2)
        
        self.assertEqual(tree.root, 2)
        self.assertEqual(tree.left.root, 4)
        self.assertEqual(tree.right.root, 6)
    
    def test_dataclass_implementation(self):
        """Тест реализации с dataclass"""
        tree = gen_bin_tree_dataclass(height=2, root=2)
        
        self.assertEqual(tree.root, 2)
        self.assertEqual(tree.left.root, 4)
        self.assertEqual(tree.right.root, 6)
    
    def test_list_implementation(self):
        """Тест реализации со списками"""
        tree = gen_bin_tree_list(height=2, root=2)
        
        self.assertEqual(tree[0], 2)  # root
        self.assertEqual(tree[1][0], 4)  # left root
        self.assertEqual(tree[2][0], 6)  # right root


def print_tree(tree: Union[Dict, TreeNodeNamedTuple, TreeNodeDataClass, List], indent: int = 0) -> None:
    """
    Красиво печатает дерево в консоль.
    
    Args:
        tree: Дерево для печати.
        indent (int): Отступ для текущего уровня.
    """
    if tree is None:
        print(" " * indent + "None")
        return
    
    # Обработка разных типов деревьев
    if isinstance(tree, dict):
        root = tree['root']
        left = tree['left']
        right = tree['right']
    elif isinstance(tree, TreeNodeNamedTuple):
        root = tree.root
        left = tree.left
        right = tree.right
    elif isinstance(tree, TreeNodeDataClass):
        root = tree.root
        left = tree.left
        right = tree.right
    elif isinstance(tree, list):
        root = tree[0]
        left = tree[1]
        right = tree[2]
    else:
        raise ValueError(f"Неизвестный тип дерева: {type(tree)}")
    
    print(" " * indent + str(root))
    
    if left is not None or right is not None:
        print_tree(left, indent + 2)
        print_tree(right, indent + 2)


if __name__ == "__main__":
    # Демонстрация работы программы
    print("=== Бинарное дерево (словарь) ===")
    tree_dict = gen_bin_tree()
    print_tree(tree_dict)
    
    print("\n=== Бинарное дерево (namedtuple) ===")
    tree_namedtuple = gen_bin_tree_namedtuple()
    print_tree(tree_namedtuple)
    
    print("\n=== Бинарное дерево (dataclass) ===")
    tree_dataclass = gen_bin_tree_dataclass()
    print_tree(tree_dataclass)
    
    print("\n=== Бинарное дерево (список) ===")
    tree_list = gen_bin_tree_list()
    print_tree(tree_list)
    
    # Запуск тестов
    print("\n=== Запуск тестов ===")
    unittest.main(argv=[''], verbosity=2, exit=False)