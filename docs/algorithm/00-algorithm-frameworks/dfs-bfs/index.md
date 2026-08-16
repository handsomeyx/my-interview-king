---
problems:
  - title: 二叉树的层序遍历
    url: https://leetcode.cn/problems/binary-tree-level-order-traversal/
    difficulty: medium
  - title: 二叉树的最大深度
    url: https://leetcode.cn/problems/maximum-depth-of-binary-tree/
    difficulty: easy
  - title: 岛屿数量
    url: https://leetcode.cn/problems/number-of-islands/
    difficulty: medium
  - title: 单词搜索
    url: https://leetcode.cn/problems/word-search/
    difficulty: medium
  - title: 单词接龙
    url: https://leetcode.cn/problems/word-ladder/
    difficulty: hard
---

# DFS/BFS 框架

## 思考锚点

DFS 和 BFS 是图和树的两种基本遍历方式，它们的区别可以用一句话概括：**DFS 用栈（递归）先走到底再回溯，BFS 用队列一层一层地走**。

理解 DFS/BFS 的关键不是记住代码，而是理解「**遍历顺序的选择决定了能否解决问题**」：
- DFS 适合需要「深入探索」的场景，比如回溯问题（全排列、组合）、连通性问题
- BFS 适合需要「层序信息」的场景，比如最短路径（无权图）、二叉树的层序遍历

为什么 DFS 可以用递归实现？因为递归的调用栈本质上就是一个栈——最后调用的函数最先返回。这和 DFS 的「先走到底再回溯」完全一致。

## 算法原理

DFS（深度优先搜索）和 BFS（广度优先搜索）是两种常用的图遍历算法，也广泛应用于树的遍历问题。

- **DFS**：从起点开始，沿着一条路径尽可能深入地搜索，直到无法继续为止，然后回溯到上一个节点，继续搜索其他路径。
- **BFS**：从起点开始，先访问所有相邻节点，然后再访问这些相邻节点的相邻节点，以此类推，按照距离从近到远的顺序搜索。

## DFS 框架

### 递归实现

```java
// 树的DFS遍历
public void dfs(TreeNode node) {
    if (node == null) {
        return;
    }
    
    // 前序遍历：先处理当前节点
    System.out.println(node.val);
    
    // 递归处理左子树
    dfs(node.left);
    
    // 中序遍历：处理当前节点
    // System.out.println(node.val);
    
    // 递归处理右子树
    dfs(node.right);
    
    // 后序遍历：处理当前节点
    // System.out.println(node.val);
}

// 图的DFS遍历（避免重复访问）
public void dfs(int start, List<List<Integer>> graph, boolean[] visited) {
    // 标记当前节点为已访问
    visited[start] = true;
    System.out.println(start);
    
    // 遍历所有相邻节点
    for (int neighbor : graph.get(start)) {
        if (!visited[neighbor]) {
            dfs(neighbor, graph, visited);
        }
    }
}
```

### 非递归实现（使用栈）

```java
// 非递归实现DFS
public void dfs(TreeNode root) {
    if (root == null) {
        return;
    }
    
    Stack<TreeNode> stack = new Stack<>();
    stack.push(root);
    
    while (!stack.isEmpty()) {
        TreeNode node = stack.pop();
        System.out.println(node.val);  // 处理当前节点
        
        // 注意：先压右子节点，再压左子节点，这样弹出顺序是左子节点先于右子节点
        if (node.right != null) {
            stack.push(node.right);
        }
        if (node.left != null) {
            stack.push(node.left);
        }
    }
}
```

## BFS 框架

### 使用队列实现

```java
// 树的BFS遍历（层序遍历）
public void bfs(TreeNode root) {
    if (root == null) {
        return;
    }
    
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    
    while (!queue.isEmpty()) {
        int size = queue.size();  // 当前层的节点数
        
        // 处理当前层的所有节点
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            System.out.println(node.val);  // 处理当前节点
            
            // 将子节点加入队列
            if (node.left != null) {
                queue.offer(node.left);
            }
            if (node.right != null) {
                queue.offer(node.right);
            }
        }
    }
}

// 图的BFS遍历（避免重复访问）
public void bfs(int start, List<List<Integer>> graph) {
    boolean[] visited = new boolean[graph.size()];
    Queue<Integer> queue = new LinkedList<>();
    
    visited[start] = true;
    queue.offer(start);
    
    while (!queue.isEmpty()) {
        int node = queue.poll();
        System.out.println(node);  // 处理当前节点
        
        // 遍历所有相邻节点
        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                queue.offer(neighbor);
            }
        }
    }
}
```

## 适用场景

### DFS 适用场景

1. **树的遍历**：前序、中序、后序遍历
2. **图的遍历**：深度优先搜索
3. **回溯问题**：如全排列、组合、子集等
4. **连通性问题**：判断图是否连通
5. **路径搜索**：寻找从起点到终点的路径

### BFS 适用场景

1. **树的层序遍历**：按层访问树的节点
2. **图的遍历**：广度优先搜索
3. **最短路径问题**：在无权图中寻找最短路径
4. **连通性问题**：判断图是否连通
5. **层次相关问题**：如二叉树的最小深度

## 注意事项

### DFS 注意事项

1. **递归深度**：递归实现可能导致栈溢出，对于深度较大的树或图，建议使用非递归实现
2. **重复访问**：在图的遍历中，需要使用 visited 数组避免重复访问
3. **回溯**：在回溯问题中，需要注意状态的保存和恢复

### BFS 注意事项

1. **队列使用**：正确使用队列来存储待访问的节点
2. **层序处理**：在处理层序遍历时，需要记录每层的节点数
3. **重复访问**：在图的遍历中，需要使用 visited 数组避免重复访问

## 示例：二叉树的层序遍历

### 题目描述

给你一个二叉树，请你返回其按 **层序遍历** 得到的节点值。 （即逐层地，从左到右访问所有节点）。

### 代码实现

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) {
        return result;
    }
    
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    
    while (!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> level = new ArrayList<>();
        
        for (int i = 0; i < size; i++) {
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
```

### 解释

1. **初始化**：创建结果列表和队列，将根节点加入队列
2. **层序遍历**：
   - 记录当前层的节点数
   - 遍历当前层的所有节点，将它们的值加入当前层的列表
   - 将子节点加入队列
   - 将当前层的列表加入结果列表
3. **返回结果**：返回层序遍历的结果

## 示例：二叉树的最大深度

### 题目描述

给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

### DFS 实现

```java
public int maxDepth(TreeNode root) {
    if (root == null) {
        return 0;
    }
    
    int leftDepth = maxDepth(root.left);
    int rightDepth = maxDepth(root.right);
    
    return Math.max(leftDepth, rightDepth) + 1;
}
```

### BFS 实现

```java
public int maxDepth(TreeNode root) {
    if (root == null) {
        return 0;
    }
    
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    int depth = 0;
    
    while (!queue.isEmpty()) {
        int size = queue.size();
        depth++;
        
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            
            if (node.left != null) {
                queue.offer(node.left);
            }
            if (node.right != null) {
                queue.offer(node.right);
            }
        }
    }
    
    return depth;
}
```

## 总结

DFS 和 BFS 是两种重要的搜索算法，各有其适用场景。通过掌握这些框架，你可以快速解决许多与树和图相关的问题。在实际应用中，需要根据具体问题选择合适的算法，并注意避免常见的陷阱。

---

## 复述自测

读完这篇，试试用自己的话回答三个问题：

1. **一句话总结**：DFS 和 BFS 的核心区别是什么？它们分别适用于哪些场景？

2. **讲给初学者听**：怎么用「走迷宫」来类比 DFS（一条路走到黑，不通再回来试别的路）和 BFS（每条路同时探索，谁先到终点）？

3. **预判追问**：如果你是面试官，读完这篇你会追问什么？（比如 DFS 递归实现的空间复杂度是多少？BFS 怎么解决「单词接龙」这类最短路径问题？）