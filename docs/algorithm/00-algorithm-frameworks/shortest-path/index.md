---
problems:
  - title: 网络延迟时间
    url: https://leetcode.cn/problems/network-delay-time/
    difficulty: medium
  - title: 单词接龙
    url: https://leetcode.cn/problems/word-ladder/
    difficulty: hard
---

# 最短路径框架

## 算法原理

最短路径算法是用于寻找图中两个节点之间最短路径的算法。常见的最短路径算法包括：

1. **Dijkstra 算法**：用于解决单源最短路径问题，适用于边权非负的图
2. **Bellman-Ford 算法**：用于解决单源最短路径问题，适用于存在负权边的图
3. **Floyd-Warshall 算法**：用于解决所有节点对之间的最短路径问题
4. **BFS 算法**：用于解决无权图的最短路径问题

## Dijkstra 算法框架

```java
public int[] dijkstra(int n, List<List<int[]>> graph, int start) {
    // 存储从起点到各节点的最短距离
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;
    
    // 优先队列，按距离排序
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{start, 0});
    
    while (!pq.isEmpty()) {
        int[] current = pq.poll();
        int u = current[0];
        int currentDist = current[1];
        
        // 如果当前距离大于已知最短距离，跳过
        if (currentDist > dist[u]) {
            continue;
        }
        
        // 遍历所有邻居
        for (int[] neighbor : graph.get(u)) {
            int v = neighbor[0];
            int weight = neighbor[1];
            int newDist = currentDist + weight;
            
            // 如果找到更短的路径，更新距离并加入优先队列
            if (newDist < dist[v]) {
                dist[v] = newDist;
                pq.offer(new int[]{v, newDist});
            }
        }
    }
    
    return dist;
}
```

## Bellman-Ford 算法框架

```java
public int[] bellmanFord(int n, int[][] edges, int start) {
    // 存储从起点到各节点的最短距离
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;
    
    // 松弛操作，最多进行 n-1 次
    for (int i = 0; i < n - 1; i++) {
        boolean updated = false;
        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int weight = edge[2];
            
            if (dist[u] != Integer.MAX_VALUE && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                updated = true;
            }
        }
        
        // 如果没有更新，提前结束
        if (!updated) {
            break;
        }
    }
    
    // 检测负权环
    for (int[] edge : edges) {
        int u = edge[0];
        int v = edge[1];
        int weight = edge[2];
        
        if (dist[u] != Integer.MAX_VALUE && dist[u] + weight < dist[v]) {
            // 存在负权环
            return null;
        }
    }
    
    return dist;
}
```

## Floyd-Warshall 算法框架

```java
public int[][] floydWarshall(int n, int[][] graph) {
    // 初始化距离矩阵
    int[][] dist = new int[n][n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                dist[i][j] = 0;
            } else if (graph[i][j] != 0) {
                dist[i][j] = graph[i][j];
            } else {
                dist[i][j] = Integer.MAX_VALUE;
            }
        }
    }
    
    // 动态规划，更新最短路径
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] != Integer.MAX_VALUE && dist[k][j] != Integer.MAX_VALUE) {
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }
    
    return dist;
}
```

## BFS 算法（无权图最短路径）

```java
public int[] bfsShortestPath(int n, List<List<Integer>> graph, int start) {
    // 存储从起点到各节点的最短距离
    int[] dist = new int[n];
    Arrays.fill(dist, -1);  // -1 表示不可达
    dist[start] = 0;
    
    // 队列
    Queue<Integer> queue = new LinkedList<>();
    queue.offer(start);
    
    while (!queue.isEmpty()) {
        int u = queue.poll();
        
        // 遍历所有邻居
        for (int v : graph.get(u)) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                queue.offer(v);
            }
        }
    }
    
    return dist;
}
```

## 适用场景

### Dijkstra 算法
- **适用场景**：单源最短路径问题，边权非负的图
- **时间复杂度**：O(E log V)，其中 E 是边数，V 是节点数

### Bellman-Ford 算法
- **适用场景**：单源最短路径问题，存在负权边的图
- **时间复杂度**：O(VE)

### Floyd-Warshall 算法
- **适用场景**：所有节点对之间的最短路径问题
- **时间复杂度**：O(V³)

### BFS 算法
- **适用场景**：无权图的最短路径问题
- **时间复杂度**：O(V + E)

## 注意事项

1. **图的表示**：可以使用邻接矩阵或邻接表来表示图
2. **初始化**：正确初始化距离数组，通常将起点的距离设为 0，其他节点的距离设为无穷大
3. **负权边**：Dijkstra 算法不支持负权边，需要使用 Bellman-Ford 算法
4. **负权环**：Bellman-Ford 算法可以检测负权环
5. **时间复杂度**：对于大规模图，需要选择合适的算法以保证效率

## 示例：网络延迟时间

### 题目描述

有 n 个网络节点，标记为 1 到 n。

给你一个列表 times，表示信号经过有向边的传递时间。 times[i] = (u, v, w)，其中 u 是源节点，v 是目标节点，w 是一个信号从源节点传递到目标节点的时间。

现在，从某个节点 K 发出一个信号。需要多久才能使所有节点都收到信号？如果不能使所有节点收到信号，返回 -1。

### 代码实现

```java
public int networkDelayTime(int[][] times, int n, int k) {
    // 构建邻接表
    List<List<int[]>> graph = new ArrayList<>();
    for (int i = 0; i <= n; i++) {
        graph.add(new ArrayList<>());
    }
    for (int[] time : times) {
        int u = time[0];
        int v = time[1];
        int w = time[2];
        graph.get(u).add(new int[]{v, w});
    }
    
    // 使用 Dijkstra 算法计算最短路径
    int[] dist = new int[n + 1];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[k] = 0;
    
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{k, 0});
    
    while (!pq.isEmpty()) {
        int[] current = pq.poll();
        int u = current[0];
        int currentDist = current[1];
        
        if (currentDist > dist[u]) {
            continue;
        }
        
        for (int[] neighbor : graph.get(u)) {
            int v = neighbor[0];
            int weight = neighbor[1];
            int newDist = currentDist + weight;
            
            if (newDist < dist[v]) {
                dist[v] = newDist;
                pq.offer(new int[]{v, newDist});
            }
        }
    }
    
    // 计算最大延迟时间
    int maxDelay = 0;
    for (int i = 1; i <= n; i++) {
        if (dist[i] == Integer.MAX_VALUE) {
            return -1;
        }
        maxDelay = Math.max(maxDelay, dist[i]);
    }
    
    return maxDelay;
}
```

### 解释

1. **构建邻接表**：将输入的边转换为邻接表表示
2. **初始化**：使用 Dijkstra 算法计算从节点 K 到所有其他节点的最短路径
3. **计算最大延迟时间**：找到从节点 K 到所有其他节点的最短路径中的最大值
4. **返回结果**：如果有节点不可达，返回 -1；否则返回最大延迟时间

## 示例：单词接龙

### 题目描述

字典 `wordList` 中从单词 `beginWord` 到 `endWord` 的转换序列是一个按下述规格形成的序列：

1. 序列中第一个单词是 `beginWord`。
2. 序列中每个相邻单词之间只有一个字母不同。
3. 序列中最后一个单词是 `endWord`。
4. 序列中的所有单词都在 `wordList` 中。

给你两个单词 `beginWord` 和 `endWord` 和一个字典 `wordList`，找到从 `beginWord` 到 `endWord` 的最短转换序列的长度。如果不存在这样的转换序列，返回 0。

### 代码实现

```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    // 将 wordList 转换为集合，提高查找效率
    Set<String> wordSet = new HashSet<>(wordList);
    if (!wordSet.contains(endWord)) {
        return 0;
    }
    
    // 使用 BFS 寻找最短路径
    Queue<String> queue = new LinkedList<>();
    queue.offer(beginWord);
    
    Set<String> visited = new HashSet<>();
    visited.add(beginWord);
    
    int level = 1;  // 初始 level 为 1（包含 beginWord）
    
    while (!queue.isEmpty()) {
        int size = queue.size();
        
        for (int i = 0; i < size; i++) {
            String current = queue.poll();
            
            // 生成所有可能的邻居
            List<String> neighbors = getNeighbors(current, wordSet);
            for (String neighbor : neighbors) {
                if (neighbor.equals(endWord)) {
                    return level + 1;
                }
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.offer(neighbor);
                }
            }
        }
        
        level++;
    }
    
    return 0;
}

// 生成所有可能的邻居
private List<String> getNeighbors(String word, Set<String> wordSet) {
    List<String> neighbors = new ArrayList<>();
    char[] chars = word.toCharArray();
    
    for (int i = 0; i < chars.length; i++) {
        char original = chars[i];
        for (char c = 'a'; c <= 'z'; c++) {
            if (c == original) {
                continue;
            }
            chars[i] = c;
            String newWord = new String(chars);
            if (wordSet.contains(newWord)) {
                neighbors.add(newWord);
            }
        }
        chars[i] = original;
    }
    
    return neighbors;
}
```

### 解释

1. **检查 endWord 是否在 wordList 中**：如果不在，直接返回 0
2. **使用 BFS 寻找最短路径**：
   - 初始化队列，将 beginWord 加入队列
   - 记录访问过的单词，避免重复访问
   - 遍历队列中的每个单词，生成所有可能的邻居
   - 如果邻居是 endWord，返回当前 level + 1
   - 如果邻居未被访问过，将其加入队列和访问集合
3. **返回结果**：如果队列为空仍未找到 endWord，返回 0

## 总结

最短路径算法是图论中的重要算法，广泛应用于网络路由、路径规划等领域。通过掌握这些算法的框架，你可以解决各种最短路径问题。在实际应用中，需要根据图的特点选择合适的算法，以保证效率和正确性。