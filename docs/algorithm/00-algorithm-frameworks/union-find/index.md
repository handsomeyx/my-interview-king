---
problems:
  - title: 冗余连接
    url: https://leetcode.cn/problems/redundant-connection/
    difficulty: medium
  - title: 岛屿数量
    url: https://leetcode.cn/problems/number-of-islands/
    difficulty: medium
---

# 并查集框架

## 算法原理

并查集（Union-Find）是一种用于处理集合合并和查询问题的数据结构。它支持两种主要操作：

1. **查找（Find）**：查找元素所属的集合
2. **合并（Union）**：将两个集合合并为一个集合

并查集的核心思想是使用树结构来表示集合，每个集合由一个根节点代表。通过路径压缩和按秩合并等优化手段，可以使操作的时间复杂度接近常数。

## 框架模板

```java
class UnionFind {
    private int[] parent;  // 记录每个元素的父节点
    private int[] rank;    // 记录每个集合的秩（大小）
    
    // 构造函数
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        
        // 初始化：每个元素的父节点是自己，秩为 1
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            rank[i] = 1;
        }
    }
    
    // 查找操作：找到元素 x 所属的集合的根节点
    public int find(int x) {
        // 路径压缩：将路径上的所有节点直接连接到根节点
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    // 合并操作：将元素 x 和元素 y 所属的集合合并
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        // 如果已经在同一个集合中，不需要合并
        if (rootX == rootY) {
            return;
        }
        
        // 按秩合并：将秩小的集合合并到秩大的集合中
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else {
            parent[rootY] = rootX;
            if (rank[rootX] == rank[rootY]) {
                rank[rootX]++;
            }
        }
    }
    
    // 判断两个元素是否在同一个集合中
    public boolean isConnected(int x, int y) {
        return find(x) == find(y);
    }
}
```

## 适用场景

1. **连通性问题**：判断图中两个节点是否连通
2. **动态连通性**：处理动态变化的连通性问题
3. **最小生成树算法**：如 Kruskal 算法
4. **图的环检测**：检测图中是否存在环
5. **元素分组**：将元素分组并处理组间关系

## 注意事项

1. **路径压缩**：在查找操作中，将路径上的所有节点直接连接到根节点，减少后续查找的时间
2. **按秩合并**：在合并操作中，将秩小的集合合并到秩大的集合中，保持树的高度较小
3. **初始化**：确保每个元素的父节点初始化为自己，秩初始化为 1
4. **元素索引**：并查集通常使用整数索引来表示元素，对于非整数元素，需要进行映射

## 示例：冗余连接

### 题目描述

树可以看成是一个连通且无环的无向图。

给定一个包含 `n` 个节点的图，节点编号从 `1` 到 `n`。图中的边是无向的，每条边都用一对节点来表示。

如果该图是一棵树，则返回 `[]`。否则，返回最后出现的导致图不成为树的那条边。

### 代码实现

```java
public int[] findRedundantConnection(int[][] edges) {
    int n = edges.length;
    UnionFind uf = new UnionFind(n + 1);  // 节点编号从 1 开始
    
    for (int[] edge : edges) {
        int u = edge[0];
        int v = edge[1];
        
        // 如果两个节点已经在同一个集合中，说明这条边是冗余的
        if (uf.isConnected(u, v)) {
            return edge;
        }
        // 否则，合并两个集合
        uf.union(u, v);
    }
    
    return new int[0];
}

class UnionFind {
    private int[] parent;
    private int[] rank;
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            rank[i] = 1;
        }
    }
    
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) {
            return;
        }
        
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else {
            parent[rootY] = rootX;
            if (rank[rootX] == rank[rootY]) {
                rank[rootX]++;
            }
        }
    }
    
    public boolean isConnected(int x, int y) {
        return find(x) == find(y);
    }
}
```

### 解释

1. **初始化并查集**：创建一个大小为 `n + 1` 的并查集，因为节点编号从 1 开始
2. **遍历边**：对于每条边，检查两个节点是否已经在同一个集合中
   - 如果是，说明这条边是冗余的，返回这条边
   - 如果不是，合并两个节点所在的集合
3. **返回结果**：如果所有边都处理完毕，返回空数组

## 示例：岛屿数量

### 题目描述

给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

### 代码实现

```java
public int numIslands(char[][] grid) {
    if (grid == null || grid.length == 0) {
        return 0;
    }
    
    int m = grid.length;
    int n = grid[0].length;
    int count = 0;
    
    // 初始化并查集
    UnionFind uf = new UnionFind(m * n);
    int waterCount = 0;
    
    // 遍历网格
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '1') {
                // 检查四个方向的邻居
                int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
                for (int[] dir : dirs) {
                    int x = i + dir[0];
                    int y = j + dir[1];
                    if (x >= 0 && x < m && y >= 0 && y < n && grid[x][y] == '1') {
                        // 合并相邻的陆地
                        uf.union(i * n + j, x * n + y);
                    }
                }
            } else {
                waterCount++;
            }
        }
    }
    
    // 岛屿数量 = 总陆地数量 - 合并的次数
    // 或者更简单的方法：计算不同的根节点数量
    Set<Integer> roots = new HashSet<>();
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '1') {
                roots.add(uf.find(i * n + j));
            }
        }
    }
    
    return roots.size();
}

class UnionFind {
    private int[] parent;
    private int[] rank;
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            rank[i] = 1;
        }
    }
    
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) {
            return;
        }
        
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else {
            parent[rootY] = rootX;
            if (rank[rootX] == rank[rootY]) {
                rank[rootX]++;
            }
        }
    }
}
```

### 解释

1. **初始化**：创建一个大小为 `m * n` 的并查集，用于表示每个格子
2. **遍历网格**：对于每个陆地格子，检查其四个方向的邻居
   - 如果邻居也是陆地，就将当前格子和邻居合并到同一个集合中
3. **计算岛屿数量**：遍历所有陆地格子，找到它们的根节点，不同的根节点数量就是岛屿的数量

## 总结

并查集是一种高效的数据结构，用于处理集合合并和查询问题。通过路径压缩和按秩合并等优化手段，可以使操作的时间复杂度接近常数。并查集在处理连通性问题、动态连通性问题、最小生成树算法等方面有广泛的应用。