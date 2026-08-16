---
problems:
  - title: 两数之和
    url: https://leetcode.cn/problems/two-sum/
    difficulty: easy
  - title: 三数之和
    url: https://leetcode.cn/problems/3sum/
    difficulty: medium
  - title: 最长连续递增序列
    url: https://leetcode.cn/problems/longest-continuous-increasing-subsequence/
    difficulty: easy
  - title: 和为 K 的子数组
    url: https://leetcode.cn/problems/subarray-sum-equals-k/
    difficulty: medium
  - title: 寻找重复数
    url: https://leetcode.cn/problems/find-the-duplicate-number/
    difficulty: medium
  - title: 数组中的第 K 个最大元素
    url: https://leetcode.cn/problems/kth-largest-element-in-an-array/
    difficulty: medium
  - title: 合并区间
    url: https://leetcode.cn/problems/merge-intervals/
    difficulty: medium
  - title: 缺失的第一个正数
    url: https://leetcode.cn/problems/first-missing-positive/
    difficulty: hard
  - title: 螺旋矩阵
    url: https://leetcode.cn/problems/spiral-matrix/
    difficulty: medium
  - title: 接雨水
    url: https://leetcode.cn/problems/trapping-rain-water/
    difficulty: hard
---

# 数组类 Top 题

数组是最基础的数据结构之一，也是面试中最常见的考点。本文将介绍数组类的高频面试题，包括数组的基本操作、双指针技巧、滑动窗口等。

## 1. 两数之和

### 题目描述

给定一个整数数组 `nums` 和一个目标值 `target`，请你在该数组中找出和为目标值的那两个整数，并返回它们的数组下标。

### 示例

```
输入：nums = [2, 7, 11, 15], target = 9
输出：[0, 1]
解释：因为 nums[0] + nums[1] = 2 + 7 = 9，所以返回 [0, 1]。
```

### 解题思路

- **暴力解法**：双重循环，时间复杂度 O(n²)
- **哈希表**：使用哈希表存储已经遍历过的元素及其下标，时间复杂度 O(n)

### 代码实现

```java
import java.util.HashMap;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        // 使用哈希表存储已经遍历过的元素及其下标
        HashMap<Integer, Integer> hashMap = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (hashMap.containsKey(complement)) {
                return new int[] {hashMap.get(complement), i};
            }
            hashMap.put(nums[i], i);
        }
        return new int[0];
    }
}

// 测试示例
// 输入: nums = [2, 7, 11, 15], target = 9
// 输出: [0, 1]
```

<div class="question-card" data-id="three-sum">
  <h2 class="question-title">2. 三数之和</h2>
  <div class="question-tags">
    <span class="question-tag">算法</span>
    <span class="question-tag">数组</span>
    <span class="question-tag">双指针</span>
    <span class="question-tag">排序</span>
    <span class="question-tag">高频</span>
  </div>
  <div class="question-content">
    <h3>题目描述</h3>
    <p>给你一个包含 n 个整数的数组 <code>nums</code>，判断 <code>nums</code> 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。</p>
    
    <h3>示例</h3>

```
输入：nums = [-1, 0, 1, 2, -1, -4]
输出：[[-1, 0, 1], [-1, -1, 2]]
```
    
    <h3>解题思路</h3>
    <ul>
      <li><strong>排序 + 双指针</strong>：先对数组排序，然后固定一个元素，使用双指针寻找另外两个元素</li>
      <li><strong>去重</strong>：需要注意避免重复的三元组</li>
    </ul>
    
    <h3>代码实现</h3>

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums);
        int n = nums.length;
        
        for (int i = 0; i < n; i++) {
            // 避免重复
            if (i > 0 && nums[i] == nums[i-1]) {
                continue;
            }
            
            int left = i + 1;
            int right = n - 1;
            
            while (left < right) {
                int total = nums[i] + nums[left] + nums[right];
                if (total == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    // 避免重复
                    while (left < right && nums[left] == nums[left+1]) {
                        left++;
                    }
                    while (left < right && nums[right] == nums[right-1]) {
                        right--;
                    }
                    left++;
                    right--;
                } else if (total < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        
        return result;
    }
}
```

  </div>
  <div class="question-actions">
    <button class="action-btn" data-action="favorite">⭐ 收藏</button>
    <button class="action-btn" data-action="wrong">❌ 错题本</button>
  </div>
</div>

## 3. 最长连续递增序列

### 题目描述

给定一个未经排序的整数数组，找到最长且连续的的递增序列。

### 示例

```
输入：nums = [1,3,5,4,7]
输出：3
解释：最长连续递增序列是 [1,3,5], 长度为 3。
虽然 [1,3,5,7] 也是升序的子序列, 但它不是连续的，因为 5 和 7 在原数组里被 4 隔开。
```

### 解题思路

- **一次遍历**：遍历数组，记录当前连续递增序列的长度，更新最长长度

### 代码实现

```java
class Solution {
    public int findLengthOfLCIS(int[] nums) {
        if (nums == null || nums.length == 0) {
            return 0;
        }
        
        int maxLength = 1;
        int currentLength = 1;
        
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > nums[i-1]) {
                currentLength++;
                maxLength = Math.max(maxLength, currentLength);
            } else {
                currentLength = 1;
            }
        }
        
        return maxLength;
    }
}

// 测试示例
// 输入: nums = [1,3,5,4,7]
// 输出: 3
// 输入: nums = [2,2,2,2,2]
// 输出: 1
```

## 4. 最长子数组和为 k

### 题目描述

给定一个整数数组和一个整数 k，你需要找到该数组中和为 k 的最长连续子数组的长度。

### 示例

```
输入：nums = [1, -1, 5, -2, 3], k = 3
输出：4
解释：子数组 [1, -1, 5, -2] 的和为 3，长度为 4。
```

### 解题思路

- **前缀和 + 哈希表**：使用哈希表存储前缀和及其出现的位置

### 代码实现

```java
import java.util.HashMap;

class Solution {
    public int maxSubArrayLen(int[] nums, int k) {
        int prefixSum = 0;
        int maxLength = 0;
        // 哈希表存储前缀和及其出现的最早位置
        HashMap<Integer, Integer> sumMap = new HashMap<>();
        sumMap.put(0, -1);
        
        for (int i = 0; i < nums.length; i++) {
            prefixSum += nums[i];
            if (sumMap.containsKey(prefixSum - k)) {
                maxLength = Math.max(maxLength, i - sumMap.get(prefixSum - k));
            }
            if (!sumMap.containsKey(prefixSum)) {
                sumMap.put(prefixSum, i);
            }
        }
        
        return maxLength;
    }
}

// 测试示例
// 输入: nums = [1, -1, 5, -2, 3], k = 3
// 输出: 4
// 输入: nums = [-2, -1, 2, 1], k = 1
// 输出: 2
```

## 5. 寻找重复数

### 题目描述

给定一个包含 n + 1 个整数的数组 nums，其数字都在 1 到 n 之间（包括 1 和 n），可知至少存在一个重复的整数。假设只有一个重复的整数，找出这个重复的数。

### 示例

```
输入：nums = [1,3,4,2,2]
输出：2
```

### 解题思路

- **二分查找**：利用抽屉原理，统计数组中小于等于 mid 的元素个数
- **快慢指针**：将问题转化为链表环的问题

### 代码实现

```java
class Solution {
    public int findDuplicate(int[] nums) {
        // 快慢指针
        int slow = nums[0];
        int fast = nums[nums[0]];
        
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[nums[fast]];
        }
        
        // 找到环的入口
        fast = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        
        return slow;
    }
}

// 测试示例
// 输入: nums = [1,3,4,2,2]
// 输出: 2
// 输入: nums = [3,1,3,4,2]
// 输出: 3
```

## 6. 数组中的第K个最大元素

### 题目描述

在未排序的数组中找到第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

### 示例

```
输入：[3,2,1,5,6,4] 和 k = 2
输出：5
```

### 解题思路

- **排序**：直接排序后取第 k 个元素，时间复杂度 O(n log n)
- **堆**：使用小顶堆，时间复杂度 O(n log k)
- **快速选择**：基于快速排序的思想，时间复杂度 O(n)

### 代码实现

```java
import java.util.PriorityQueue;

class Solution {
    public int findKthLargest(int[] nums, int k) {
        // 使用小顶堆
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int num : nums) {
            heap.offer(num);
            if (heap.size() > k) {
                heap.poll();
            }
        }
        return heap.peek();
    }
}

// 测试示例
// 输入: nums = [3,2,1,5,6,4], k = 2
// 输出: 5
// 输入: nums = [3,2,3,1,2,4,5,5,6], k = 4
// 输出: 4
```

## 7. 合并区间

### 题目描述

给出一个区间的集合，请合并所有重叠的区间。

### 示例

```
输入：[[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠，将它们合并为 [1,6].
```

### 解题思路

- **排序**：按区间的起始位置排序，然后遍历合并

### 代码实现

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public int[][] merge(int[][] intervals) {
        if (intervals == null || intervals.length == 0) {
            return new int[0][];
        }
        
        // 按区间的起始位置排序
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        List<int[]> merged = new ArrayList<>();
        merged.add(intervals[0]);
        
        for (int i = 1; i < intervals.length; i++) {
            int[] last = merged.get(merged.size() - 1);
            int[] current = intervals[i];
            if (current[0] <= last[1]) {
                // 重叠，合并
                last[1] = Math.max(last[1], current[1]);
            } else {
                // 不重叠，添加新区间
                merged.add(current);
            }
        }
        
        return merged.toArray(new int[merged.size()][]);
    }
}

// 测试示例
// 输入: intervals = [[1,3],[2,6],[8,10],[15,18]]
// 输出: [[1, 6], [8, 10], [15, 18]]
// 输入: intervals = [[1,4],[4,5]]
// 输出: [[1, 5]]
```

## 8. 缺失的第一个正数

### 题目描述

给你一个未排序的整数数组，请你找出其中没有出现的最小的正整数。

### 示例

```
输入：[1,2,0]
输出：3

输入：[3,4,-1,1]
输出：2

输入：[7,8,9,11,12]
输出：1
```

### 解题思路

- **原地哈希**：将数组视为哈希表，将每个元素放到其对应的位置

### 代码实现

```java
class Solution {
    public int firstMissingPositive(int[] nums) {
        int n = nums.length;
        
        // 将每个元素放到其对应的位置
        for (int i = 0; i < n; i++) {
            while (1 <= nums[i] && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                // 交换元素
                int temp = nums[nums[i] - 1];
                nums[nums[i] - 1] = nums[i];
                nums[i] = temp;
            }
        }
        
        // 找到第一个缺失的正整数
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) {
                return i + 1;
            }
        }
        
        return n + 1;
    }
}

// 测试示例
// 输入: nums = [1,2,0]
// 输出: 3
// 输入: nums = [3,4,-1,1]
// 输出: 2
// 输入: nums = [7,8,9,11,12]
// 输出: 1
```

## 9. 螺旋矩阵

### 题目描述

给定一个包含 m x n 个元素的矩阵（m 行, n 列），请按照顺时针螺旋顺序，返回矩阵中的所有元素。

### 示例

```
输入：
[  [ 1, 2, 3 ],  [ 4, 5, 6 ],  [ 7, 8, 9 ]]
输出：[1,2,3,6,9,8,7,4,5]
```

### 解题思路

- **模拟**：模拟螺旋遍历的过程，定义四个边界

### 代码实现

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        if (matrix == null || matrix.length == 0) {
            return result;
        }
        
        int top = 0;
        int bottom = matrix.length - 1;
        int left = 0;
        int right = matrix[0].length - 1;
        
        while (top <= bottom && left <= right) {
            // 从左到右
            for (int i = left; i <= right; i++) {
                result.add(matrix[top][i]);
            }
            top++;
            
            // 从上到下
            for (int i = top; i <= bottom; i++) {
                result.add(matrix[i][right]);
            }
            right--;
            
            // 从右到左
            if (top <= bottom) {
                for (int i = right; i >= left; i--) {
                    result.add(matrix[bottom][i]);
                }
                bottom--;
            }
            
            // 从下到上
            if (left <= right) {
                for (int i = bottom; i >= top; i--) {
                    result.add(matrix[i][left]);
                }
                left++;
            }
        }
        
        return result;
    }
}

// 测试示例
// 输入: matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
// 输出: [1, 2, 3, 6, 9, 8, 7, 4, 5]
// 输入: matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
// 输出: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
```

## 10. 接雨水

### 题目描述

给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

### 示例

```
输入：[0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
```

### 解题思路

- **双指针**：从两端向中间遍历，记录左右最大值
- **单调栈**：使用单调栈存储柱子的索引

### 代码实现

```java
class Solution {
    public int trap(int[] height) {
        if (height == null || height.length == 0) {
            return 0;
        }
        
        int left = 0;
        int right = height.length - 1;
        int leftMax = 0;
        int rightMax = 0;
        int result = 0;
        
        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left];
                } else {
                    result += leftMax - height[left];
                }
                left++;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    result += rightMax - height[right];
                }
                right--;
            }
        }
        
        return result;
    }
}

// 测试示例
// 输入: height = [0,1,0,2,1,0,1,3,2,1,2,1]
// 输出: 6
// 输入: height = [4,2,0,3,2,5]
// 输出: 9
```

## 总结

数组类的高频面试题主要包括：

1. **基本操作**：两数之和、三数之和、最长连续递增序列
2. **前缀和**：最长子数组和为 k
3. **查找**：寻找重复数、数组中的第K个最大元素
4. **区间处理**：合并区间
5. **原地操作**：缺失的第一个正数
6. **矩阵操作**：螺旋矩阵
7. **双指针**：接雨水

这些题目涵盖了数组的常见操作和技巧，掌握这些题目对于应对面试中的数组相关问题非常有帮助。