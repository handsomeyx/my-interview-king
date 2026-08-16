---
problems:
  - title: 两数之和 II - 输入有序数组
    url: https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/
    difficulty: medium
  - title: 盛最多水的容器
    url: https://leetcode.cn/problems/container-with-most-water/
    difficulty: medium
  - title: 验证回文串
    url: https://leetcode.cn/problems/valid-palindrome/
    difficulty: easy
  - title: 移除元素
    url: https://leetcode.cn/problems/remove-element/
    difficulty: easy
  - title: 接雨水
    url: https://leetcode.cn/problems/trapping-rain-water/
    difficulty: hard
---

# 左右指针框架

## 算法原理

左右指针是一种双指针技巧，通常用于处理数组或字符串的双向遍历问题。通过维护两个指针（左指针和右指针），从数组的两端向中间移动，直到满足特定条件。

## 框架模板

```java
public void twoPointers(int[] nums) {
    int left = 0;           // 左指针初始化为数组起点
    int right = nums.length - 1;  // 右指针初始化为数组终点
    
    while (left < right) {    // 当左指针小于右指针时循环
        // 根据具体问题逻辑处理当前指针位置的元素
        if (/* 条件判断 */) {
            // 满足条件，移动左指针或右指针
            left++;  // 或 right--
        } else {
            // 不满足条件，移动另一个指针
            right--;  // 或 left++
        }
    }
    // 循环结束，处理结果
}
```

## 适用场景

1. **有序数组的两数之和**：在有序数组中找到两个数之和等于目标值
2. **回文串判断**：判断一个字符串是否为回文
3. **反转数组**：将数组元素反转
4. **移除元素**：移除数组中指定值的元素
5. **盛最多水的容器**：找到可以盛最多水的容器

## 注意事项

1. **循环条件**：通常是 `left < right`，确保指针不会交叉
2. **指针移动**：根据具体问题逻辑，决定移动左指针还是右指针
3. **边界处理**：注意数组的边界情况，避免越界访问
4. **时间复杂度**：通常为 O(n)，其中 n 是数组长度

## 示例：两数之和 II - 输入有序数组

### 题目描述

给定一个已按照**升序排列**的整数数组 `numbers`，请你从数组中找出两个数，使得它们的和等于目标值 `target`。

### 代码实现

```java
public int[] twoSum(int[] numbers, int target) {
    int left = 0;
    int right = numbers.length - 1;
    
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) {
            // 返回索引（注意题目要求的索引是从1开始）
            return new int[]{left + 1, right + 1};
        } else if (sum < target) {
            // 和小于目标值，移动左指针
            left++;
        } else {
            // 和大于目标值，移动右指针
            right--;
        }
    }
    // 题目保证有解，所以不会执行到这里
    return new int[]{-1, -1};
}
```

### 解释

1. **初始化指针**：左指针指向数组起点，右指针指向数组终点
2. **计算和**：计算左右指针指向元素的和
3. **判断和与目标值的关系**：
   - 如果和等于目标值，返回结果
   - 如果和小于目标值，移动左指针（增大和）
   - 如果和大于目标值，移动右指针（减小和）
4. **循环直到找到解**：由于题目保证有解，循环会在找到解后结束

## 示例：回文串判断

### 题目描述

判断一个字符串是否为回文串。回文串是指正着读和倒着读都一样的字符串。

### 代码实现

```java
public boolean isPalindrome(String s) {
    // 预处理：将字符串转换为小写并去除非字母数字字符
    s = s.toLowerCase().replaceAll("[^a-z0-9]", "");
    
    int left = 0;
    int right = s.length() - 1;
    
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
```

### 解释

1. **预处理**：将字符串转换为小写并去除非字母数字字符
2. **初始化指针**：左指针指向字符串起点，右指针指向字符串终点
3. **比较字符**：比较左右指针指向的字符
   - 如果不相等，返回 false
   - 如果相等，移动左右指针向中间靠拢
4. **循环结束**：如果所有字符都比较完毕且相等，返回 true

## 总结

左右指针是一种非常实用的算法技巧，适用于多种数组和字符串问题。通过掌握这个框架，你可以快速解决许多常见的算法问题，提高解题效率。