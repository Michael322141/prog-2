import unittest

def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

class TestTwoSum(unittest.TestCase):
    def test_example1(self):
        nums = [2, 7, 11, 15]
        target = 9
        result = two_sum(nums, target)
        self.assertEqual(sorted(result), [0, 1])
    
    def test_example2(self):
        nums = [3, 2, 4]
        target = 6
        result = two_sum(nums, target)
        self.assertEqual(sorted(result), [1, 2])
    
    def test_example3(self):
        nums = [3, 3]
        target = 6
        result = two_sum(nums, target)
        self.assertEqual(sorted(result), [0, 1])
    
    def test_no_solution(self):
        nums = [1, 2, 3]
        target = 7
        result = two_sum(nums, target)
        self.assertEqual(result, [])
    
    def test_negative_numbers(self):
        nums = [-1, -2, -3, -4]
        target = -7
        result = two_sum(nums, target)
        self.assertEqual(sorted(result), [2, 3])

if __name__ == '__main__':
    unittest.main()
