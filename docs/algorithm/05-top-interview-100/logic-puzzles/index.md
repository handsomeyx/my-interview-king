---
problems:
  - title: 二进制中 1 的个数
    url: https://leetcode.cn/problems/number-of-1-bits/
    difficulty: easy
  - title: 丑数
    url: https://leetcode.cn/problems/ugly-number/
    difficulty: easy
  - title: 阶乘后的零
    url: https://leetcode.cn/problems/factorial-trailing-zeroes/
    difficulty: medium
  - title: 找不同
    url: https://leetcode.cn/problems/find-the-difference/
    difficulty: easy
  - title: 有效的括号
    url: https://leetcode.cn/problems/valid-parentheses/
    difficulty: easy
  - title: 回文数
    url: https://leetcode.cn/problems/palindrome-number/
    difficulty: easy
  - title: 斐波那契数列
    url: https://leetcode.cn/problems/fibonacci-number/
    difficulty: easy
  - title: 最大子数组和
    url: https://leetcode.cn/problems/maximum-subarray/
    difficulty: medium
  - title: 买卖股票的最佳时机
    url: https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/
    difficulty: easy
---

# 智力题与逻辑推演

智力题和逻辑推演是面试中常见的题型，主要考察候选人的逻辑思维能力和问题解决能力。本文将介绍一些常见的智力题和逻辑推演问题。

## 1. 两数交换

### 题目描述

不使用临时变量，交换两个整数的值。

### 示例

```
输入：a = 5, b = 10
输出：a = 10, b = 5
```

### 解题思路

- **位运算**：使用异或操作交换两个数的值
- **算术运算**：使用加减法交换两个数的值

### 代码实现

```python
def swap_with_xor(a, b):
    """
    使用异或操作交换两个数的值
    :param a: 第一个整数
    :param b: 第二个整数
    :return: 交换后的两个整数
    """
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b

def swap_with_arithmetic(a, b):
    """
    使用算术运算交换两个数的值
    :param a: 第一个整数
    :param b: 第二个整数
    :return: 交换后的两个整数
    """
    a = a + b
    b = a - b
    a = a - b
    return a, b

# 测试示例
print(swap_with_xor(5, 10))  # 输出: (10, 5)
print(swap_with_arithmetic(5, 10))  # 输出: (10, 5)
```

## 2. 斐波那契数列

### 题目描述

计算斐波那契数列的第 n 项。

### 示例

```
输入：n = 5
输出：5
解释：斐波那契数列前 6 项为：0, 1, 1, 2, 3, 5
```

### 解题思路

- **递归**：使用递归计算，时间复杂度 O(2^n)
- **动态规划**：使用动态规划计算，时间复杂度 O(n)
- **矩阵快速幂**：使用矩阵快速幂计算，时间复杂度 O(log n)

### 代码实现

```python
def fibonacci_recursive(n):
    """
    使用递归计算斐波那契数列的第 n 项
    :param n: 项数
    :return: 第 n 项的值
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_dp(n):
    """
    使用动态规划计算斐波那契数列的第 n 项
    :param n: 项数
    :return: 第 n 项的值
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

def fibonacci_matrix(n):
    """
    使用矩阵快速幂计算斐波那契数列的第 n 项
    :param n: 项数
    :return: 第 n 项的值
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    def multiply(a, b):
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
        ]
    
    def matrix_pow(matrix, power):
        result = [[1, 0], [0, 1]]  # 单位矩阵
        while power > 0:
            if power % 2 == 1:
                result = multiply(result, matrix)
            matrix = multiply(matrix, matrix)
            power //= 2
        return result
    
    # 斐波那契矩阵
    fib_matrix = [[1, 1], [1, 0]]
    # 计算矩阵的 n-1 次幂
    result_matrix = matrix_pow(fib_matrix, n-1)
    # 结果就是矩阵的 [0][0] 元素
    return result_matrix[0][0]

# 测试示例
print(fibonacci_recursive(5))  # 输出: 5
print(fibonacci_dp(5))  # 输出: 5
print(fibonacci_matrix(5))  # 输出: 5
```

## 3. 二进制中 1 的个数

### 题目描述

输入一个整数，输出该数二进制表示中 1 的个数。

### 示例

```
输入：n = 9
输出：2
解释：9 的二进制表示为 1001，其中有 2 个 1。
```

### 解题思路

- **位运算**：使用位运算统计 1 的个数
- **内置函数**：使用 Python 的内置函数 bin() 和 count() 统计 1 的个数

### 代码实现

```python
def count_ones(n):
    """
    统计整数二进制表示中 1 的个数
    :param n: 整数
    :return: 二进制表示中 1 的个数
    """
    count = 0
    while n:
        n &= n - 1  # 清除最低位的 1
        count += 1
    return count

def count_ones_builtin(n):
    """
    使用内置函数统计整数二进制表示中 1 的个数
    :param n: 整数
    :return: 二进制表示中 1 的个数
    """
    return bin(n).count('1')

# 测试示例
print(count_ones(9))  # 输出: 2
print(count_ones_builtin(9))  # 输出: 2
```

## 4. 丑数

### 题目描述

编写一个程序判断给定的数是否是丑数。丑数就是只包含质因数 2, 3, 5 的正整数。

### 示例

```
输入：6
输出：True
解释：6 = 2 × 3

输入：8
输出：True
解释：8 = 2 × 2 × 2

输入：14
输出：False
解释：14 包含质因数 7，不是丑数。
```

### 解题思路

- **循环除法**：将数不断除以 2, 3, 5，最后判断是否等于 1

### 代码实现

```python
def is_ugly(num):
    """
    判断给定的数是否是丑数
    :param num: 整数
    :return: 是否是丑数
    """
    if num <= 0:
        return False
    
    for factor in [2, 3, 5]:
        while num % factor == 0:
            num //= factor
    
    return num == 1

# 测试示例
print(is_ugly(6))  # 输出: True
print(is_ugly(8))  # 输出: True
print(is_ugly(14))  # 输出: False
```

## 5. 阶乘后的零

### 题目描述

给定一个整数 n，返回 n! 结果中尾随零的数量。

### 示例

```
输入：3
输出：0
解释：3! = 6，没有尾随零。

输入：5
输出：1
解释：5! = 120，有一个尾随零。

输入：10
输出：2
解释：10! = 3628800，有两个尾随零。
```

### 解题思路

- **因子分解**：尾随零的数量等于 n! 中 5 的因子个数

### 代码实现

```python
def trailing_zeroes(n):
    """
    返回 n! 结果中尾随零的数量
    :param n: 整数
    :return: 尾随零的数量
    """
    count = 0
    while n > 0:
        n //= 5
        count += n
    return count

# 测试示例
print(trailing_zeroes(3))  # 输出: 0
print(trailing_zeroes(5))  # 输出: 1
print(trailing_zeroes(10))  # 输出: 2
```

## 6. 回文数

### 题目描述

判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。

### 示例

```
输入：121
输出：True

输入：-121
输出：False
解释：从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。

输入：10
输出：False
解释：从右向左读, 为 01 。因此它不是一个回文数。
```

### 解题思路

- **字符串转换**：将整数转换为字符串，然后判断是否是回文
- **数学方法**：通过数学运算反转整数，然后比较是否相等

### 代码实现

```python
def is_palindrome_str(x):
    """
    使用字符串转换判断是否是回文数
    :param x: 整数
    :return: 是否是回文数
    """
    if x < 0:
        return False
    return str(x) == str(x)[::-1]

def is_palindrome_math(x):
    """
    使用数学方法判断是否是回文数
    :param x: 整数
    :return: 是否是回文数
    """
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    
    reversed_num = 0
    while x > reversed_num:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    
    return x == reversed_num or x == reversed_num // 10

# 测试示例
print(is_palindrome_str(121))  # 输出: True
print(is_palindrome_str(-121))  # 输出: False
print(is_palindrome_str(10))  # 输出: False

print(is_palindrome_math(121))  # 输出: True
print(is_palindrome_math(-121))  # 输出: False
print(is_palindrome_math(10))  # 输出: False
```

## 7. 找不同

### 题目描述

给定两个字符串 s 和 t，它们只包含小写字母。字符串 t 由字符串 s 随机重排，然后在随机位置添加一个字母。请找出在 t 中被添加的字母。

### 示例

```
输入：s = "abcd", t = "abcde"
输出："e"
解释：'e' 是那个被添加的字母。
```

### 解题思路

- **异或运算**：使用异或运算找到不同的字符
- **计数**：统计每个字符的出现次数，找到次数不同的字符

### 代码实现

```python
def find_the_difference_xor(s, t):
    """
    使用异或运算找到在 t 中被添加的字母
    :param s: 字符串 s
    :param t: 字符串 t
    :return: 被添加的字母
    """
    result = 0
    for c in s + t:
        result ^= ord(c)
    return chr(result)

def find_the_difference_count(s, t):
    """
    使用计数找到在 t 中被添加的字母
    :param s: 字符串 s
    :param t: 字符串 t
    :return: 被添加的字母
    """
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    for c in t:
        count[ord(c) - ord('a')] -= 1
        if count[ord(c) - ord('a')] < 0:
            return c
    return ''

# 测试示例
print(find_the_difference_xor("abcd", "abcde"))  # 输出: "e"
print(find_the_difference_count("abcd", "abcde"))  # 输出: "e"
```

## 8. 有效的括号

### 题目描述

给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。

有效字符串需满足：
1. 左括号必须用相同类型的右括号闭合。
2. 左括号必须以正确的顺序闭合。

### 示例

```
输入："()"
输出：True

输入："()[]{}"
输出：True

输入："(]"
输出：False

输入："([)]"
输出：False

输入："{[]}"
输出：True
```

### 解题思路

- **栈**：使用栈来匹配括号

### 代码实现

```python
def is_valid(s):
    """
    判断字符串是否有效
    :param s: 字符串
    :return: 是否有效
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            # 右括号
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            # 左括号
            stack.append(char)
    
    return not stack

# 测试示例
print(is_valid("()"))  # 输出: True
print(is_valid("()[]{}"))  # 输出: True
print(is_valid("(]"))  # 输出: False
print(is_valid("([)]"))  # 输出: False
print(is_valid("{[]}"))  # 输出: True
```

## 9. 最大子序和

### 题目描述

给定一个整数数组 nums，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

### 示例

```
输入：[-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6。
```

### 解题思路

- **动态规划**：使用动态规划计算最大子序和
- **分治法**：使用分治法计算最大子序和

### 代码实现

```python
def max_sub_array_dp(nums):
    """
    使用动态规划计算最大子序和
    :param nums: 整数数组
    :return: 最大子序和
    """
    if not nums:
        return 0
    
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum

def max_sub_array_divide(nums):
    """
    使用分治法计算最大子序和
    :param nums: 整数数组
    :return: 最大子序和
    """
    def divide_conquer(nums, left, right):
        if left == right:
            return nums[left]
        
        mid = (left + right) // 2
        # 左子数组的最大和
        left_max = divide_conquer(nums, left, mid)
        # 右子数组的最大和
        right_max = divide_conquer(nums, mid + 1, right)
        # 跨中间的最大和
        cross_max = 0
        left_cross = float('-inf')
        right_cross = float('-inf')
        
        # 计算左侧跨中间的最大和
        temp = 0
        for i in range(mid, left - 1, -1):
            temp += nums[i]
            left_cross = max(left_cross, temp)
        
        # 计算右侧跨中间的最大和
        temp = 0
        for i in range(mid + 1, right + 1):
            temp += nums[i]
            right_cross = max(right_cross, temp)
        
        cross_max = left_cross + right_cross
        
        return max(left_max, right_max, cross_max)
    
    if not nums:
        return 0
    
    return divide_conquer(nums, 0, len(nums) - 1)

# 测试示例
print(max_sub_array_dp([-2,1,-3,4,-1,2,1,-5,4]))  # 输出: 6
print(max_sub_array_divide([-2,1,-3,4,-1,2,1,-5,4]))  # 输出: 6
```

## 10. 买卖股票的最佳时机

### 题目描述

给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。

如果你最多只允许完成一笔交易（即买入和卖出一支股票一次），设计一个算法来计算你所能获取的最大利润。

### 示例

```
输入：[7,1,5,3,6,4]
输出：5
解释：在第 2 天（价格 = 1）的时候买入，在第 5 天（价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。
```

### 解题思路

- **一次遍历**：遍历数组，记录当前的最小价格和最大利润

### 代码实现

```python
def max_profit(prices):
    """
    计算买卖股票的最佳时机
    :param prices: 股票价格数组
    :return: 最大利润
    """
    if not prices:
        return 0
    
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        current_profit = price - min_price
        max_profit = max(max_profit, current_profit)
    
    return max_profit

# 测试示例
print(max_profit([7,1,5,3,6,4]))  # 输出: 5
print(max_profit([7,6,4,3,1]))  # 输出: 0
```

## 总结

智力题和逻辑推演是面试中常见的题型，主要考察候选人的逻辑思维能力和问题解决能力。本文介绍了一些常见的智力题和逻辑推演问题，包括：

1. **基本操作**：两数交换、斐波那契数列
2. **位运算**：二进制中 1 的个数、找不同
3. **数学问题**：丑数、阶乘后的零、回文数
4. **栈**：有效的括号
5. **动态规划**：最大子序和
6. **贪心算法**：买卖股票的最佳时机

这些题目涵盖了智力题和逻辑推演的常见类型，掌握这些题目对于应对面试中的智力题和逻辑推演问题非常有帮助。