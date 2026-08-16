---
title: 动态规划专项练习 II（二维背包与子序列）
---

# 动态规划专项练习 II（二维背包与子序列）

> 配套：[动态规划 I（一维入门）](./dynamic-programming-practice-i/)。本篇讲二维 DP——**背包**（选不选 + 容量）和**子序列**（双串对齐）。难点在三件事：**dp[i][j] 表示什么（前 i 个 / 以 i j 结尾 / 容量 j）**、**物品能不能重复用（0-1 倒序 / 完全正序）**、**转移有几个分支**。

## 框架速记

```text
// 0-1 背包（一维滚动）：每个物品选或不选，倒序避免重复
int[] dp = new int[capacity + 1];
for (int num : items) {
    for (int j = capacity; j >= num; j--) {   // ← 倒序
        dp[j] = Math.max(dp[j], dp[j - num] + value[num]);
    }
}

// 双串子序列：dp[i][j] = s1 前 i 与 s2 前 j 的最优
int[][] dp = new int[m + 1][n + 1];
for (int i = 1; i <= m; i++) for (int j = 1; j <= n; j++) {
    if (s1[i-1] == s2[j-1]) dp[i][j] = dp[i-1][j-1] + 1;
    else dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
}
```

三个钩子：**dp 维度含义**、**遍历顺序（倒序 / 正序）**、**转移分支数**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/) | 中 | 0-1 背包判定能否凑 target |
| 2 | [目标和](https://leetcode.cn/problems/target-sum/) | 中 | 0-1 背包计数 |
| 3 | [零钱兑换](https://leetcode.cn/problems/coin-change/) | 中 | 完全背包求最少 |
| 4 | [零钱兑换 II](https://leetcode.cn/problems/coin-change-ii/) | 中 | 完全背包计数 |
| 5 | [最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/) | 中 | 双串 LCS |
| 6 | [最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/) | 中 | 一维 DP（O(n²)）或 二分（O(n log n)） |
| 7 | [不同的子序列](https://leetcode.cn/problems/distinct-subsequences/) | 中 | 双串计数 |
| 8 | [两个字符串的删除操作](https://leetcode.cn/problems/delete-operation-for-two-strings/) | 中 | LCS 变体（m+n-2·LCS） |
| 9 | [买卖股票的最佳时机 IV](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/) | 困 | k 次交易的状态机 DP |
| 10 | [编辑距离](https://leetcode.cn/problems/edit-distance/) | 中 | 三分支：增/删/改 |

---

## 例题 1：分割等和子集（LC 416，0-1 背包判定）

**题目**：判断正整数数组能否分成两个子集，使两子集和相等。

**为什么是背包**：两子集和相等 = 其中一个子集和等于 `sum/2`。问题变成「从 nums 里选若干元素，能否凑出 `sum/2`」——这就是标准 0-1 背包（每个元素选或不选，目标容量 `sum/2`）。

**如何套 + 变化点**：`dp[j]` = 能否凑出和 j。初始 `dp[0] = true`（凑和 0 不选任何元素）。对每个 num，倒序更新 `dp[j] = dp[j] || dp[j-num]`。

```java
public boolean canPartition(int[] nums) {
    int sum = 0;
    for (int n : nums) sum += n;
    if (sum % 2 != 0) return false;          // 奇数不可能平分
    int target = sum / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;
    for (int num : nums) {
        for (int j = target; j >= num; j--) {   // ← 倒序
            dp[j] = dp[j] || dp[j - num];
        }
    }
    return dp[target];
}
```

**易错点**：
- 内层**倒序**（`j = target; j >= num; j--`），不是正序。0-1 背包每个物品只能选一次——倒序保证 `dp[j]` 用的是「上一轮的 dp[j-num]」（同物品还没被选）；正序会让 `dp[j-num]` 已经包含了当前 num，相当于同物品被选多次（退化成完全背包）。
- `sum` 为奇直接返回 false，**不能漏**。奇数和无法分成两个整数相等的子集，不提前判会让 target = sum/2 含小数（int 截断），逻辑错。
- `dp[0] = true`（凑和 0 是「什么都不选」，合法）。漏了这行所有 dp 都 false，返回错。

---

## 例题 2：最长公共子序列（LC 1143，双串）

**题目**：求两个字符串的最长公共子序列长度（子序列可不连续）。

**如何套 + 变化点**：`dp[i][j]` = `s1` 前 i 个字符与 `s2` 前 j 个字符的 LCS 长度。两字符相等就 `dp[i-1][j-1] + 1`；不等就取 `max(dp[i-1][j], dp[i][j-1])`（要么不算 s1 的第 i 个，要么不算 s2 的第 j 个）。

```java
public int longestCommonSubsequence(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1.charAt(i - 1) == s2.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1] + 1;
            else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    return dp[m][n];
}
```

**易错点**：
- 比较 `s1.charAt(i-1)` 和 `s2.charAt(j-1)`，**下标是 `i-1` 不是 `i`**。dp 维度是 `m+1 × n+1`（含空串），第 i 行对应 s1 的第 i-1 个字符。写 `i` 会越界且语义错。
- `dp` 数组多一行一列（第 0 行/列表示空串，LCS = 0），**不用初始化**（int 默认 0）。但有些人习惯从 0 开始遍历字符串（`i = 0`），那就得自己处理边界——统一用 `i = 1` 起 + `charAt(i-1)` 最省事。
- 不等时取 `max(dp[i-1][j], dp[i][j-1])`，**不要漏 `dp[i-1][j-1]`**。虽然 `dp[i-1][j-1] ≤ max(dp[i-1][j], dp[i][j-1])` 所以不影响答案，但写 `max(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` 更清晰，避免新手误以为「不等就一定要舍弃」。

---

## 例题 3：编辑距离（LC 72，三分支）

**题目**：把 `word1` 变成 `word2` 的最少操作次数（插入/删除/替换一个字符各算 1 次）。

**如何套 + 变化点**：`dp[i][j]` = `word1` 前 i 个变成 `word2` 前 j 个的最少操作。字符相等 → `dp[i-1][j-1]`（无操作）；不等 → 三种操作取 min：替换 `dp[i-1][j-1] + 1`、删除 word1 第 i 个 `dp[i-1][j] + 1`、插入（等价于删 word2 第 j 个）`dp[i][j-1] + 1`。

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i;      // word2 为空：删 i 个
    for (int j = 0; j <= n; j++) dp[0][j] = j;      // word1 为空：插 j 个
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
        }
    }
    return dp[m][n];
}
```

**易错点**：
- **base case `dp[i][0] = i` 和 `dp[0][j] = j`**。word2 为空时，把 word1 前 i 个全删（i 次操作）；word1 为空时，插 j 个（j 次）。漏了 base case 会全 0（int 默认），返回错。
- 不等时的三种操作对应**三个不同的 dp 来源**：`dp[i-1][j-1]+1`（替换）、`dp[i-1][j]+1`（删 word1[i-1]）、`dp[i][j-1]+1`（删 word2[j-1]，等价于在 word1 插入）。三者取 min，**漏一个就错**。新人常只写替换和删除，漏了「插入」（其实是对称的）。
- 编辑距离是「双串 DP」的集大成者——LCS 是它的特例（只删不替换）。理解了这道题，7/8（不同的子序列、删除操作）就是降维。

---

## 练习建议

按模板分组：
- 0-1 背包（倒序）：1、2
- 完全背包（正序）：3、4
- 双串子序列：5、7、8
- 一维变体：6
- 状态机 DP：9（股票 k 次）
- 三分支：10（编辑距离）

**如果时间只够做 3 道**：做 **1、5、10**——分别覆盖「0-1 背包 / 双串 LCS / 编辑距离」二维 DP 三大模板。2 是 1 的计数变体，3/4 是 1/2 换完全背包，7/8 是 5/10 的变体。

## 下一步

06-practice 专项练习 9 篇到此收官。二维 DP 是 DP 的分水岭——1/5/10 这三道彻底吃透，背包和子序列两大类就通了。卡题时回看 [动态规划框架](../00-algorithm-frameworks/dynamic-programming/) 和本篇「三个钩子」，对照「dp 维度、遍历顺序、转移分支」。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
