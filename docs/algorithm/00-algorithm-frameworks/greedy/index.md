---
problems:
  - title: 分发饼干
    url: https://leetcode.cn/problems/assign-cookies/
    difficulty: easy
  - title: 跳跃游戏
    url: https://leetcode.cn/problems/jump-game/
    difficulty: medium
  - title: 买卖股票的最佳时机 II
    url: https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/
    difficulty: medium
---

# 贪心算法框架

## 算法原理

贪心算法是一种在每一步选择中都采取在当前状态下最好或最优（即最有利）的选择，从而希望导致结果是全局最好或最优的算法。

贪心算法的核心思想是：在问题的每个阶段，都做出一个局部最优的选择，期望通过这些局部最优选择的积累，最终得到全局最优解。

## 框架模板

```java
public int greedyAlgorithm(int[] nums) {
    // 1. 预处理：排序或其他操作
    Arrays.sort(nums);
    
    // 2. 贪心选择：从局部最优开始，逐步构建全局最优
    int result = 0;
    int current = 0;
    
    for (int i = 0; i < nums.length; i++) {
        // 做出当前的最优选择
        current = Math.max(current + nums[i], nums[i]);
        // 更新全局最优
        result = Math.max(result, current);
    }
    
    return result;
}
```

## 适用场景

贪心算法适用于具有以下性质的问题：

1. **贪心选择性质**：整体的最优解可以通过一系列局部最优的选择来得到
2. **最优子结构**：问题的最优解包含其子问题的最优解

常见的贪心算法问题包括：
- **活动选择问题**：选择最多的不重叠活动
- **霍夫曼编码**：构建最优前缀码
- **分数背包问题**：在背包容量有限的情况下，最大化物品的总价值
- **最小生成树**：如 Kruskal 算法和 Prim 算法
- **单源最短路径**：如 Dijkstra 算法

## 注意事项

1. **贪心策略的正确性**：不是所有问题都适合使用贪心算法，需要证明贪心策略能够得到全局最优解
2. **排序的重要性**：许多贪心问题需要先对数据进行排序
3. **局部最优与全局最优的关系**：局部最优的选择必须能够导致全局最优

## 示例：分发饼干

### 题目描述

假设你是一位很棒的家长，想要给你的孩子们一些小饼干。但是，每个孩子最多只能给一块饼干。

对每个孩子 i，都有一个胃口值 g[i]，这是能让孩子们满足胃口的饼干的最小尺寸；并且每块饼干 j，都有一个尺寸 s[j] 。如果 s[j] >= g[i]，我们可以将这个饼干 j 分配给孩子 i ，这个孩子会得到满足。你的目标是尽可能满足越多数量的孩子，并输出这个最大数值。

### 代码实现

```java
public int findContentChildren(int[] g, int[] s) {
    // 排序
    Arrays.sort(g);
    Arrays.sort(s);
    
    int i = 0;  // 孩子的索引
    int j = 0;  // 饼干的索引
    
    while (i < g.length && j < s.length) {
        if (s[j] >= g[i]) {
            // 饼干能满足孩子的胃口
            i++;
        }
        // 无论是否满足，饼干都要移动到下一个
        j++;
    }
    
    return i;
}
```

### 解释

1. **排序**：将孩子的胃口值和饼干的尺寸从小到大排序
2. **贪心选择**：
   - 从最小的饼干开始，尝试满足最小胃口的孩子
   - 如果饼干能满足孩子的胃口，就将饼干分配给这个孩子，并移动到下一个孩子
   - 无论是否满足，都移动到下一个饼干
3. **返回结果**：返回满足的孩子数量

## 示例：跳跃游戏

### 题目描述

给定一个非负整数数组 `nums`，你最初位于数组的第一个位置。

数组中的每个元素代表你在该位置可以跳跃的最大长度。

判断你是否能够到达最后一个位置。

### 代码实现

```java
public boolean canJump(int[] nums) {
    int n = nums.length;
    int farthest = 0;  // 记录当前能到达的最远距离
    
    for (int i = 0; i < n; i++) {
        // 如果当前位置超过了能到达的最远距离，返回 false
        if (i > farthest) {
            return false;
        }
        // 更新能到达的最远距离
        farthest = Math.max(farthest, i + nums[i]);
        // 如果已经能到达最后一个位置，返回 true
        if (farthest >= n - 1) {
            return true;
        }
    }
    
    return false;
}
```

### 解释

1. **贪心选择**：
   - 记录当前能到达的最远距离 `farthest`
   - 遍历数组，对于每个位置，更新能到达的最远距离
   - 如果当前位置超过了能到达的最远距离，说明无法继续前进，返回 false
   - 如果能到达的最远距离已经超过或等于最后一个位置，返回 true

## 示例：买卖股票的最佳时机 II

### 题目描述

给定一个数组 `prices`，其中 `prices[i]` 是一支给定股票第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。

### 代码实现

```java
public int maxProfit(int[] prices) {
    int maxProfit = 0;
    
    for (int i = 1; i < prices.length; i++) {
        // 如果今天的价格比昨天高，就进行交易
        if (prices[i] > prices[i-1]) {
            maxProfit += prices[i] - prices[i-1];
        }
    }
    
    return maxProfit;
}
```

### 解释

1. **贪心选择**：
   - 遍历数组，对于每一天，如果今天的价格比昨天高，就进行交易，赚取差价
   - 这样的策略可以捕获所有的上涨区间，从而获得最大利润

## 总结

贪心算法是一种简单而有效的算法方法，适用于具有贪心选择性质和最优子结构的问题。通过在每一步做出局部最优的选择，贪心算法可以快速得到全局最优解。在实际应用中，需要注意证明贪心策略的正确性，并根据问题的特点选择合适的贪心策略。