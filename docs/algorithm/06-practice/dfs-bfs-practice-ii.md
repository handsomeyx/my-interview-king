---
title: DFS/BFS 专项练习 II（状态空间与组合技术）
---

# DFS/BFS 专项练习 II（状态空间与组合技术）

> 配套：[DFS/BFS I（网格与图）](./dfs-bfs-practice-i/)。本篇讲 BFS 的进阶——**状态空间搜索**（把「状态」当节点，BFS 求最短转换）和**双技术组合**（DFS 找岛 + BFS 连接）。难点不在模板，在三件事：**状态怎么定义（字符串 / 元组 / 矩阵快照）**、**邻居怎么生成**、**visited 怎么去重**。

## 框架速记

```text
// 状态空间 BFS（求最短转换序列）
Queue<状态> q = new LinkedList<>();
Set<状态> visited = new HashSet<>();
q.offer(初始状态); visited.add(初始状态);
int steps = 0;
while (!q.isEmpty()) {
    int size = q.size();
    for (int i = 0; i < size; i++) {
        状态 cur = q.poll();
        if (cur == 目标) return steps;
        for (状态 next : 生成所有邻居(cur)) {
            if (合法 && !visited.contains(next)) { visited.add(next); q.offer(next); }
        }
    }
    steps++;
}
```

三个钩子：**状态定义**、**邻居生成规则**、**visited 去重**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [单词接龙](https://leetcode.cn/problems/word-ladder/) | 困 | 字符串状态，改一字母生成邻居 |
| 2 | [打开转盘锁](https://leetcode.cn/problems/open-the-lock/) | 中 | 4 位数字状态，每位 ±1 |
| 3 | [滑动谜题](https://leetcode.cn/problems/sliding-puzzle/) | 困 | 矩阵快照状态（序列化成字符串） |
| 4 | [二进制矩阵中的最短路径](https://leetcode.cn/problems/shortest-path-in-binary-matrix/) | 简 | 8 方向网格 BFS |
| 5 | [地图分析](https://leetcode.cn/problems/as-far-from-land-as-possible/) | 中 | 多源 BFS 求最远距离 |
| 6 | [迷宫中离入口最近的出口](https://leetcode.cn/problems/nearest-exit-from-entrance-in-maze/) | 中 | 网格 BFS + 出口判定 |
| 7 | [跳跃游戏 III](https://leetcode.cn/problems/jump-game-iii/) | 中 | 跳跃规则生成邻居 |
| 8 | [最短的桥](https://leetcode.cn/problems/shortest-bridge/) | 中 | DFS 找岛 + BFS 连接 |
| 9 | [获取所有钥匙的最短路径](https://leetcode.cn/problems/shortest-path-to-get-all-keys/) | 困 | 状态含钥匙位掩码 |
| 10 | [推箱子](https://leetcode.cn/problems/minimum-moves-to-move-a-box-to-their-target-location/) | 困 | 双状态（箱+人）A*/BFS |

---

## 例题 1：单词接龙（LC 127，字符串状态 BFS）

**题目**：从 `beginWord` 每次改一个字母变成 `wordList` 里的词，求到 `endWord` 的最短转换序列长度。

**为什么 BFS 不是 DFS**：求「最短」转换序列，BFS 天然按层扩展，第一次到 endWord 就是最短步数。DFS 要枚举所有路径再取 min，状态空间是指数级（每个单词 26 种变换），必超时。

**如何套 + 变化点**：状态 = 单词（字符串）。邻居生成：对当前单词每个位置，尝试改成 a-z，看是否在 wordList 里。visited 用 HashSet 去重。

```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> dict = new HashSet<>(wordList);
    if (!dict.contains(endWord)) return 0;
    Queue<String> q = new LinkedList<>();
    Set<String> visited = new HashSet<>();
    q.offer(beginWord); visited.add(beginWord);
    int steps = 1;
    while (!q.isEmpty()) {
        int size = q.size();
        for (int k = 0; k < size; k++) {
            String cur = q.poll();
            if (cur.equals(endWord)) return steps;
            for (int i = 0; i < cur.length(); i++) {
                char[] arr = cur.toCharArray();
                for (char c = 'a'; c <= 'z'; c++) {
                    arr[i] = c;
                    String next = new String(arr);
                    if (dict.contains(next) && !visited.contains(next)) {
                        visited.add(next); q.offer(next);
                    }
                }
            }
        }
        steps++;
    }
    return 0;
}
```

**易错点**：
- 邻居生成用「改每一位为 a-z」，**不是**「遍历 wordList 找差一位的词」。后者每次 O(n·L)，n=5000 时一层就爆；前者固定 26·L，快得多。这是这题性能的关键。
- `steps` 初始 1（含 beginWord 本身），不是 0。题目问「转换序列长度」（含首尾），BFS 第一层就是 beginWord，steps 在层结束后 +1，第一次匹配时返回的 steps 已包含完整序列。
- `visited` 必须在 **offer 时就标记**，不是 pop 时。否则同一层的重复状态会重复入队，队列爆炸。

---

## 例题 2：打开转盘锁（LC 752，状态 BFS + 禁忌）

**题目**：4 位转盘锁（每位 0-9），每次把一位拨一格（9↔0 环），`deadends` 里的状态不能碰，求从 `"0000"` 到 `target` 的最少拨动次数。

**如何套 + 变化点**：状态 = 4 位数字字符串。邻居生成：每位 +1 或 -1（mod 10）。deadends 当作 visited 的一部分（一开始就并入）。

```java
public int openLock(String[] deadends, String target) {
    Set<String> dead = new HashSet<>(Arrays.asList(deadends));
    if (dead.contains("0000")) return -1;       // 起点就锁死
    Queue<String> q = new LinkedList<>();
    Set<String> visited = new HashSet<>(dead);  // deadends 一开始就当 visited
    q.offer("0000"); visited.add("0000");
    int turns = 0;
    while (!q.isEmpty()) {
        int size = q.size();
        for (int k = 0; k < size; k++) {
            String cur = q.poll();
            if (cur.equals(target)) return turns;
            for (int i = 0; i < 4; i++) {
                for (int d = -1; d <= 1; d += 2) {
                    char[] arr = cur.toCharArray();
                    arr[i] = (char) ((arr[i] - '0' + d + 10) % 10 + '0');   // 环形 ±1
                    String next = new String(arr);
                    if (!visited.contains(next)) { visited.add(next); q.offer(next); }
                }
            }
        }
        turns++;
    }
    return -1;
}
```

**易错点**：
- 环形拨动用 `(arr[i] - '0' + d + 10) % 10`，**`+10` 不能漏**。`d = -1` 时 `arr[i] - '0' - 1` 对 `'0'` 是 `-1`，Java 的 `%` 对负数保留负号（`-1 % 10 = -1`），加 10 再 % 才能正确环绕到 9。
- `dead` 一开始就并入 `visited`，**不是每次 offer 前单独判 `dead.contains(next)`**。把 deadends 当成「已访问的禁忌状态」统一处理，代码更简洁，且避免漏判（比如 `"0000"` 本身就是 deadend，要在 BFS 前就判，否则直接错）。

---

## 例题 3：最短的桥（LC 934，DFS + BFS 组合）

**题目**：n×n 二元矩阵，有两个岛（连通的 1），求把它们连起来最少要填几个 0（桥的长度）。

**为什么先 DFS 再 BFS**：这题两步——先「定位」第一个岛（哪些格子属于岛 1），再「扩散」找最短桥。DFS 天然适合「连通块染色」（一次性把整个岛标出来），BFS 适合「最短扩散距离」。组合用：DFS 染色岛 1（顺便把岛 1 所有格子入队），再 BFS 从岛 1 所有点同时向外扩散，第一次碰到岛 2 的格子时，扩散的层数就是最短桥。

**如何套 + 变化点**：第一步 DFS 把岛 1 染成 2（避免和岛 2 混），所有岛 1 格子入队；第二步多源 BFS（岛 1 全部点为源）向外扩 0，第一次遇到 `grid == 1`（岛 2）时返回层数。

```java
public int shortestBridge(int[][] grid) {
    int n = grid.length;
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    Queue<int[]> q = new LinkedList<>();
    // 第一步：DFS 找第一个岛，染色为 2，所有点入队
    boolean found = false;
    for (int i = 0; i < n && !found; i++) {
        for (int j = 0; j < n && !found; j++) {
            if (grid[i][j] == 1) { dfs(grid, i, j, q); found = true; }
        }
    }
    // 第二步：BFS 从岛 1（=2）扩散，遇到岛 2（=1）的距离即答案
    int dist = 0;
    while (!q.isEmpty()) {
        int size = q.size();
        for (int k = 0; k < size; k++) {
            int[] cur = q.poll();
            for (int[] d : dirs) {
                int ni = cur[0] + d[0], nj = cur[1] + d[1];
                if (ni >= 0 && ni < n && nj >= 0 && nj < n) {
                    if (grid[ni][nj] == 1) return dist;     // 碰到岛 2
                    if (grid[ni][nj] == 0) { grid[ni][nj] = 2; q.offer(new int[]{ni, nj}); }
                }
            }
        }
        dist++;
    }
    return -1;
}
private void dfs(int[][] grid, int i, int j, Queue<int[]> q) {
    if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] != 1) return;
    grid[i][j] = 2;
    q.offer(new int[]{i, j});
    dfs(grid, i+1, j, q); dfs(grid, i-1, j, q); dfs(grid, i, j+1, q); dfs(grid, i, j-1, q);
}
```

**易错点**：
- DFS 染色后岛 1 变成 2，BFS 扩散时遇到的「岛 2」是 `grid == 1`（没染色的那个）。**不要染成同一个值**——如果两岛都染 2 就分不清，BFS 会无限扩散。染色值要区别于岛 2。
- BFS 第一次碰到 `grid == 1` 返回的 `dist` 是「桥长」（填的 0 的个数），**不是 dist+1**。因为 BFS 在「扩散到岛 2 那一层」之前，dist 已经 ++ 到「从岛 1 边缘走 dist 步碰到岛 2」。边界要对清楚，写反就差 1。
- DFS 找第一个岛时用 `found` 标志**只染一个岛**。漏了 found 会把两个岛都染成 2，BFS 无目标。

---

## 练习建议

按范式分组：
- 状态空间 BFS：1、2、3、9、10
- 网格 BFS 变体：4、5、6、7
- 双技术组合：8（DFS+BFS）

**如果时间只够做 3 道**：做 **1、5、8**——分别覆盖「字符串状态 BFS / 多源 BFS 求最远 / DFS+BFS 组合」三种最考抽象能力的 BFS 范式。2 是 1 的简化（状态更小），6 是 5 的变体。

## 下一步

BFS 的难点不在「走」，而在「把问题抽象成状态图」。本篇覆盖状态空间与组合技术；剩下 7 道的变化点已在表格列出。卡题时先问自己：「状态是什么？邻居怎么生成？visited 怎么去重？」——这三个钩子想清楚，BFS 框架就能套上。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
