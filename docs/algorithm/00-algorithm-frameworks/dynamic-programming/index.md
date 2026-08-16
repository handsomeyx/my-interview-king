---
problems:
  - title: 爬楼梯
    url: https://leetcode.cn/problems/climbing-stairs/
    difficulty: easy
  - title: 最大子数组和
    url: https://leetcode.cn/problems/maximum-subarray/
    difficulty: medium
  - title: 分割等和子集（0-1 背包）
    url: https://leetcode.cn/problems/partition-equal-subset-sum/
    difficulty: medium
  - title: 最长公共子序列
    url: https://leetcode.cn/problems/longest-common-subsequence/
    difficulty: medium
  - title: 编辑距离
    url: https://leetcode.cn/problems/edit-distance/
    difficulty: medium
  - title: 最长回文子串
    url: https://leetcode.cn/problems/longest-palindromic-substring/
    difficulty: medium
---

# 动态规划框架

## 思考锚点

动态规划的核心思想可以用一句话概括：**把大问题拆成子问题，子问题的最优解包含在大问题的最优解中**。这就是「最优子结构」。

但真正让 DP 变得困难的不是这个概念，而是两个实际问题：
1. **怎么定义状态**？状态定义错了，后面全白搭。比如爬楼梯题用 `dp[i]` 表示到第 i 阶的方法数，这是自然的定义。但更复杂的题（比如区间 DP、状态压缩 DP），状态定义就需要经验。
2. **怎么找状态转移**？这是从一个状态到另一个状态的「桥梁」。转移方程不是凭空想出来的，而是基于问题的决策过程——每个状态有哪些选择，每种选择会把你带到哪个新状态。

学习 DP 的正确姿势：**先理解问题的决策过程，再把决策翻译成状态转移方程**。

## 算法原理

动态规划（Dynamic Programming，DP）是一种用于解决具有重叠子问题和最优子结构的问题的算法方法。它通过将原问题分解为子问题，先求解子问题，然后从这些子问题的解得到原问题的解。

## 框架模板

```java
public int dynamicProgramming(int[] nums) {
    // 1. 定义状态
    int n = nums.length;
    int[] dp = new int[n];
    
    // 2. 初始化状态
    dp[0] = nums[0];
    
    // 3. 状态转移
    for (int i = 1; i < n; i++) {
        dp[i] = Math.max(dp[i-1] + nums[i], nums[i]);
    }
    
    // 4. 计算结果
    int result = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        result = Math.max(result, dp[i]);
    }
    
    return result;
}
```

## 适用场景

1. **最优子结构**：问题的最优解包含其子问题的最优解
2. **重叠子问题**：不同的子问题包含相同的子子问题
3. **无后效性**：子问题的解一旦确定，就不再改变

常见的动态规划问题包括：
- **一维DP**：如最大子数组和、爬楼梯
- **二维DP**：如最长公共子序列、编辑距离
- **背包问题**：0-1背包、完全背包
- **区间DP**：如最长回文子串
- **状态压缩DP**：如旅行商问题

## 注意事项

1. **状态定义**：正确定义状态是动态规划的关键，状态应该能够描述问题的当前状态
2. **状态转移**：找到状态之间的转移关系，这是动态规划的核心
3. **初始条件**：正确初始化状态，确保边界情况的处理
4. **空间优化**：对于某些问题，可以使用滚动数组等方法优化空间复杂度

## 示例：爬楼梯

### 题目描述

假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶？

### 代码实现

```java
public int climbStairs(int n) {
    if (n <= 2) {
        return n;
    }
    
    // 定义状态：dp[i] 表示爬到第 i 阶的方法数
    int[] dp = new int[n + 1];
    
    // 初始化状态
    dp[1] = 1;
    dp[2] = 2;
    
    // 状态转移
    for (int i = 3; i <= n; i++) {
        // 爬到第 i 阶的方法数 = 爬到第 i-1 阶的方法数 + 爬到第 i-2 阶的方法数
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    return dp[n];
}
```

### 解释

1. **状态定义**：`dp[i]` 表示爬到第 i 阶的方法数
2. **初始条件**：
   - 爬到第 1 阶有 1 种方法
   - 爬到第 2 阶有 2 种方法
3. **状态转移**：爬到第 i 阶的方法数等于爬到第 i-1 阶的方法数（再爬 1 阶）加上爬到第 i-2 阶的方法数（再爬 2 阶）
4. **返回结果**：返回 `dp[n]`，即爬到第 n 阶的方法数

## 示例：最大子数组和

### 题目描述

给定一个整数数组 `nums`，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

### 代码实现

```java
public int maxSubArray(int[] nums) {
    int n = nums.length;
    if (n == 0) {
        return 0;
    }
    
    // 定义状态：dp[i] 表示以 nums[i] 结尾的最大子数组和
    int[] dp = new int[n];
    
    // 初始化状态
    dp[0] = nums[0];
    
    // 状态转移
    for (int i = 1; i < n; i++) {
        // 选择：要么将当前元素加入前面的子数组，要么以当前元素开始新的子数组
        dp[i] = Math.max(dp[i-1] + nums[i], nums[i]);
    }
    
    // 计算结果
    int maxSum = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        maxSum = Math.max(maxSum, dp[i]);
    }
    
    return maxSum;
}
```

### 解释

1. **状态定义**：`dp[i]` 表示以 `nums[i]` 结尾的最大子数组和
2. **初始条件**：`dp[0] = nums[0]`，因为以第一个元素结尾的最大子数组和就是它本身
3. **状态转移**：对于每个元素，有两种选择：
   - 将当前元素加入前面的子数组
   - 以当前元素开始新的子数组
   取这两种选择中的较大值作为 `dp[i]`
4. **返回结果**：遍历 `dp` 数组，找到最大的值，即为最大子数组和

## 示例：0-1背包问题

### 题目描述

给定一个容量为 `capacity` 的背包和 `n` 个物品，每个物品有重量 `weight[i]` 和价值 `value[i]`，选择一些物品放入背包，使得总重量不超过容量，且总价值最大。

### 代码实现

```java
public int knapsack(int capacity, int[] weight, int[] value) {
    int n = weight.length;
    
    // 定义状态：dp[i][j] 表示前 i 个物品，容量为 j 时的最大价值
    int[][] dp = new int[n + 1][capacity + 1];
    
    // 状态转移
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= capacity; j++) {
            if (j >= weight[i-1]) {
                // 可以选择放入第 i 个物品
                dp[i][j] = Math.max(dp[i-1][j], dp[i-1][j - weight[i-1]] + value[i-1]);
            } else {
                // 不能放入第 i 个物品
                dp[i][j] = dp[i-1][j];
            }
        }
    }
    
    return dp[n][capacity];
}
```

### 解释

1. **状态定义**：`dp[i][j]` 表示前 i 个物品，容量为 j 时的最大价值
2. **状态转移**：
   - 如果当前物品的重量不超过背包容量，则可以选择放入或不放入该物品
   - 如果放入，则价值为前 i-1 个物品在容量 j - weight[i-1] 时的最大价值加上当前物品的价值
   - 如果不放入，则价值为前 i-1 个物品在容量 j 时的最大价值
   - 取这两种选择中的较大值作为 `dp[i][j]`
3. **返回结果**：返回 `dp[n][capacity]`，即所有物品都考虑后，容量为 capacity 时的最大价值

## 总结

动态规划是一种强大的算法方法，适用于解决具有重叠子问题和最优子结构的问题。通过掌握动态规划的框架，你可以解决许多复杂的算法问题。在实际应用中，需要注意正确定义状态、找到状态转移关系、处理初始条件，并根据需要进行空间优化。

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：动态规划的核心思想是什么？两个关键特征（最优子结构 + 重叠子问题）分别是什么意思？

2. **讲给初学者听**：怎么用「爬楼梯」来类比 DP 的状态和状态转移？为什么 `dp[i] = dp[i-1] + dp[i-2]` 是对的？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如为什么有些 DP 题用二维数组，有些用一维滚动数组？状态压缩 DP 的本质是什么？）