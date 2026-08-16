---
problems:
  - title: 下一个更大元素 I
    url: https://leetcode.cn/problems/next-greater-element-i/
    difficulty: easy
  - title: 柱状图中最大的矩形
    url: https://leetcode.cn/problems/largest-rectangle-in-histogram/
    difficulty: hard
  - title: 接雨水
    url: https://leetcode.cn/problems/trapping-rain-water/
    difficulty: hard
  - title: 滑动窗口最大值
    url: https://leetcode.cn/problems/sliding-window-maximum/
    difficulty: hard
---

# 优化算法

优化算法是提高程序效率的重要工具，包括贪心算法、双指针、滑动窗口和单调栈等。本章节将介绍这些优化算法的原理和应用。

## 贪心算法

### 基本概念

贪心算法是一种在每一步选择中都采取在当前状态下最好或最优的选择，从而希望导致结果是全局最好或最优的算法。

### 应用场景

- 活动选择问题
- 霍夫曼编码
- 最小生成树算法（Kruskal、Prim）
- 单源最短路径算法（Dijkstra）

### 代码示例

```python
def can_jump(nums):
    """
    跳跃游戏
    :param nums: 非负整数数组
    :return: 是否能够到达最后一个位置
    """
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
        if max_reach >= len(nums) - 1:
            return True
    return False
```

## 双指针

### 基本概念

双指针是一种使用两个指针来遍历数组或链表的技术，通常用于优化时间复杂度。

### 应用场景

- 两数之和
- 反转数组
- 寻找中间节点
- 判断链表是否有环

### 代码示例

```python
def two_sum(nums, target):
    """
    两数之和 II - 输入有序数组
    :param nums: 有序整数数组
    :param target: 目标值
    :return: 和为目标值的两个整数的下标
    """
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left + 1, right + 1]  # 题目要求返回从1开始的索引
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

## 滑动窗口

### 基本概念

滑动窗口是一种在数组或字符串上维护一个可变大小的窗口的技术，用于解决子数组或子字符串的问题。

### 应用场景

- 最长无重复子串
- 最小覆盖子串
- 滑动窗口最大值

### 代码示例

```python
def length_of_longest_substring(s):
    """
    最长无重复子串
    :param s: 字符串
    :return: 最长无重复子串的长度
    """
    char_set = set()
    left = 0
    max_length = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    return max_length
```

## 单调栈

### 基本概念

单调栈是一种特殊的栈，栈中的元素保持单调递增或单调递减的顺序。

### 应用场景

- 下一个更大元素
- 柱状图中最大的矩形
- 接雨水

### 代码示例

```python
def next_greater_element(nums):
    """
    下一个更大元素 I
    :param nums: 整数数组
    :return: 每个元素的下一个更大元素
    """
    result = [-1] * len(nums)
    stack = []
    for i in range(len(nums)):
        while stack and nums[i] > nums[stack[-1]]:
            index = stack.pop()
            result[index] = nums[i]
        stack.append(i)
    return result
```

## 总结

优化算法是提高程序效率的重要工具，不同的优化算法有不同的特点和适用场景：

- **贪心算法**：在每一步选择中都采取最优选择，适用于具有贪心选择性质的问题
- **双指针**：使用两个指针遍历数组或链表，适用于有序数组、链表等问题
- **滑动窗口**：维护一个可变大小的窗口，适用于子数组或子字符串问题
- **单调栈**：保持栈中元素的单调性，适用于寻找下一个更大元素等问题

在实际应用中，应根据具体问题的特点，选择合适的优化算法，以提高程序的效率。