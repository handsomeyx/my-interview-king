---
problems:
  - title: N 皇后
    url: https://leetcode.cn/problems/n-queens/
    difficulty: hard
---

# 搜索算法

搜索算法是解决问题的重要工具，包括二分搜索、深度优先搜索（DFS）、广度优先搜索（BFS）和回溯等。本章节将介绍这些搜索算法的原理和应用。

## 二分搜索

### 基本概念

二分搜索是一种在有序数组中查找特定元素的高效算法，时间复杂度为 O(log n)。

### 基本步骤

1. 确定搜索范围的左边界和右边界
2. 计算中间位置
3. 比较中间位置的元素与目标值
4. 根据比较结果缩小搜索范围
5. 重复步骤 2-4，直到找到目标值或搜索范围为空

### 应用场景

- 在有序数组中查找元素
- 查找第一个或最后一个满足条件的元素
- 寻找极值

### 代码实现

```python
def binary_search(nums, target):
    """
    二分搜索
    :param nums: 有序数组
    :param target: 目标值
    :return: 目标值的索引，若不存在返回 -1
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 深度优先搜索（DFS）

### 基本概念

深度优先搜索是一种优先探索深层节点的搜索算法，通常使用递归或栈实现。

### 应用场景

- 树的遍历
- 图的遍历
- 迷宫问题
- 组合问题

### 代码实现

```python
def dfs(graph, start, visited):
    """
    深度优先搜索
    :param graph: 图的邻接表
    :param start: 起始节点
    :param visited: 已访问节点集合
    """
    visited.add(start)
    print(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

## 广度优先搜索（BFS）

### 基本概念

广度优先搜索是一种优先探索浅层节点的搜索算法，通常使用队列实现。

### 应用场景

- 最短路径问题
- 层序遍历
- 寻找连通分量

### 代码实现

```python
def bfs(graph, start):
    """
    广度优先搜索
    :param graph: 图的邻接表
    :param start: 起始节点
    """
    visited = set()
    queue = [start]
    visited.add(start)
    
    while queue:
        node = queue.pop(0)
        print(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
```

## 回溯算法

### 基本概念

回溯算法是一种通过探索所有可能的解来找到所有解的算法，当探索到某一步时，如果发现该路径不能得到有效解，则回溯到上一步，尝试其他路径。

### 应用场景

- 排列问题
- 组合问题
- 子集问题
- 棋盘问题（如八皇后）

### 代码实现

```java
import java.util.*;

public class Solution {
    public void backtrack(int[] nums, int start, List<Integer> path, List<List<Integer>> result) {
        """
        回溯算法示例：生成所有子集
        :param nums: 输入数组
        :param start: 起始索引
        :param path: 当前路径
        :param result: 结果集
        """
        result.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.remove(path.size() - 1);
        }
    }
    
    // 使用示例
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }
}
```

## 总结

搜索算法是解决问题的重要工具，不同的搜索算法有不同的特点和适用场景：

- **二分搜索**：适合在有序数组中查找元素
- **深度优先搜索**：适合探索所有可能的解，如排列、组合问题
- **广度优先搜索**：适合寻找最短路径，如迷宫问题
- **回溯算法**：适合需要探索所有可能解的问题，如子集、排列问题

在实际应用中，应根据具体问题选择合适的搜索算法，以提高解决问题的效率。