---
problems:
  - title: 二分查找
    url: https://leetcode.cn/problems/binary-search/
    difficulty: easy
  - title: 搜索旋转排序数组
    url: https://leetcode.cn/problems/search-in-rotated-sorted-array/
    difficulty: medium
  - title: 查找元素的第一个和最后一个位置
    url: https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/
    difficulty: medium
---

# 二分查找框架

## 思考锚点

二分查找的核心前提是「有序」。如果数据无序，二分就无从谈起。所以当你遇到一道有序数组的查找题时，二分应该是你的第一反应。

二分的本质是「**缩小搜索空间**」——每次比较后，你可以确定目标值只可能在左半或右半，从而把搜索范围减半。时间复杂度从 O(n) 降到 O(log n)，这是质的飞跃。

但二分的难点在于「**边界处理**」：循环条件是 `left <= right` 还是 `left < right`？边界更新是 `left = mid + 1` 还是 `left = mid`？这些细节决定了你能不能写对。

学习二分的关键：**理解「搜索空间」在每一步的变化，而不是死记硬背模板**。

## 算法原理

二分查找是一种在有序数组中查找特定元素的高效算法。它的基本思想是：

1. 将查找区间分为两部分
2. 比较中间元素与目标值
3. 根据比较结果缩小查找区间
4. 重复上述过程，直到找到目标值或确定目标值不存在

## 框架模板

```java
public int binarySearch(int[] nums, int target) {
    int left = 0;
    int right = nums.length - 1;
    
    while (left <= right) {
        // 计算中间位置，避免溢出
        int mid = left + (right - left) / 2;
        
        if (nums[mid] == target) {
            // 找到目标值，返回索引
            return mid;
        } else if (nums[mid] < target) {
            // 目标值在右半部分，更新左边界
            left = mid + 1;
        } else {
            // 目标值在左半部分，更新右边界
            right = mid - 1;
        }
    }
    
    // 目标值不存在，返回 -1
    return -1;
}
```

## 适用场景

1. **有序数组的查找**：二分查找要求数组是有序的
2. **范围查找**：如查找第一个大于等于目标值的元素
3. **旋转排序数组的查找**：如查找旋转排序数组中的最小值
4. **二分答案**：在可能的答案范围内进行二分查找，如求平方根

## 注意事项

1. **边界条件**：注意循环条件是 `left <= right` 还是 `left < right`
2. **中间位置计算**：使用 `mid = left + (right - left) / 2` 避免整数溢出
3. **边界更新**：注意左边界和右边界的更新方式，避免死循环
4. **重复元素**：如果数组中有重复元素，需要根据具体问题调整查找策略

## 示例：二分查找

### 题目描述

给定一个有序数组 `nums` 和一个目标值 `target`，返回 `target` 在数组中的索引。如果 `target` 不存在于数组中，返回 -1。

### 代码实现

```java
public int search(int[] nums, int target) {
    int left = 0;
    int right = nums.length - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}
```

### 解释

1. **初始化边界**：左边界 `left` 初始化为 0，右边界 `right` 初始化为数组长度减 1
2. **循环查找**：当左边界小于等于右边界时，继续查找
   - 计算中间位置 `mid`
   - 如果中间元素等于目标值，返回中间位置
   - 如果中间元素小于目标值，说明目标值在右半部分，更新左边界为 `mid + 1`
   - 如果中间元素大于目标值，说明目标值在左半部分，更新右边界为 `mid - 1`
3. **返回结果**：如果循环结束仍未找到目标值，返回 -1

## 示例：查找第一个大于等于目标值的元素

### 题目描述

给定一个有序数组 `nums` 和一个目标值 `target`，返回第一个大于等于 `target` 的元素的索引。如果不存在这样的元素，返回数组长度。

### 代码实现

```java
public int findFirstGreaterOrEqual(int[] nums, int target) {
    int left = 0;
    int right = nums.length;
    
    while (left < right) {
        int mid = left + (right - left) / 2;
        
        if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    return left;
}
```

### 解释

1. **初始化边界**：左边界 `left` 初始化为 0，右边界 `right` 初始化为数组长度
2. **循环查找**：当左边界小于右边界时，继续查找
   - 计算中间位置 `mid`
   - 如果中间元素小于目标值，说明第一个大于等于目标值的元素在右半部分，更新左边界为 `mid + 1`
   - 否则，说明第一个大于等于目标值的元素在左半部分或就是中间元素，更新右边界为 `mid`
3. **返回结果**：当循环结束时，左边界 `left` 就是第一个大于等于目标值的元素的索引

## 示例：旋转排序数组的查找

### 题目描述

假设按照升序排序的数组在预先未知的某个点上进行了旋转。例如，数组 `[0,1,2,4,5,6,7]` 可能变为 `[4,5,6,7,0,1,2]`。

给定一个旋转排序数组 `nums` 和一个目标值 `target`，返回 `target` 在数组中的索引。如果 `target` 不存在于数组中，返回 -1。

### 代码实现

```java
public int search(int[] nums, int target) {
    int left = 0;
    int right = nums.length - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (nums[mid] == target) {
            return mid;
        }
        
        // 判断左半部分是否有序
        if (nums[left] <= nums[mid]) {
            // 左半部分有序
            if (target >= nums[left] && target < nums[mid]) {
                // 目标值在左半部分
                right = mid - 1;
            } else {
                // 目标值在右半部分
                left = mid + 1;
            }
        } else {
            // 右半部分有序
            if (target > nums[mid] && target <= nums[right]) {
                // 目标值在右半部分
                left = mid + 1;
            } else {
                // 目标值在左半部分
                right = mid - 1;
            }
        }
    }
    
    return -1;
}
```

### 解释

1. **初始化边界**：左边界 `left` 初始化为 0，右边界 `right` 初始化为数组长度减 1
2. **循环查找**：当左边界小于等于右边界时，继续查找
   - 计算中间位置 `mid`
   - 如果中间元素等于目标值，返回中间位置
   - 判断左半部分是否有序
     - 如果左半部分有序，检查目标值是否在左半部分
     - 如果右半部分有序，检查目标值是否在右半部分
   - 根据检查结果更新边界
3. **返回结果**：如果循环结束仍未找到目标值，返回 -1

## 总结

二分查找是一种高效的查找算法，时间复杂度为 O(log n)，适用于有序数组的查找问题。通过掌握二分查找的框架，你可以解决各种变体问题，如范围查找、旋转排序数组的查找等。在实际应用中，需要注意边界条件的处理和中间位置的计算，以避免错误。

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：二分查找的核心思想是什么？为什么它的时间复杂度是 O(log n)？

2. **讲给初学者听**：怎么用「猜数字游戏」来类比二分查找？为什么每次都能排除一半的可能性？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如二分查找的 `left <= right` 和 `left < right` 两种写法有什么区别？如何用二分查找找「第一个大于等于目标值的位置」？）