---
title: 动态规划专项练习 I（一维入门）
---

# 动态规划专项练习 I（一维入门）

> 配套框架：[动态规划框架](../00-algorithm-frameworks/dynamic-programming/)。一维 DP 的所有题，骨架只有一个——**「当前状态由前几个状态推出」**。难点不在写代码（模板就一个双层结构），而在三件事：**状态怎么定义、转移方程怎么写、初始值怎么定**。下面精讲 3 道覆盖三种典型转移（线性递推 / 选不选 / 以 i 结尾），再给 7 道变化点清单。

## 框架速记

```text
// 一维 DP 模板
int[] dp = new int[n + 1];
dp[0] = 初始值;   // ← 初始值定错，全盘错
for (int i = 1; i <= n; i++) {
    dp[i] = 由 dp[i-1], dp[i-2] ... 推出;   // ← 转移方程
}
return dp[n]（或 max(dp)）;
```

三个钩子：**状态定义（dp[i] 表示什么）**、**转移方程**、**初始值**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [爬楼梯](https://leetcode.cn/problems/climbing-stairs/) | 简 | 线性递推：dp[i] = dp[i-1] + dp[i-2] |
| 2 | [斐波那契数](https://leetcode.cn/problems/fibonacci-number/) | 简 | 同 1，更基础 |
| 3 | [使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/) | 简 | 线性递推 + 取 min |
| 4 | [打家劫舍](https://leetcode.cn/problems/house-robber/) | 中 | 选/不选：偷→dp[i-2]+nums[i]，不偷→dp[i-1] |
| 5 | [打家劫舍 II](https://leetcode.cn/problems/house-robber-ii/) | 中 | 环形：拆成两条线性分别 DP |
| 6 | [删除并获得点数](https://leetcode.cn/problems/delete-and-earn/) | 中 | 打家劫舍变体（按值聚合计数） |
| 7 | [最大子数组和](https://leetcode.cn/problems/maximum-subarray/) | 中 | dp[i] = max(nums[i], dp[i-1]+nums[i]) |
| 8 | [整数拆分](https://leetcode.cn/problems/integer-break/) | 中 | dp[i] = max(j·(i-j), j·dp[i-j]) |
| 9 | [不同的二叉搜索树](https://leetcode.cn/problems/unique-binary-search-trees/) | 中 | 卡特兰数：dp[i] = Σ dp[j]·dp[i-1-j] |
| 10 | [解码方法](https://leetcode.cn/problems/decode-ways/) | 中 | 一位/两位两种转移 |

---

## 例题 1：爬楼梯（LC 70，线性递推）

**题目**：每次爬 1 或 2 阶，爬到第 n 阶有多少种方法。

**为什么是 DP 不是暴力**：从第 n 阶往回看，只有两种可能来源——从 n-1 阶爬 1 步、从 n-2 阶爬 2 步。所以「到 n 阶的方法数 = 到 n-1 的方法数 + 到 n-2 的方法数」。这就是最优子结构，递推即可，不用暴力枚举所有走法（指数级）。

**如何套 + 变化点**：`dp[i]` = 到第 i 阶的方法数。转移 `dp[i] = dp[i-1] + dp[i-2]`。初始值 `dp[0] = 1`（站在地面算 1 种）、`dp[1] = 1`。

```java
public int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;   // 滚动数组，只用前两个
    for (int i = 3; i <= n; i++) {
        int cur = prev1 + prev2;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

**易错点**：
- `dp[0] = 1`，**不是 0**。dp[0] 表示「站在地面（0 阶）的方法数」，算 1 种（站着不动）。写 0 会让 `dp[2] = dp[1] + dp[0] = 1 + 0 = 1`，但实际到 2 阶有 2 种（1+1 或 2），全盘错。
- 这题**等价于斐波那契**（`dp[i] = dp[i-1] + dp[i-2]`），但**初始值不同**——斐波那契 fib(0)=0, fib(1)=1；爬楼梯 dp[0]=1, dp[1]=1。套同一个转移方程，初始值定错就答案差一位。

---

## 例题 2：打家劫舍（LC 198，选/不选）

**题目**：数组表示每家钱数，不能偷相邻两家，求最多偷多少。

**如何套 + 变化点**：`dp[i]` = 前 i 家最多能偷多少。对每家有两种选择：**偷**（则前一家不能偷，`dp[i-2] + nums[i-1]`）或 **不偷**（继承前一家 `dp[i-1]`）。取 max。

```java
public int rob(int[] nums) {
    int n = nums.length;
    if (n == 1) return nums[0];
    int prev2 = nums[0];                 // dp[1]：只有第 1 家
    int prev1 = Math.max(nums[0], nums[1]);  // dp[2]：前两家取大
    for (int i = 3; i <= n; i++) {
        int cur = Math.max(prev1, prev2 + nums[i - 1]);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

**易错点**：
- **偷的情况是 `dp[i-2] + nums[i-1]`**，不是 `dp[i-1] + nums[i-1]`。偷了第 i-1 家（数组下标 i-1，对应第 i 家），就不能偷第 i-1 家（相邻），所以只能从 `dp[i-2]` 来。
- 初始化要单独处理 `n == 1`：直接返回 `nums[0]`，否则 `Math.max(nums[0], nums[1])` 会越界（n=1 时没 nums[1]）。
- `nums` 下标和 `dp` 下标错位：`dp[i]` 是「前 i 家」，对应数组 `nums[0..i-1]`。第 i 家钱是 `nums[i-1]`，不是 `nums[i]`。

---

## 例题 3：最大子数组和（LC 53，以 i 结尾）

**题目**：找连续子数组使其和最大，返回最大和。

**为什么状态是「以 i 结尾」不是「前 i 个」**：子数组要求**连续**。如果 `dp[i]` 定义为「前 i 个的最大子数组和」，那么 `dp[i]` 和 `dp[i-1]` 之间没有清晰转移——最大子数组可能在前 i-1 个里（不含 i），也可能含 i，含 i 时又必须从某处连续到 i，状态不闭合。定义成「**以 nums[i] 结尾**的最大子数组和」就清晰了：要么延续前面的（`dp[i-1] + nums[i]`），要么从 i 重新开始（`nums[i]`），取 max。连续性由「以 i 结尾」自动保证。

**如何套 + 变化点**：`dp[i]` = 以 `nums[i]` 结尾的最大子数组和。转移 `dp[i] = max(nums[i], dp[i-1] + nums[i])`。答案是 `max(dp)`（不是 `dp[n-1]`，因为最大子数组可能结束在任意位置）。

```java
public int maxSubArray(int[] nums) {
    int cur = nums[0], ans = nums[0];   // cur = dp[i]，ans = max(dp)
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(nums[i], cur + nums[i]);
        ans = Math.max(ans, cur);
    }
    return ans;
}
```

**易错点**：
- `ans` 初始 `nums[0]`，**不是 0 或 `Integer.MIN_VALUE`**。如果全负（如 `[-1, -2]`），最大子数组和是 `-1`（单元素），`ans=0` 会错返回 0（空子数组，但题目要求非空）。用 `nums[0]` 从第一个元素开始，逻辑统一。
- 答案是 `max(dp)`（遍历过程中维护 `ans`），**不是 `dp[n-1]`**。`dp[i]` 是「以 i 结尾」的最大，但全局最大可能结束在中间任意 i。返回最后一个 dp 会漏。

**对比**：例 1/2 的 `dp[i]` 是「前 i 个/到第 i 阶」，例 3 是「以 i 结尾」——状态定义直接决定转移能否写对。

---

## 练习建议

按转移类型分组：
- 线性递推（基础）：1、2、3
- 选/不选（打家劫舍系列）：4、5、6
- 以 i 结尾（连续子序列）：7
- 计数型 DP：8、9、10

**如果时间只够做 3 道**：做 **4、7、10**——分别覆盖「选/不选 / 以 i 结尾 / 多种转移并存」三种最典型的状态设计。1/2 是热身，5/6 是 4 的变体。

## 下一步

动态规划专项 II 会讲二维 DP（背包、子序列、股票）。本篇覆盖一维入门；剩下 7 道的变化点已在表格列出。卡题时回看 [动态规划框架](../00-algorithm-frameworks/dynamic-programming/)，对照「状态定义 + 转移方程 + 初始值」三处钩子。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）

---

<div class="review-guide">
<div class="review-guide-title">📝 做完后复盘引导</div>
<ol>
  <li>**用费曼技巧讲解**：不看代码，试着用自己的话向一个完全不懂算法的人讲解「一维动态规划的核心思想」。能讲清楚吗？</li>
  <li>**找出你的漏洞**：在讲解过程中，哪些地方卡壳了？是状态定义不清楚？还是转移方程的推导逻辑不明白？</li>
  <li>**对比不同题目**：把做过的题目按「线性递推 / 选不选 / 以 i 结尾」分类，每类的状态定义和转移方程有什么规律？</li>
  <li>**尝试变体**：如果把题目条件改一下（比如爬楼梯从 1/2 步改成 1/3/5 步），你的解法还适用吗？哪里需要改？</li>
</ol>
</div>
