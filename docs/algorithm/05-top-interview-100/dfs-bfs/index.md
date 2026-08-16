---
problems:
  - title: 二叉树的层序遍历
    url: https://leetcode.cn/problems/binary-tree-level-order-traversal/
    difficulty: medium
  - title: 二叉树的最大深度
    url: https://leetcode.cn/problems/maximum-depth-of-binary-tree/
    difficulty: easy
  - title: 路径总和
    url: https://leetcode.cn/problems/path-sum/
    difficulty: easy
  - title: 岛屿数量
    url: https://leetcode.cn/problems/number-of-islands/
    difficulty: medium
  - title: 单词搜索
    url: https://leetcode.cn/problems/word-search/
    difficulty: medium
---

# DFS/BFS Top 题

深度优先搜索（DFS）和广度优先搜索（BFS）是两种常用的搜索算法，在解决树、图等结构的问题时非常有效。本章节将介绍一些高频的DFS/BFS面试题。

## 1. 二叉树的层序遍历

### 题目描述
给你一个二叉树，请你返回其按层序遍历得到的节点值。 （即逐层地，从左到右访问所有节点）。

### 解题思路
- 使用队列实现广度优先搜索
- 每次遍历一层节点，将它们的子节点加入队列
- 记录每一层的节点值

### 代码实现

```java
import java.util.*;

public class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) {
            return result;
        }
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) {
                    queue.offer(node.left);
                }
                if (node.right != null) {
                    queue.offer(node.right);
                }
            }
            result.add(level);
        }
        return result;
    }
}

// 二叉树节点定义
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}
```

## 2. 二叉树的最大深度

### 题目描述
给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

### 解题思路
- 使用深度优先搜索
- 递归计算左子树和右子树的深度，取最大值加1

### 代码实现

```java
public class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);
        return Math.max(leftDepth, rightDepth) + 1;
    }
}

// 二叉树节点定义
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}
```

## 3. 路径总和

### 题目描述
给你二叉树的根节点 `root` 和一个表示目标和的整数 `targetSum` ，判断该树中是否存在 根节点到叶子节点 的路径，这条路径上所有节点值相加等于目标和 `targetSum` 。

### 解题思路
- 使用深度优先搜索
- 从根节点开始，递归遍历左右子树，同时更新当前路径的和
- 当到达叶子节点时，检查当前和是否等于目标和

### 代码实现

```java
public class Solution {
    public boolean hasPathSum(TreeNode root, int targetSum) {
        if (root == null) {
            return false;
        }
        if (root.left == null && root.right == null) {
            return root.val == targetSum;
        }
        return hasPathSum(root.left, targetSum - root.val) || hasPathSum(root.right, targetSum - root.val);
    }
}

// 二叉树节点定义
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}
```

## 4. 岛屿数量

### 题目描述
给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

### 解题思路
- 使用深度优先搜索
- 遍历网格，当遇到 '1' 时，进行 DFS 遍历，将所有相连的 '1' 标记为 '0'，并增加岛屿计数

### 代码实现

```java
public class Solution {
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) {
            return 0;
        }
        int count = 0;
        int m = grid.length;
        int n = grid[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }
    
    private void dfs(char[][] grid, int i, int j) {
        int m = grid.length;
        int n = grid[0].length;
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] == '0') {
            return;
        }
        grid[i][j] = '0';
        dfs(grid, i - 1, j); // 上
        dfs(grid, i + 1, j); // 下
        dfs(grid, i, j - 1); // 左
        dfs(grid, i, j + 1); // 右
    }
}
```

## 5. 单词搜索

### 题目描述
给定一个二维网格和一个单词，找出该单词是否存在于网格中。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中"相邻"单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

### 解题思路
- 使用深度优先搜索和回溯
- 从网格的每个位置开始，尝试匹配单词的第一个字符
- 如果匹配，继续搜索相邻的单元格，直到找到完整的单词或无法继续匹配

### 代码实现

```java
public class Solution {
    public boolean exist(char[][] board, String word) {
        if (board == null || board.length == 0 || board[0].length == 0 || word == null || word.length() == 0) {
            return false;
        }
        int m = board.length;
        int n = board[0].length;
        boolean[][] visited = new boolean[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (dfs(board, visited, i, j, word, 0)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    private boolean dfs(char[][] board, boolean[][] visited, int i, int j, String word, int index) {
        if (index == word.length()) {
            return true;
        }
        int m = board.length;
        int n = board[0].length;
        if (i < 0 || i >= m || j < 0 || j >= n || visited[i][j] || board[i][j] != word.charAt(index)) {
            return false;
        }
        visited[i][j] = true;
        boolean result = dfs(board, visited, i - 1, j, word, index + 1) ||
                        dfs(board, visited, i + 1, j, word, index + 1) ||
                        dfs(board, visited, i, j - 1, word, index + 1) ||
                        dfs(board, visited, i, j + 1, word, index + 1);
        visited[i][j] = false;
        return result;
    }
}
```

## 总结

DFS和BFS是解决树、图等结构问题的重要工具。通过练习这些高频题目，可以掌握DFS和BFS的基本思路和解题技巧，为面试做好准备。