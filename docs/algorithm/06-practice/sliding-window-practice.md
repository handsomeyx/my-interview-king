---
title: 滑动窗口专项练习
---

# 滑动窗口专项练习

> 配套框架：[滑动窗口框架](../00-algorithm-frameworks/sliding-window/)。滑动窗口的所有题，区别只有三处：**什么时候收缩、什么时候更新结果、结果怎么定义**。下面精讲 3 道覆盖三种典型收缩语义，再给 7 道变化点清单自己练。每题只改那三处。

## 框架速记

```text
while (right 未到末尾) {
    右扩：把 s[right] 加入窗口
    right++
    while (窗口需要收缩) {     // ← 各题在这里写不同条件
        左缩：把 s[left] 移出窗口
        left++
    }
    在这里更新结果             // ← 各题在这里写不同统计
}
```

记住三个钩子：**收缩条件、更新位置、结果定义**。每题只改这三处。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点（钩子怎么改） |
|---|---|---|---|
| 1 | [无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/) | 中 | 收缩：当前字符计数 > 1；结果：最长 |
| 2 | [找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/) | 中 | 固定窗口（=p 长度），逐位比计数 |
| 3 | [最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/) | 困 | 收缩：valid 已满足；结果：最短 |
| 4 | [字符串的排列](https://leetcode.cn/problems/permutation-in-string/) | 中 | 固定窗口，同 2 的计数比对 |
| 5 | [替换后的最长重复字符](https://leetcode.cn/problems/longest-repeating-character-replacement/) | 中 | 收缩：窗口长 - 最多字符数 > k |
| 6 | [长度最小的子数组](https://leetcode.cn/problems/minimum-size-subarray-sum/) | 中 | 收缩：sum ≥ target；结果：最短 |
| 7 | [滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/) | 困 | 单调队列维护窗口最大值 |
| 8 | [乘积小于 K 的子数组](https://leetcode.cn/problems/subarray-product-less-than-k/) | 中 | 收缩：prod ≥ k；结果：ans += r-l+1 |
| 9 | [最大连续 1 的个数 III](https://leetcode.cn/problems/max-consecutive-ones-iii/) | 中 | 容忍窗口内最多 k 个 0 |
| 10 | [存在重复元素 II](https://leetcode.cn/problems/contains-duplicate-ii/) | 简 | 固定窗口 + 集合查重 |

---

## 例题 1：无重复字符的最长子串（LC 3，基础）

**题目**：给定字符串 `s`，找不含重复字符的最长子串的长度。

**如何套 + 变化点**：标准可变窗口，右扩字符进窗口，窗口内出现重复（当前字符计数 > 1）就左缩到无重复，结果在每次右扩后取最长。这里收缩条件是「当前字符计数 > 1」——因为 `merge` 已经把当前字符 +1 了，`> 1` 才表示「加入后出现重复」。

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> window = new HashMap<>();
    int left = 0, right = 0, result = 0;
    while (right < s.length()) {
        char c = s.charAt(right);
        right++;
        window.merge(c, 1, Integer::sum);
        while (window.get(c) > 1) {        // 收缩条件：当前字符重复
            char d = s.charAt(left);
            left++;
            window.merge(d, -1, Integer::sum);
        }
        result = Math.max(result, right - left);  // 更新结果：最长
    }
    return result;
}
```

**易错点**：
- 收缩条件写 `window.get(c) > 1`，**不是 `>= 1`**。`merge` 已把当前字符计数 +1，写 `>= 1` 会让每个字符一进来就触发收缩，窗口永远为空，永远返回 0。
- 顺序必须**先 `right++`、先 `merge` 计数，再判断收缩**。如果先判断 `window.get(c) > 1` 再 `merge`，此时计数还没 +1，刚加入的字符会被漏判。

---

## 例题 2：最小覆盖子串（LC 76，进阶）

**题目**：给定字符串 `s` 和 `t`，返回 `s` 中涵盖 `t` 所有字符的最小子串。

**如何套 + 变化点**：仍是可变窗口，但「何时收缩」变了——窗口涵盖了 `t` 全部字符时才收缩（为了找更短）。用 `valid` 记录「窗口里满足 `t` 需求的字符种类数」，收缩条件 `valid == need.size()`，结果在收缩**前**取最短。

```java
public String minWindow(String s, String t) {
    Map<Character, Integer> need = new HashMap<>(), window = new HashMap<>();
    for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);

    int left = 0, right = 0, valid = 0;
    int start = 0, len = Integer.MAX_VALUE;

    while (right < s.length()) {
        char c = s.charAt(right);
        right++;
        if (need.containsKey(c)) {
            window.merge(c, 1, Integer::sum);
            if (window.get(c).equals(need.get(c))) valid++;
        }
        while (valid == need.size()) {       // 收缩条件：已涵盖 t 全部字符
            if (right - left < len) {        // 更新结果：最短
                start = left;
                len = right - left;
            }
            char d = s.charAt(left);
            left++;
            if (need.containsKey(d)) {
                if (window.get(d).equals(need.get(d))) valid--;
                window.merge(d, -1, Integer::sum);
            }
        }
    }
    return len == Integer.MAX_VALUE ? "" : s.substring(start, start + len);
}
```

**易错点**：
- `valid` 增减规则最容易写错。**只有某字符计数「刚好等于」需求时 `valid++`**；**只有某字符原本相等、即将变少时 `valid--`**。判断条件颠倒会漏统计或重复统计。
- 收缩内层的顺序：**先判 `valid--` 的条件，再 `merge -1`**。如果先 `merge` 再判，`window.get(d)` 已经变小，「原本是否相等」的判断失真，`valid` 漏减。

**对比**：例 1 收缩是因为「窗口里有了重复」，例 2 收缩是因为「窗口已经满足需求、想找更短的」。同一个框架，收缩语义不同。

---

## 例题 3：滑动窗口最大值（LC 239，变式）

**题目**：给定数组和窗口大小 `k`，返回每个窗口里的最大值。

**为什么必须单调队列**：暴力做法是每个窗口扫 `k` 个元素取 max，复杂度 `O(n·k)`。`n=10^5`、`k=10^3` 时直接 10^8，必超时。这道题的难点不在「扩/缩」，而在「O(1) 取窗口最大值」——必须换数据结构。单调队列（双端队列）就是干这个的。

**如何套 + 变化点**：单调队列存索引（对应值单调递减），队首永远是当前窗口最大值。右扩时弹出队尾所有比新元素小的；左缩时若队首索引已出窗口就弹出。

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] res = new int[n - k + 1];
    Deque<Integer> dq = new ArrayDeque<>();   // 存索引，对应值单调递减
    for (int i = 0; i < n; i++) {
        // 右扩：维护单调性
        while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
        dq.offerLast(i);
        // 左缩：队首索引出窗口则弹出
        while (dq.peekFirst() <= i - k) dq.pollFirst();
        // 更新结果：窗口成型后记队首
        if (i >= k - 1) res[i - k + 1] = nums[dq.peekFirst()];
    }
    return res;
}
```

**易错点**：
- 单调队列**存索引、不存值**。存值会丢失「队首是否过期」的信息，没法判断该不该弹出。
- 边界 `dq.peekFirst() <= i - k` 用 `<=`，**不是 `<`**。`<=` 表示「队首索引 ≤ i-k，已不在窗口内」；写 `<` 会让 `i-k` 那个临界索引残留，最大值可能取到窗口外元素。

---

## 练习建议

按类型分组：
- 可变窗口，练收缩条件：1、6、9
- 固定窗口：2、4、10
- 进阶：3（valid 计数）、5（容忍 k）、8（计数法 `ans += r-l+1`）
- 压轴：7（单调队列）

**如果时间只够做 3 道**：做 **1、3、7**——分别覆盖「重复收缩 / 满足收缩 / 单调队列」三种完全不同的收缩语义，做完滑动窗口的主干就拿下了，其余题都是这三种的变体。

## 下一步

三道精讲覆盖了三种收缩语义；剩下 7 道的变化点已在表格列出，按需练。卡在某题时回看 [滑动窗口框架](../00-algorithm-frameworks/sliding-window/) 的三处钩子，对照「这题改了哪一处」。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
