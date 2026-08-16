---
problems:
  - title: 两数之和
    url: https://leetcode.cn/problems/two-sum/
    difficulty: easy
  - title: 三数之和
    url: https://leetcode.cn/problems/3sum/
    difficulty: medium
---

# 时空复杂度分析深度指南

## 什么是复杂度分析

复杂度分析是评估算法性能的重要方法，它帮助我们：

1. **预测算法在不同输入规模下的表现**
2. **比较不同算法的效率**
3. **优化算法性能**
4. **在面试中展示专业能力**

## 时间复杂度

### 基本概念

时间复杂度表示算法执行时间随输入规模增长的变化趋势，通常用大O符号（O-notation）表示。

### 常见时间复杂度

| 复杂度 | 名称 | 描述 | 示例 |
|--------|------|------|------|
| O(1) | 常数时间 | 执行时间与输入规模无关 | 数组访问、哈希表查找 |
| O(log n) | 对数时间 | 执行时间与输入规模的对数成正比 | 二分查找 |
| O(n) | 线性时间 | 执行时间与输入规模成正比 | 线性搜索 |
| O(n log n) | 线性对数时间 | 执行时间与输入规模乘以其对数成正比 | 快速排序、归并排序 |
| O(n²) | 平方时间 | 执行时间与输入规模的平方成正比 | 冒泡排序、插入排序 |
| O(2ⁿ) | 指数时间 | 执行时间与2的输入规模次方成正比 | 斐波那契递归 |
| O(n!) | 阶乘时间 | 执行时间与输入规模的阶乘成正比 | 旅行商问题的暴力解法 |

### 时间复杂度分析方法

#### 1. 基本操作计数

识别算法中的基本操作（如赋值、比较、算术运算等），计算其执行次数。

**示例**：
```python
def sum_array(arr):
    total = 0  # 1次
    for num in arr:  # n次
        total += num  # n次
    return total  # 1次
```

总操作数：1 + n + n + 1 = 2n + 2，时间复杂度为 O(n)。

#### 2. 循环分析

- **单层循环**：时间复杂度为 O(n)
- **嵌套循环**：时间复杂度为 O(n²)、O(n³)等
- **二分查找**：时间复杂度为 O(log n)

**示例**：
```python
def nested_loop(n):
    for i in range(n):  # n次
        for j in range(n):  # n次
            print(i, j)  # n²次
```

时间复杂度为 O(n²)。

#### 3. 递归分析

使用递归树或主定理来分析递归算法的时间复杂度。

**示例**：
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

递归树的高度为 n，每个节点有两个子节点，时间复杂度为 O(2ⁿ)。

### 时间复杂度计算技巧

1. **忽略常数项**：O(2n + 3) = O(n)
2. **忽略低阶项**：O(n² + n) = O(n²)
3. **乘法法则**：嵌套循环，O(n) * O(m) = O(nm)
4. **加法法则**：顺序执行，O(n) + O(m) = O(max(n, m))

## 空间复杂度

### 基本概念

空间复杂度表示算法所需的额外空间随输入规模增长的变化趋势。

### 常见空间复杂度

| 复杂度 | 名称 | 描述 | 示例 |
|--------|------|------|------|
| O(1) | 常数空间 | 所需空间与输入规模无关 | 原地排序算法 |
| O(log n) | 对数空间 | 所需空间与输入规模的对数成正比 | 递归二分查找 |
| O(n) | 线性空间 | 所需空间与输入规模成正比 | 线性数据结构 |
| O(n²) | 平方空间 | 所需空间与输入规模的平方成正比 | 二维数组 |

### 空间复杂度分析方法

#### 1. 额外空间分析

计算算法除输入和输出外使用的额外空间。

**示例**：
```python
def reverse_array(arr):
    reversed_arr = []  # 额外空间 O(n)
    for i in range(len(arr)-1, -1, -1):
        reversed_arr.append(arr[i])
    return reversed_arr
```

空间复杂度为 O(n)。

#### 2. 原地算法

不使用额外空间或仅使用常数额外空间的算法。

**示例**：
```python
def reverse_array_in_place(arr):
    left, right = 0, len(arr)-1  # 额外空间 O(1)
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr
```

空间复杂度为 O(1)。

#### 3. 递归空间

递归算法的空间复杂度包括递归调用栈的空间。

**示例**：
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
```

递归深度为 n，空间复杂度为 O(n)。

## 实战分析示例

### 示例1：两数之和

**代码**：
```python
def twoSum(nums, target):
    hash_map = {}  # 额外空间 O(n)
    for i, num in enumerate(nums):  # 时间 O(n)
        complement = target - num
        if complement in hash_map:  # 时间 O(1)
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
```

**时间复杂度**：O(n)，其中 n 是数组长度
**空间复杂度**：O(n)，用于存储哈希表

### 示例2：三数之和

**代码**：
```python
def threeSum(nums):
    nums.sort()  # 时间 O(n log n)
    result = []
    for i in range(len(nums)):  # 时间 O(n)
        if i > 0 and nums[i] == nums[i-1]:
            continue
        left, right = i+1, len(nums)-1
        while left < right:  # 时间 O(n)
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
    return result
```

**时间复杂度**：O(n²)，其中 n 是数组长度
**空间复杂度**：O(1)（不考虑输出空间）

### 示例3：二叉树遍历

**代码**：
```python
def dfs(root):
    if not root:
        return
    print(root.val)
    dfs(root.left)
    dfs(root.right)
```

**时间复杂度**：O(n)，其中 n 是树的节点数
**空间复杂度**：O(h)，其中 h 是树的高度，最坏情况下为 O(n)

## 复杂度优化策略

### 时间复杂度优化

1. **使用更高效的数据结构**：如哈希表、堆等
2. **减少不必要的计算**：如剪枝、缓存中间结果
3. **优化算法策略**：如从暴力解法到动态规划

### 空间复杂度优化

1. **使用原地算法**：避免额外空间
2. **复用空间**：如使用现有数据结构存储中间结果
3. **权衡时间和空间**：根据实际需求选择合适的算法

## 常见误区

1. **忽略常数因子**：在实际应用中，常数因子可能影响性能
2. **只关注最坏情况**：平均情况和最好情况也很重要
3. **混淆时间和空间**：需要根据实际需求平衡两者
4. **忽略输入规模**：不同输入规模可能需要不同的算法

## 面试中的复杂度分析

在面试中，你应该：

1. **主动分析复杂度**：在讲解算法时主动分析时间和空间复杂度
2. **解释分析过程**：展示你的分析思路，而不仅仅是结果
3. **考虑优化空间**：讨论可能的优化方向
4. **结合实际场景**：根据具体应用场景选择合适的算法

## 总结

复杂度分析是算法学习的重要组成部分，掌握它可以帮助你：

1. 设计更高效的算法
2. 在面试中展示专业能力
3. 理解算法的性能瓶颈
4. 做出合理的技术决策

通过不断练习和分析，你将逐渐掌握复杂度分析的技巧，成为一名优秀的算法工程师。