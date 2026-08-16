---
problems:
  - title: 斐波那契数列
    url: https://leetcode.cn/problems/fibonacci-number/
    difficulty: easy
  - title: 最长递增子序列
    url: https://leetcode.cn/problems/longest-increasing-subsequence/
    difficulty: medium
  - title: 最大子数组和
    url: https://leetcode.cn/problems/maximum-subarray/
    difficulty: medium
  - title: 分割等和子集（0-1 背包）
    url: https://leetcode.cn/problems/partition-equal-subset-sum/
    difficulty: medium
  - title: 最长回文子串
    url: https://leetcode.cn/problems/longest-palindromic-substring/
    difficulty: medium
  - title: 买卖股票的最佳时机
    url: https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/
    difficulty: easy
---

# 动态规划

动态规划是一种通过将原问题分解为子问题并存储子问题的解来避免重复计算的算法设计方法。本章节将介绍动态规划的基本思想和常见类型。

## 基本思想

动态规划的基本思想是：
1. **分解问题**：将原问题分解为若干个子问题
2. **定义状态**：定义状态表示子问题的解
3. **状态转移**：建立状态之间的转移关系
4. **初始状态**：确定初始状态的值
5. **计算顺序**：按照依赖关系计算状态

## 常见类型

### 1. 线性动态规划

**特点**：状态转移是线性的，通常只依赖于前一个或前几个状态。

**示例**：
- 斐波那契数列
- 最长递增子序列
- 最大子数组和

**代码示例**：最长递增子序列

```python
def length_of_lis(nums):
    """
    最长递增子序列
    :param nums: 整数数组
    :return: 最长递增子序列的长度
    """
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

### 2. 背包问题

**特点**：给定一组物品和一个背包，每个物品有重量和价值，求在背包容量限制下，能装入的最大价值。

**类型**：
- 0-1背包：每个物品只能选或不选
- 完全背包：每个物品可以选多次
- 多重背包：每个物品有有限的数量

**代码示例**：0-1背包

```python
def knapsack(weights, values, capacity):
    """
    0-1背包问题
    :param weights: 物品重量数组
    :param values: 物品价值数组
    :param capacity: 背包容量
    :return: 最大价值
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if j >= weights[i-1]:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-weights[i-1]] + values[i-1])
            else:
                dp[i][j] = dp[i-1][j]
    return dp[n][capacity]
```

### 3. 区间动态规划

**特点**：状态表示区间 [i, j] 的最优解。

**示例**：
- 最长回文子串
- 矩阵链相乘
- 石子合并

**代码示例**：最长回文子串

```python
def longest_palindrome(s):
    """
    最长回文子串
    :param s: 字符串
    :return: 最长回文子串
    """
    n = len(s)
    if n < 2:
        return s
    dp = [[False] * n for _ in range(n)]
    start, max_length = 0, 1
    # 单个字符是回文
    for i in range(n):
        dp[i][i] = True
    # 两个字符的回文
    for i in range(n-1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            start = i
            max_length = 2
    # 长度大于2的回文
    for length in range(3, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                start = i
                max_length = length
    return s[start:start+max_length]
```

### 4. 状态机动态规划

**特点**：状态之间的转移类似于状态机的状态转换。

**示例**：
- 买卖股票问题
- 打家劫舍问题
- 状态压缩动态规划

**代码示例**：买卖股票问题

```java
public class Solution {
    public int maxProfit(int[] prices) {
        """
        买卖股票的最佳时机 I
        :param prices: 股票价格数组
        :return: 最大利润
        """
        if (prices == null || prices.length == 0) {
            return 0;
        }
        int minPrice = Integer.MAX_VALUE;
        int maxProfit = 0;
        for (int price : prices) {
            minPrice = Math.min(minPrice, price);
            maxProfit = Math.max(maxProfit, price - minPrice);
        }
        return maxProfit;
    }
}
```

## 总结

动态规划是一种强大的算法设计方法，适用于解决具有重叠子问题和最优子结构的问题。常见的动态规划类型包括：

- **线性动态规划**：状态转移是线性的
- **背包问题**：选择物品以最大化价值
- **区间动态规划**：状态表示区间的最优解
- **状态机动态规划**：状态之间的转移类似于状态机

在实际应用中，应根据具体问题的特点，选择合适的动态规划类型，并设计相应的状态转移方程。