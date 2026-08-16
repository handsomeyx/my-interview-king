---
problems:
  - title: 无重复字符的最长子串
    url: https://leetcode.cn/problems/longest-substring-without-repeating-characters/
    difficulty: medium
  - title: 最小覆盖子串
    url: https://leetcode.cn/problems/minimum-window-substring/
    difficulty: hard
  - title: 找到字符串中所有字母异位词
    url: https://leetcode.cn/problems/find-all-anagrams-in-a-string/
    difficulty: medium
  - title: 滑动窗口最大值
    url: https://leetcode.cn/problems/sliding-window-maximum/
    difficulty: hard
---

# 滑动窗口框架

## 思考锚点

滑动窗口的核心思想是「**在数组或字符串上维护一个动态区间**」，通过双指针（左右边界）的移动，高效地解决子数组/子串的问题。

为什么需要滑动窗口？因为很多子数组/子串问题如果用暴力解法，需要两层甚至三层循环，时间复杂度是 O(n²) 或 O(n³)。滑动窗口通过「**双指针同向移动**」，将时间复杂度降到 O(n)。

滑动窗口的关键在于「**什么时候扩大窗口、什么时候缩小窗口**」：
- 扩大窗口（移动右指针）：当窗口内的条件还不满足时
- 缩小窗口（移动左指针）：当窗口内的条件已经满足时，尝试缩小以找最优解

这个「扩大-满足-缩小」的循环是滑动窗口的本质。

## 算法原理

滑动窗口是一种用于解决子数组/子串问题的算法技巧。通过维护一个可变大小的窗口（连续的子数组或子串），在数组或字符串上滑动，以找到满足特定条件的解。

> 🤔 停下来想想：为什么滑动窗口能把 O(n²) 降到 O(n)？

## 框架模板

```java
public void slidingWindow(String s) {
    // 用于记录窗口内的字符及其出现次数
    Map<Character, Integer> window = new HashMap<>();
    int left = 0, right = 0;  // 窗口的左右边界
    int result = 0;            // 存储结果
    
    while (right < s.length()) {
        // 扩大窗口，将右边界的字符加入窗口
        char c = s.charAt(right);
        right++;
        // 更新窗口内的数据结构
        window.put(c, window.getOrDefault(c, 0) + 1);
        
        // 判断是否需要收缩窗口
        while (/* 窗口需要收缩的条件 */) {
            // 缩小窗口，将左边界的字符移出窗口
            char d = s.charAt(left);
            left++;
            // 更新窗口内的数据结构
            window.put(d, window.get(d) - 1);
            if (window.get(d) == 0) {
                window.remove(d);
            }
        }
        
        // 在这里更新结果
        result = Math.max(result, right - left);
    }
    
    // 返回结果
    return result;
}
```

## 适用场景

1. **最长无重复子串**：找到字符串中最长的无重复字符的子串
2. **最小覆盖子串**：找到包含目标字符串所有字符的最小子串
3. **滑动窗口最大值**：找到滑动窗口中的最大值
4. **子数组和问题**：找到和为目标值的连续子数组
5. **字符串排列**：判断字符串的排列是否是另一个字符串的子串

## 注意事项

1. **窗口大小**：窗口大小可以是固定的，也可以是可变的
2. **窗口移动**：当窗口不满足条件时，移动左边界；当窗口满足条件时，移动右边界
3. **数据结构**：根据具体问题选择合适的数据结构来记录窗口内的信息

> 🤔 停下来想想：什么时候该扩大窗口、什么时候该缩小？判断依据是什么？
4. **时间复杂度**：通常为 O(n)，其中 n 是数组或字符串的长度

## 示例：最长无重复子串

### 题目描述

给定一个字符串 `s`，找出其中不含有重复字符的**最长子串**的长度。

### 代码实现

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> window = new HashMap<>();
    int left = 0, right = 0;
    int result = 0;
    
    while (right < s.length()) {
        char c = s.charAt(right);
        right++;
        // 更新窗口
        window.put(c, window.getOrDefault(c, 0) + 1);
        
        // 判断是否需要收缩窗口
        while (window.get(c) > 1) {
            char d = s.charAt(left);
            left++;
            // 更新窗口
            window.put(d, window.get(d) - 1);
            if (window.get(d) == 0) {
                window.remove(d);
            }
        }
        
        // 更新结果
        result = Math.max(result, right - left);
    }
    
    return result;
}
```

### 解释

1. **初始化**：使用哈希表 `window` 记录窗口内的字符及其出现次数，左指针 `left` 和右指针 `right` 初始化为 0
2. **扩大窗口**：将右指针指向的字符加入窗口，更新哈希表
3. **判断是否需要收缩窗口**：如果窗口内有重复字符（当前字符的出现次数大于 1），则移动左指针，直到窗口内没有重复字符
4. **更新结果**：每次扩大窗口后，更新最长无重复子串的长度

## 示例：最小覆盖子串

### 题目描述

给定两个字符串 `s` 和 `t`，返回 `s` 中包含 `t` 所有字符的**最小子串**。如果 `s` 中不存在这样的子串，则返回空字符串。

### 代码实现

```java
public String minWindow(String s, String t) {
    // 记录 t 中字符的出现次数
    Map<Character, Integer> need = new HashMap<>();
    for (char c : t.toCharArray()) {
        need.put(c, need.getOrDefault(c, 0) + 1);
    }
    
    // 记录窗口内的字符及其出现次数
    Map<Character, Integer> window = new HashMap<>();
    int left = 0, right = 0;
    int valid = 0;  // 记录窗口中满足 need 条件的字符个数
    int start = 0, length = Integer.MAX_VALUE;  // 记录最小覆盖子串的起始位置和长度
    
    while (right < s.length()) {
        char c = s.charAt(right);
        right++;
        
        // 更新窗口
        if (need.containsKey(c)) {
            window.put(c, window.getOrDefault(c, 0) + 1);
            if (window.get(c).equals(need.get(c))) {
                valid++;
            }
        }
        
        // 判断是否需要收缩窗口
        while (valid == need.size()) {
            // 更新最小覆盖子串
            if (right - left < length) {
                start = left;
                length = right - left;
            }
            
            // 缩小窗口
            char d = s.charAt(left);
            left++;
            
            // 更新窗口
            if (need.containsKey(d)) {
                if (window.get(d).equals(need.get(d))) {
                    valid--;
                }
                window.put(d, window.get(d) - 1);
            }
        }
    }
    
    return length == Integer.MAX_VALUE ? "" : s.substring(start, start + length);
}
```

### 解释

1. **初始化**：使用哈希表 `need` 记录 `t` 中字符的出现次数，使用哈希表 `window` 记录窗口内的字符及其出现次数，`valid` 记录窗口中满足 `need` 条件的字符个数
2. **扩大窗口**：将右指针指向的字符加入窗口，更新哈希表和 `valid` 值
3. **判断是否需要收缩窗口**：当窗口满足 `need` 条件时（`valid == need.size()`），尝试收缩窗口以找到最小覆盖子串
4. **更新结果**：每次收缩窗口前，更新最小覆盖子串的起始位置和长度

## 总结

滑动窗口是一种非常有效的算法技巧，适用于解决各种子数组和子串问题。通过掌握这个框架，你可以快速解决许多常见的算法问题，提高解题效率。

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：滑动窗口的核心思想是什么？它为什么能将时间复杂度降到 O(n)？

2. **讲给初学者听**：怎么用「图书馆占座」来类比滑动窗口？当人进来（扩大窗口）和离开（缩小窗口）时，窗口如何变化？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如如何用滑动窗口解决「最小覆盖子串」问题？固定长度和可变长度窗口的区别是什么？）