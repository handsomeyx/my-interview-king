---
problems:
  - title: 爬楼梯
    url: https://leetcode.cn/problems/climbing-stairs/
    difficulty: easy
  - title: 最大子数组和
    url: https://leetcode.cn/problems/maximum-subarray/
    difficulty: medium
  - title: 打家劫舍
    url: https://leetcode.cn/problems/house-robber/
    difficulty: medium
  - title: 零钱兑换
    url: https://leetcode.cn/problems/coin-change/
    difficulty: medium
  - title: 最长递增子序列
    url: https://leetcode.cn/problems/longest-increasing-subsequence/
    difficulty: medium
---

# 动态规划 Top 题

动态规划是算法面试中的重点和难点，掌握动态规划的解题思路对于通过技术面试至关重要。本章节将介绍一些高频的动态规划面试题。

## 1. 爬楼梯

### 题目描述
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶？

### 解题思路
- **状态定义**：`dp[i]` 表示爬到第 i 阶楼梯的方法数
- **状态转移**：`dp[i] = dp[i-1] + dp[i-2]`，因为到达第 i 阶楼梯的方法数等于到达第 i-1 阶的方法数加上到达第 i-2 阶的方法数
- **初始状态**：`dp[1] = 1`，`dp[2] = 2`

### 代码实现

```java
public class Solution {
    public int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        int[] dp = new int[n + 1];
        dp[1] = 1;
        dp[2] = 2;
        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }
}
```

## 2. 最大子数组和

### 题目描述
给你一个整数数组 `nums`，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

### 解题思路
- **状态定义**：`dp[i]` 表示以第 i 个元素结尾的最大子数组和
- **状态转移**：`dp[i] = max(nums[i], dp[i-1] + nums[i])`，即要么当前元素自己构成一个子数组，要么与前面的子数组连接
- **初始状态**：`dp[0] = nums[0]`

### 代码实现

```java
public class Solution {
    public int maxSubArray(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        dp[0] = nums[0];
        int max = dp[0];
        for (int i = 1; i < n; i++) {
            dp[i] = Math.max(nums[i], dp[i - 1] + nums[i]);
            max = Math.max(max, dp[i]);
        }
        return max;
    }
}
```

## 3. 打家劫舍

### 题目描述
你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

### 解题思路
- **状态定义**：`dp[i]` 表示前 i 个房屋能偷到的最高金额
- **状态转移**：`dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])`，即要么不偷第 i 个房屋，要么偷第 i 个房屋但不偷第 i-1 个房屋
- **初始状态**：`dp[0] = 0`，`dp[1] = nums[0]`

### 代码实现

```java
public class Solution {
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 0) {
            return 0;
        }
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = nums[0];
        for (int i = 2; i <= n; i++) {
            dp[i] = Math.max(dp[i - 1], dp[i - 2] + nums[i - 1]);
        }
        return dp[n];
    }
}
```

## 4. 零钱兑换

### 题目描述
给你一个整数数组 `coins` ，表示不同面额的硬币；以及一个整数 `amount` ，表示总金额。

计算并返回可以凑成总金额所需的 最少的硬币个数 。如果没有任何一种硬币组合能组成总金额，返回 `-1` 。

### 解题思路
- **状态定义**：`dp[i]` 表示凑成金额 i 所需的最少硬币个数
- **状态转移**：对于每个金额 i，遍历所有硬币面额 coin，如果 i >= coin，则 `dp[i] = min(dp[i], dp[i-coin] + 1)`
- **初始状态**：`dp[0] = 0`，其他初始化为无穷大

### 代码实现

```java
public class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (i >= coin && dp[i - coin] != Integer.MAX_VALUE) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount];
    }
}
```

## 5. 最长递增子序列

### 题目描述
给你一个整数数组 `nums` ，找到其中最长严格递增子序列的长度。

### 解题思路
- **状态定义**：`dp[i]` 表示以第 i 个元素结尾的最长递增子序列的长度
- **状态转移**：对于每个 i，遍历 j 从 0 到 i-1，如果 nums[i] > nums[j]，则 `dp[i] = max(dp[i], dp[j] + 1)`
- **初始状态**：所有 `dp[i]` 初始化为 1

### 代码实现

```java
public class Solution {
    public int lengthOfLIS(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        int max = 1;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[i] > nums[j]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
            max = Math.max(max, dp[i]);
        }
        return max;
    }
}
```

## 总结

动态规划问题的关键在于找到正确的状态定义和状态转移方程。通过练习这些高频题目，可以掌握动态规划的基本思路和解题技巧，为面试做好准备。