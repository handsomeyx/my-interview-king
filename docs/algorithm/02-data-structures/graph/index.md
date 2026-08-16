# 图论

> 图的表示 + 四大核心算法（并查集 / Dijkstra / 拓扑排序 / Floyd）。面试常考的不是背算法，是「**什么时候用哪个 + 为什么**」。配套：[专项·DFS/BFS](../../06-practice/dfs-bfs-practice-i/)、[系统算法·一致性哈希](../../04-system-algorithms/consistent-hashing/)。

---

## 图的表示

### 邻接矩阵 vs 邻接表

| 方式 | 空间 | 适用 | 查边 | 遍历邻居 |
|---|---|---|---|---|
| 邻接矩阵 `int[][]` | O(V²) | 稠密图 | O(1) | O(V) |
| 邻接表 `List<Integer>[]` | O(V+E) | 稀疏图 | O(度) | O(度) |

```java
// 邻接表（最常用）
List<Integer>[] graph = new ArrayList[n];
for (int i = 0; i < n; i++) graph[i] = new ArrayList<>();
graph[0].add(1);   // 0→1 有向；无向再 graph[1].add(0)
```

**易错**：面试题绝大多数是**稀疏图**（网格、树、社交网络），用邻接表。邻接矩阵只在 V 很小（<1000）或查边频繁时用。无向图每条边存两次（`graph[a].add(b); graph[b].add(a)`），忘了加反向会变成有向图，BFS/DFS 跑出错。

## 并查集

### 原理

用树形结构维护「属于同一集合」。`find(x)` 找根（根是集合代表），`union(x, y)` 合并两集合。

### Java 实现（路径压缩 + 按秩合并）

```java
class UnionFind {
    int[] parent, rank;
    UnionFind(int n) {
        parent = new int[n]; rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);  // 路径压缩
        return parent[x];
    }
    boolean union(int x, int y) {       // 返回是否合并（不同集合 = true）
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (rank[rx] < rank[ry]) parent[rx] = ry;
        else if (rank[rx] > rank[ry]) parent[ry] = rx;
        else { parent[ry] = rx; rank[rx]++; }
        return true;
    }
}
```

### 两个优化 + 关系

- **路径压缩**（`find` 里把 x 直接连到根）：让后续 `find` 近似 O(1)。
- **按秩合并**（矮树挂高树）：让树不退化成链表。
- **两个都用** → 均摊 O(α(n))（α ≈ 反阿克曼函数，n ≤ 10^80 时 α ≤ 4），**近似 O(1)**。

**易错**：只写路径压缩不写按秩合并，实际够用（竞赛/面试都过），但面试官追问「怎么保证 O(1)」时要答出**两者配合**。另外 `union` 返回 `boolean`（是否成功合并）比返回 void 有用——很多题（LC 684 冗余连接）靠它判「这条边是否多余」。

### 应用

连通分量（LC 547）、Kruskal 最小生成树（边排序 + 并查集判环）、判图有无环（LC 684）。

---

## 最短路径

### 三大算法对比

| 算法 | 场景 | 复杂度 | 核心 |
|---|---|---|---|
| Dijkstra | 单源、**非负权** | O(E log V) | 贪心（每次取最近） |
| Bellman-Ford | 单源、**可负权** | O(VE) | 所有边松弛 V-1 轮 |
| Floyd | **多源** | O(V³) | DP：`dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j])` |

### Dijkstra 为什么不能有负权

Dijkstra 的核心假设是「**已确定的最短距离不会再变**」——每次取最小距离的点标记为「已确定」，因为它不可能通过其他点绕回来更短（非负权保证绕路 ≥ 直达）。负权打破这个假设：一个已确定的点可能通过负边绕回来更短，贪心就错了。

Bellman-Ford 不做这个假设——它对**所有边**松弛 V-1 轮，每轮可能更新已确定的点。代价是慢（O(VE)），但能处理负权 + 检测负环（第 V 轮还能松弛 = 有负环）。

### Dijkstra 代码

```java
int[] dijkstra(int n, List<int[]>[] graph, int src) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{src, 0});
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int u = cur[0], d = cur[1];
        if (d > dist[u]) continue;            // ← lazy deletion：跳过过期
        for (int[] edge : graph[u]) {
            int v = edge[0], w = edge[1];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.offer(new int[]{v, dist[v]});
            }
        }
    }
    return dist;
}
```

**易错**：`if (d > dist[u]) continue` 是 **lazy deletion**——同一节点可能被多次入队（每次距离不同），出队时跳过过期的。不写这行会 TLE（重复处理，复杂度退化）。

---

## 拓扑排序

### 原理

对 **DAG**（有向无环图）线性排序，使每条边 (u,v) 的 u 在 v 前。

### Kahn（BFS 入度法，最常用）

```java
int[] topoSort(int n, List<int[]> edges) {
    List<Integer>[] graph = new ArrayList[n];
    int[] indegree = new int[n];
    for (int i = 0; i < n; i++) graph[i] = new ArrayList<>();
    for (int[] e : edges) { graph[e[0]].add(e[1]); indegree[e[1]]++; }
    Queue<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (indegree[i] == 0) q.offer(i);
    int[] res = new int[n]; int idx = 0;
    while (!q.isEmpty()) {
        int u = q.poll(); res[idx++] = u;
        for (int v : graph[u]) if (--indegree[v] == 0) q.offer(v);
    }
    return idx == n ? res : new int[0];   // idx<n 说明有环
}
```

### 拓扑排序判环

**处理完的节点数 < 总节点数 → 有环**（环里的点入度永远降不到 0）。这就是 [课程表 LC 207](../../06-practice/dfs-bfs-practice-i/) 的判环方法。

**易错**：拓扑排序**只适用于 DAG**。有环图不能拓扑排序——返回「无法排序」本身就是判环的信号。

---

## 面试高频：图论怎么考

| 问题特征 | 选哪个 |
|---|---|
| 连通性 / 连通分量 | DFS / BFS / 并查集 |
| 单源最短路径（非负权） | Dijkstra + 堆 |
| 单源最短路径（负权） | Bellman-Ford |
| 任意两点最短 | Floyd（DP，V 小时用） |
| 依赖关系 / 编译顺序 | 拓扑排序 Kahn |
| 判有环 | 拓扑排序（处理数 < 总数）/ DFS 三色 |
| 最小生成树 | Kruskal（并查集）/ Prim |

> 图论的核心不是背算法——是「**看到问题特征选对算法**」：连通 → DFS/BFS/并查集；最短 → Dijkstra（非负）/ Bellman-Ford（负）；依赖 → 拓扑。刷题见 [DFS/BFS 专项](../../06-practice/dfs-bfs-practice-i/)。
