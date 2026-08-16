---
title: DFS/BFS 专项练习 I（网格与图）
---

# DFS/BFS 专项练习 I（网格与图）

> 配套框架：[DFS/BFS 框架](../00-algorithm-frameworks/dfs-bfs/)。网格和图的题，骨架只有两个——**DFS（染色/连通）** 和 **BFS（最短/扩散）**。区别在三件事：**用什么遍历、怎么标记访问、从哪里出发（单源/多源）**。下面精讲 3 道覆盖三种范式（网格 DFS / 多源 BFS / 拓扑排序），再给 7 道变化点清单。

## 框架速记

```text
// 网格 DFS（连通分量、染色）
void dfs(grid, i, j) {
    if (越界 || 已访问 || 不可达) return;
    grid[i][j] = VISITED;          // ← 就地标记，省 visited 数组
    for (dir in 上下左右) dfs(grid, i+dir[0], j+dir[1]);
}

// BFS（最短步数、扩散）
Queue<node> q = new LinkedList<>();
q.offer(起点);
while (!q.isEmpty()) {
    int size = q.size();
    for (int i = 0; i < size; i++) {   // 逐层
        node = q.poll();
        for (邻居) if (未访问) { 标记; q.offer(邻居); }
    }
    step++;     // 走完一层
}
```

三个钩子：**遍历方式（DFS/BFS）**、**访问标记（就地改 grid / visited 数组）**、**起点（单源 / 多源同时入队）**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [岛屿数量](https://leetcode.cn/problems/number-of-islands/) | 中 | 网格 DFS 染色 |
| 2 | [岛屿的最大面积](https://leetcode.cn/problems/max-area-of-island/) | 中 | DFS 计数返回 |
| 3 | [被围绕的区域](https://leetcode.cn/problems/surrounded-regions/) | 中 | 从边界 DFS 反向染色 |
| 4 | [图像渲染](https://leetcode.cn/problems/flood-fill/) | 简 | DFS 染色（起点扩散） |
| 5 | [腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/) | 中 | 多源 BFS，求分钟数 |
| 6 | [01 矩阵](https://leetcode.cn/problems/01-matrix/) | 中 | 多源 BFS（从 0 扩散到 1） |
| 7 | [课程表](https://leetcode.cn/problems/course-schedule/) | 中 | 拓扑排序判环 |
| 8 | [课程表 II](https://leetcode.cn/problems/course-schedule-ii/) | 中 | 拓扑返回顺序 |
| 9 | [克隆图](https://leetcode.cn/problems/clone-graph/) | 中 | DFS + HashMap |
| 10 | [钥匙和房间](https://leetcode.cn/problems/keys-and-rooms/) | 中 | DFS 可达性 |

---

## 例题 1：岛屿数量（LC 200，网格 DFS）

**题目**：`'1'` 是陆地、`'0'` 是水，统计岛屿数量（水平/垂直相连的 `'1'` 算一个岛）。

**如何套 + 变化点**：遍历每个格子，遇到 `'1'` 就是一个新岛（count++），然后用 DFS 把整个岛「淹掉」（`'1'` 改 `'0'`，就地标记访问），保证不重复数。

```java
public int numIslands(char[][] grid) {
    int count = 0;
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == '1') {
                count++;
                dfs(grid, i, j);
            }
        }
    }
    return count;
}
private void dfs(char[][] grid, int i, int j) {
    if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] != '1') return;
    grid[i][j] = '0';   // 就地标记
    dfs(grid, i + 1, j); dfs(grid, i - 1, j); dfs(grid, i, j + 1); dfs(grid, i, j - 1);
}
```

**易错点**：
- **就地标记**（`grid[i][j] = '0'`）省掉 visited 数组，省内存。但**必须在递归开头先标记再展开**，否则会无限递归（A 访问 B，B 看到邻居 A 还是 `'1'`，又回去访问 A，栈溢出）。
- 越界 + 状态判断**全写在递归首行**（`if 越界 || grid[i][j] != '1'`）。不要在调用前分别判，那样代码乱且容易漏判一个方向。

---

## 例题 2：腐烂的橘子（LC 994，多源 BFS）

**题目**：每分钟，腐烂橘子（值 2）会传染上下左右的fresh橘子（值 1）。求所有 fresh 橘子腐烂的最短分钟数；若有 fresh 永远染不到，返回 -1。

**为什么用 BFS 而非 DFS**：橘子传染是「同时扩散」——每分钟所有腐烂橘子一起向外扩 1 格。这天然是**按层**进行，BFS 的逐层就是「每分钟」。DFS 是一条路走到底，会得到错误的「单条路径深度」而不是「最短扩散时间」。而且初始有**多个**腐烂橘子（多源），必须全部 Day0 同时入队。

**如何套 + 变化点**：把所有初始腐烂橘子先入队（多源 BFS 起点），逐层扩散。用 `fresh` 计数（初始 fresh 数），每染一个就 `fresh--`；最后 `fresh == 0` 返回分钟数，否则 -1。

```java
public int orangesRotting(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    Queue<int[]> q = new LinkedList<>();
    int fresh = 0;
    for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
        if (grid[i][j] == 2) q.offer(new int[]{i, j});   // 多源：所有腐烂橘子先入队
        else if (grid[i][j] == 1) fresh++;
    }
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    int minutes = 0;
    while (!q.isEmpty() && fresh > 0) {     // fresh>0 才继续（全染完提前停）
        int size = q.size();
        for (int k = 0; k < size; k++) {
            int[] cur = q.poll();
            for (int[] d : dirs) {
                int ni = cur[0] + d[0], nj = cur[1] + d[1];
                if (ni >= 0 && ni < m && nj >= 0 && nj < n && grid[ni][nj] == 1) {
                    grid[ni][nj] = 2;
                    fresh--;
                    q.offer(new int[]{ni, nj});
                }
            }
        }
        minutes++;
    }
    return fresh == 0 ? minutes : -1;
}
```

**易错点**：
- **多源**：所有腐烂橘子先入队（`if (grid[i][j] == 2) q.offer(...)`），**不是**找一个源开始 BFS。多源 BFS 的关键就是把所有源当 Day0 的起点。
- 循环条件带 `fresh > 0`：染完了就别再空转一层（否则 minutes 会多 +1）。
- 返回 `fresh == 0 ? minutes : -1`：可能存在 fresh 永远染不到（被水隔开），要靠 fresh 计数判断，不能直接返回 minutes。

---

## 例题 3：课程表（LC 207，拓扑排序判环）

**题目**：`numCourses` 门课，`prerequisites[i] = [a, b]` 表示要先修 b 才能修 a。判断能否修完所有课。

**如何套 + 变化点**：本质是有向图判环——有环则死锁（互相依赖）修不完。用**拓扑排序（BFS + 入度）**：每次把「入度为 0」（无依赖）的课入队，出队时把它作为依赖的后续课程的入度 -1，新的入度 0 再入队。最后**处理过的课程数 == 总课程数**则无环，可完成。

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    int[] indegree = new int[numCourses];
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
    for (int[] p : prerequisites) {
        adj.get(p[1]).add(p[0]);    // p[1] → p[0]
        indegree[p[0]]++;
    }
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) if (indegree[i] == 0) q.offer(i);
    int count = 0;
    while (!q.isEmpty()) {
        int course = q.poll();
        count++;
        for (int next : adj.get(course)) {
            if (--indegree[next] == 0) q.offer(next);
        }
    }
    return count == numCourses;
}
```

**易错点**：
- **入度减 0 的判断在 `--` 之后**（`if (--indegree[next] == 0)`）。先减再判；如果写成 `indegree[next]--; if (indegree[next] == 0)` 也对，但合并成一行更简洁且不易漏。
- 判环靠 `count == numCourses`：处理的节点数等于总数说明所有节点都被拓扑序排出（无环）；不等则剩下的节点都在环里（入度永远降不到 0）。**不要返回 `q.isEmpty()`**——队列空了不代表全部处理（可能环里的节点从没入过队）。
- 邻接表方向：`prerequisites[i] = [a, b]` 表示 b→a（先 b 后 a），所以边是 `adj.get(b).add(a)`，`a` 的入度 +1。方向反了就判不出环。

---

## 练习建议

按范式分组：
- 网格 DFS（连通/染色）：1、2、3、4
- 多源 BFS（扩散/最短）：5、6
- 图 + 拓扑（有向判环）：7、8
- 图 + DFS（克隆/可达）：9、10

**如果时间只够做 3 道**：做 **1、5、7**——分别覆盖「网格 DFS / 多源 BFS / 拓扑排序」三种 DFS/BFS 最核心范式。2/3/4 是 1 的变体（改 DFS 访问动作），6 是 5 的变体（换数据含义），8 是 7 加返回顺序。

## 下一步

DFS/BFS 专项 II 会讲进阶（状态 BFS、双向 BFS、A*）。本篇覆盖网格与图基础；剩下 7 道的变化点已在表格列出。卡题时回看 [DFS/BFS 框架](../00-algorithm-frameworks/dfs-bfs/)，对照「遍历方式 + 访问标记 + 起点」三处钩子。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
