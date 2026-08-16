---
title: 回溯专项练习 I（排列 / 组合 / 子集）
---

# 回溯专项练习 I（排列 / 组合 / 子集）

> 配套：回溯本质就是「**决策树的 DFS**」。排列/组合/子集这三类是回溯的最经典应用，区别只在三件事：**要不要回头（用 used 还是 start）、要不要去重（同层跳重复）、什么时候收集结果（进函数 / 叶子 / 每个节点）**。下面精讲 3 道覆盖三种范式（子集 / 排列 / 组合），再给 7 道变化点清单。

## 框架速记

```text
void backtrack(路径, 选择列表) {
    if (满足结束条件) { result.add(路径副本); return; }   // ← 副本！
    for (选择 : 选择列表) {
        做选择（加入路径）;
        backtrack(路径, 新选择列表);
        撤销选择（从路径移除）;     // ← 回溯的关键
    }
}
```

三个钩子：**选择列表怎么来（start / used / 全集）**、**去重（排序 + 同层跳相同）**、**收集时机（每个节点 / 叶子 / 特定条件）**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [子集](https://leetcode.cn/problems/subsets/) | 中 | 每个节点都收集，start 不回头 |
| 2 | [子集 II](https://leetcode.cn/problems/subsets-ii/) | 中 | 1 + 排序去重 |
| 3 | [全排列](https://leetcode.cn/problems/permutations/) | 中 | used 数组，每层从 0 遍历 |
| 4 | [全排列 II](https://leetcode.cn/problems/permutations-ii/) | 中 | 3 + 排序去重 |
| 5 | [组合总和](https://leetcode.cn/problems/combination-sum/) | 中 | 可重复选，递归传 i 不回头 |
| 6 | [组合总和 II](https://leetcode.cn/problems/combination-sum-ii/) | 中 | 不可重复选 + 去重 |
| 7 | [组合](https://leetcode.cn/problems/combinations/) | 中 | 固定大小 k 的组合 |
| 8 | [电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/) | 中 | 多组选择列表 |
| 9 | [分割回文串](https://leetcode.cn/problems/palindrome-partitioning/) | 中 | 分割点为选择 |
| 10 | [复原 IP 地址](https://leetcode.cn/problems/restore-ip-addresses/) | 中 | 分割 + 合法性约束 |

---

## 例题 1：子集（LC 78，每个节点都收集）

**题目**：返回不含重复元素的数组的所有子集（幂集）。

**如何套 + 变化点**：回溯决策树，每个节点代表「选了某几个元素」。子集题的特点是「**每个节点都要收集**」（不是只叶子），因为路径上每一步都是一个合法子集。用 `start` 控制不回头（避免 `[1,2]` 和 `[2,1]` 重复，子集不分顺序）。

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> res = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), res);
    return res;
}
private void backtrack(int[] nums, int start, List<Integer> path, List<List<Integer>> res) {
    res.add(new ArrayList<>(path));        // 每个节点都收集（副本）
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]);
        backtrack(nums, i + 1, path, res);  // i+1 不回头
        path.remove(path.size() - 1);       // 撤销
    }
}
```

**易错点**：
- 收集必须用 `new ArrayList<>(path)`，**不能 `res.add(path)`**。path 在整个回溯中是同一个对象，直接 add 会让 res 里所有元素指向同一个 path，最后全是空（撤销到底）。必须拷贝当前快照。
- 子集用 `start` 不回头（`backtrack(nums, i+1, ...)`），**不用 used 数组**。子集 `[1,2]` 和 `[2,1]` 视为同一个，start 保证后选的下标大于前选，天然去重。

---

## 例题 2：全排列（LC 46，used 回头）

**题目**：返回不含重复元素的数组的所有全排列。

**如何套 + 变化点**：和子集的关键区别——排列**顺序敏感**（`[1,2]` 和 `[2,1]` 是两个排列）。所以不能 start 不回头（那会漏掉 `[2,1]`），要用 **used 数组**，每层都从 0 遍历、跳过已用。叶子（path 长度 == nums 长度）才收集。

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> res = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), res);
    return res;
}
private void backtrack(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> res) {
    if (path.size() == nums.length) { res.add(new ArrayList<>(path)); return; }   // 叶子收集
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        path.add(nums[i]); used[i] = true;
        backtrack(nums, used, path, res);
        path.remove(path.size() - 1); used[i] = false;                            // 撤销要成对
    }
}
```

**易错点**：
- **撤销要成对**：`path.remove` 的同时必须 `used[i] = false`。只撤销 path 忘了 used，会导致后续分支以为某元素没用，重复选，结果错乱。
- 收集时机是**叶子**（`path.size() == nums.length`），不是每个节点。子集每节点都收（因为任意大小都是合法子集），排列只有「选满」才是合法排列。混淆会多收或漏收。

**对比**：例 1（子集）用 start、每节点收集；例 2（排列）用 used、叶子收集。选择列表怎么来 + 收集时机，两类题完全不同。

---

## 例题 3：组合总和（LC 39，可重复选 + 不回头）

**题目**：无重复正整数数组 `candidates` 和目标 `target`，找出所有和为 target 的组合（同一数字可无限次选）。返回的组合集合不能重复。

**为什么用 start 而非 used**：这道题「可重复选」+「组合不分顺序」。如果用 used + 每层从 0，会得到 `[2,3]` 和 `[3,2]` 两个重复组合。用 **start 不回头**（递归传 `i` 而非 `i+1`，保证可重复选当前；下一层从 `i` 开始而非 `i+1` 保证不回头），天然避免顺序变体。

**如何套 + 变化点**：`start` 控制不回头，递归传 `i`（不是 `i+1`，允许重复选当前元素）。叶子条件是「和 ≥ target」（== 收集，> 剪枝）。

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> res = new ArrayList<>();
    Arrays.sort(candidates);   // 排序便于剪枝
    backtrack(candidates, 0, target, new ArrayList<>(), res);
    return res;
}
private void backtrack(int[] candidates, int start, int remain, List<Integer> path, List<List<Integer>> res) {
    if (remain == 0) { res.add(new ArrayList<>(path)); return; }
    for (int i = start; i < candidates.length; i++) {
        if (candidates[i] > remain) break;        // 排序后剪枝，后面更大直接 break
        path.add(candidates[i]);
        backtrack(candidates, i, remain - candidates[i], path, res);   // 传 i 不是 i+1（可重复）
        path.remove(path.size() - 1);
    }
}
```

**易错点**：
- 递归传 **`i` 不是 `i+1`**。传 `i` 允许重复选当前元素（如 candidates=[2,3], target=4，选 2 后还能选 2 得 `[2,2]`）；传 `i+1` 就退化成「不可重复」，漏解。
- 剪枝 `if (candidates[i] > remain) break` 依赖**先排序**（`Arrays.sort`）。不排序只能 `continue`（后面可能有更小的），排序后才能 `break`（后面更大，一定超）。漏了排序就 break 会漏解。

---

## 练习建议

按范式分组：
- 子集（每节点收集 + start）：1、2
- 排列（used 回头 + 叶子收集）：3、4
- 组合（start + 可重复/不可重复）：5、6、7
- 分割（分割点为选择）：9、10
- 多组选择列表：8

**如果时间只够做 3 道**：做 **1、3、5**——分别覆盖「子集 / 排列 / 组合」回溯三大范式，做完这三道，回溯的「选择列表怎么来 + 去重 + 收集时机」就通了，2/4/6 都是这三道的去重变体（加排序 + 同层跳相同）。

## 下一步

本篇覆盖排列/组合/子集三大类；剩下 7 道的变化点已在表格列出。回溯去重的核心套路（**排序 + 同层跳相同元素**）在做 2/4/6 时会反复遇到，做一道就懂。卡题时回看本篇「三个钩子」，对照「选择列表怎么来、要不要去重、什么时候收集」。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
