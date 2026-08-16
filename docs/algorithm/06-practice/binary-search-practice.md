---
title: 二分查找专项练习
---

# 二分查找专项练习

> 配套框架：[二分查找框架](../00-algorithm-frameworks/binary-search/)。二分题刷不熟，多半不是思路不会，而是**边界写崩**（死循环、漏一个、下标越界）。下面精讲 3 道覆盖三种典型二分（精确匹配 / 找边界 / 旋转数组），再给 7 道变化点清单。核心只在一件事：**搜索区间怎么定义、收缩分支怎么写**。

## 框架速记

```text
int left = 0, right = n;     // 左闭右开 [left, right)
while (left < right) {       // 终止：left == right
    int mid = left + (right - left) / 2;
    if (满足条件) right = mid;       // 收缩右边界，mid 可能为答案
    else            left = mid + 1;  // 收缩左边界，mid 已排除
}
return left;                 // 或按题意返回
```

三个钩子：**搜索区间（左闭右开 / 左闭右闭）**、**收缩分支（right = mid 还是 mid-1）**、**返回值（left 还是 mid）**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [二分查找](https://leetcode.cn/problems/binary-search/) | 简 | 标准模板，精确匹配 |
| 2 | [查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) | 中 | 左边界 + 右边界两次二分 |
| 3 | [搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/) | 中 | 先判哪半有序，再决定方向 |
| 4 | [寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/) | 中 | 与右端点比，判中点在哪半 |
| 5 | [x 的平方根](https://leetcode.cn/problems/sqrtx/) | 简 | 二分答案，mid*mid 与 x 比 |
| 6 | [第一个错误的版本](https://leetcode.cn/problems/first-bad-version/) | 简 | 找第一个 true（左边界） |
| 7 | [寻找峰值](https://leetcode.cn/problems/find-peak-element/) | 中 | 与右邻比，往上升方向走 |
| 8 | [有效的完全平方数](https://leetcode.cn/problems/valid-perfect-square/) | 简 | 二分找平方等于 num 的数 |
| 9 | [爱吃香蕉的珂珂](https://leetcode.cn/problems/koko-eating-bananas/) | 中 | 二分答案：以速度为变量二分最小速度 |
| 10 | [寻找两个正序数组的中位数](https://leetcode.cn/problems/median-of-two-sorted-arrays/) | 困 | 二分划分数组（压轴） |

---

## 例题 1：二分查找（LC 704，基础）

**题目**：给定升序数组 `nums` 和目标值 `target`，返回下标，未找到返回 -1。

**如何套 + 变化点**：标准左闭右开 `[left, right)`，收缩看「mid 的值与 target 比大小」，相等即返回。

```java
public int search(int[] nums, int target) {
    int left = 0, right = nums.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) left = mid + 1;
        else right = mid;
    }
    return -1;
}
```

**易错点**：
- `mid = left + (right - left) / 2`，**不是 `(left + right) / 2`**。后者在 `left + right` 接近 `Integer.MAX_VALUE` 时溢出成负数，数组下标越界。这是二分最经典的坑，面试官爱问。
- 左闭右开区间 `right = nums.length`（不是 `length - 1`），循环条件 `left < right`（不是 `<=`）。区间定义和循环条件必须配套——混用「右开区间 + `<=` 循环」会多查一个越界位置，「右闭区间 + `<` 循环」会漏查最后一个元素。

---

## 例题 2：查找元素的第一个和最后一个位置（LC 34，左/右边界）

**题目**：返回 `target` 在排序数组里的起止下标，无则 `[-1,-1]`。

**如何套 + 变化点**：精确匹配（704）找到就 return，但本题要找「重复元素的左右边界」。分两步——**先二分找左边界（第一个 == target），再二分找右边界（最后一个 == target）**。关键是「找到 `nums[mid] == target` 时**不 return**，继续往左/右压」。

```java
public int[] searchRange(int[] nums, int target) {
    return new int[]{ leftBound(nums, target), rightBound(nums, target) };
}

// 左边界：第一个 == target 的位置
int leftBound(int[] nums, int target) {
    int left = 0, right = nums.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] < target) left = mid + 1;
        else right = mid;          // == 也收缩右，继续往左找
    }
    if (left == nums.length || nums[left] != target) return -1;
    return left;
}

// 右边界：最后一个 == target 的位置（等价于「第一个 > target 的位置」-1）
int rightBound(int[] nums, int target) {
    int left = 0, right = nums.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] <= target) left = mid + 1;   // <= 都往右压
        else right = mid;
    }
    int last = left - 1;
    if (last < 0 || nums[last] != target) return -1;
    return last;
}
```

**易错点**：
- 左边界：`nums[mid] < target` 才 `left = mid + 1`，**`==` 和 `>` 都走 `right = mid`**（往左压）。如果 `==` 时 `return mid`，就退化成 704，找不到边界。
- 右边界：`nums[mid] <= target` 都 `left = mid + 1`（含 `==`，往右压）。注意是 `<=` 不是 `<`——`<` 会让 `==` 的 mid 被当左边界收缩，漏掉右半的重复元素。
- 返回前必须**越界检查**：左边界可能 `left == nums.length`（target 比所有数大），右边界可能 `last < 0`（target 比所有数小）；不判会数组越界。

**对比 704**：704 找到就停，本题找到不停（继续压边界）。这是「精确匹配」和「找边界」的区别。

---

## 例题 3：搜索旋转排序数组（LC 33，旋转）

**题目**：升序数组在某个点旋转（如 `[4,5,6,7,0,1,2]`），找 `target` 下标。

**为什么先判有序半区**：旋转数组不是整体有序，没法直接比 mid 和 target。但二分切一刀后，`[left, mid]` 和 `[mid, right]` **必有一半是有序的**——这是旋转数组唯一的突破口。先判哪半有序，再判 target 在不在有序区间，就能决定往哪边缩。这是唯一能在 O(log n) 解决的思路。

**如何套 + 变化点**：每次 mid 后，用 `nums[left] <= nums[mid]` 判左半是否有序；有序则看 target 在不在左半区间，不在则去右半；左半无序则右半必有序，对称处理。

```java
public int search(int[] nums, int target) {
    int left = 0, right = nums.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[left] <= nums[mid]) {              // 左半有序
            if (nums[left] <= target && target < nums[mid]) right = mid;
            else left = mid + 1;
        } else {                                    // 右半有序
            if (nums[mid] < target && target <= nums[right - 1]) left = mid + 1;
            else right = mid;
        }
    }
    return -1;
}
```

**易错点**：
- `nums[left] <= nums[mid]` 用 `<=`，**不是 `<`**。当 `left == mid`（区间只剩 1-2 个元素）时也视为左半有序；用 `<` 会漏判这种边界，进错分支。
- 判 target 在不在左半区间用 `nums[left] <= target && target < nums[mid]`，**右端点用 `<` 不是 `<=`**——`nums[mid]` 已经在上一行单独判过（== return），不该再含进区间比较。

---

## 练习建议

按类型分组：
- 标准模板 + 二分答案：1、5、6、8、9
- 左右边界：2（核心，必会）
- 旋转数组：3、4
- 压轴：10（二分划分数组，log(min(m,n))，面试最高难）

**如果时间只够做 3 道**：做 **2、3、10**——分别覆盖「找边界 / 旋转数组 / 双数组二分划分」三种最考功力的二分场景。1 和 5、6、8 是同一套标准模板的变体，会了 2 之后挑一道练手即可。

## 下一步

三道精讲覆盖了精确匹配 / 找边界 / 旋转数组三种二分；剩下 7 道的变化点已在表格列出。卡在某题时回看 [二分查找框架](../00-algorithm-frameworks/binary-search/)，对照「搜索区间 + 收缩分支 + 返回值」三处钩子，看这题改了哪一处。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
