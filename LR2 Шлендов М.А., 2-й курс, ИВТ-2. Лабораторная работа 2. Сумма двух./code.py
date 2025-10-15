#Шлендов М.А., 2-й курс, ИВТ-2. Лабораторная работа 2. Сумма двух.
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

if __name__ == "__main__":
    # Test 1
    nums1 = [1, 2, 5, 7]
    target1 = 3
    print(f"Input: nums = {nums1}, target = {target1}")
    print(f"Output: {two_sum(nums1, target1)}")
    print()
