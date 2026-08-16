---
problems:
  - title: 数组中的第 K 个最大元素
    url: https://leetcode.cn/problems/kth-largest-element-in-an-array/
    difficulty: medium
---

# 堆与前缀树

> 堆（优先队列）和 Trie（前缀树）——两种高频面试数据结构。配套：[专项·DFS/BFS](../../06-practice/dfs-bfs-practice-i/)（堆用于 BFS Top K）、[集合框架](../../../java/basics/collection)（PriorityQueue）。

---

## 堆

### 原理

堆是「**用数组实现的完全二叉树**」，满足：父节点 ≤ 子节点（小顶堆）或 父节点 ≥ 子节点（大顶堆）。

- 数组 `a[]` 表示：`a[i]` 的父是 `a[(i-1)/2]`，左子 `a[2i+1]`，右子 `a[2i+2]`。
- 堆顶（`a[0]`）是最小值（小顶堆）或最大值（大顶堆）。
- 插入：尾部加元素 → 向上调整（`siftUp`）。删除堆顶：末尾移到堆顶 → 向下调整（`siftDown`）。

### Java 实现：PriorityQueue

Java 的 `PriorityQueue` 就是堆（默认小顶堆）：

```java
// 小顶堆（默认）
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
// 大顶堆
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

minHeap.offer(3); minHeap.offer(1); minHeap.offer(2);
minHeap.peek();   // 1（堆顶最小）
minHeap.poll();    // 弹出 1
```

**面试几乎不要求手写堆**（`siftUp`/`siftDown`）——会用 `PriorityQueue` 就行。但要理解原理（问「PriorityQueue 底层是什么」→ 堆）。

### Top K 问题（最常考）

**「求数组第 K 大」——用小顶堆维护 K 个最大元素**：

```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>();   // 小顶堆
    for (int num : nums) {
        pq.offer(num);
        if (pq.size() > k) pq.poll();   // 堆顶是最小，淘汰它保留 K 大
    }
    return pq.peek();   // 堆顶 = 第 K 大
}
```

**为什么用小顶堆而不是大顶堆**？要找「第 K 大」，堆里维护 K 个元素，堆顶是这 K 个里**最小的**——就是第 K 大。如果用大顶堆，堆顶是最大的，淘汰它就错了。

**复杂度**：O(n log K)——每个元素入堆一次（log K），比排序 O(n log n) 快（K << n 时）。

### 易错点

- **小顶堆 vs 大顶堆选哪个**：求 **Top K 大**（最大 K 个）用**小顶堆**（淘汰最小的）；求 **Top K 小**（最小 K 个）用**大顶堆**（淘汰最大的）。口诀：**「找大的用小堆，找小的用大堆」**。反了就全错。
- **`PriorityQueue` 不是 FIFO**——按优先级出（堆）。当普通队列用 `poll` 会发现不是先进先出。
- **堆排序**：建堆 O(n) + 每次弹堆顶 O(log n) × n = O(n log n)。不如快排（常数大），但适合「只取前 K」的场景（O(n log K)）。

---

## 前缀树（Trie）

### 原理

多叉树，每条从根到节点的路径代表一个字符串的**前缀**。根不存字符，每条边代表一个字符。

```
        root
       / | \
      a  b  c
     /       \
    p         a
   /           \
  p             t
 /
($)
```
（存了 "app" 和 "cat"）

### Java 实现

```java
class Trie {
    static class Node {
        Node[] children = new Node[26];   // 26 个字母（或用 HashMap 支持任意字符）
        boolean isEnd;
    }
    private Node root = new Node();

    public void insert(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) cur.children[i] = new Node();
            cur = cur.children[i];
        }
        cur.isEnd = true;
    }

    public boolean search(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) return false;
            cur = cur.children[i];
        }
        return cur.isEnd;     // 必须 isEnd（"app" 存了不代表 "ap" 存了）
    }

    public boolean startsWith(String prefix) {
        Node cur = root;
        for (char c : prefix.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) return false;
            cur = cur.children[i];
        }
        return true;          // 只要走到这，前缀就存在
    }
}
```

### 易错点

- **`search` 和 `startsWith` 的区别**：`search` 要求**完整单词**（`isEnd == true`）；`startsWith` 只要求**前缀存在**（走到就行）。Trie 存了 "app"，`search("ap")` 返回 **false**（"ap" 不是完整词），`startsWith("ap")` 返回 **true**。新手常把 search 写成 startsWith。
- **`children` 用数组还是 HashMap**：如果只有小写字母（a-z），用 `Node[26]`（快、省内存）；如果有任意字符（中文/大写/数字），用 `HashMap<Character, Node>`（灵活但慢）。面试题一般 26 字母，用数组。
- **空间复杂度**：Trie 比直接存字符串**更费内存**（每个字符一个 Node）。但查询前缀快（O(L)，L 是字符串长度）。

### 应用

自动补全（输入 "ap" 提示 "app"/"apple"/"apply"）、拼写检查、IP 路由（最长前缀匹配）、LC 208 实现 Trie、LC 212 单词搜索 II。

---

## 面试高频

| 数据结构 | 高频考法 |
|---|---|
| 堆 | Top K 大/小（小顶堆/大顶堆选择）、合并 K 个有序链表、数据流中位数（大+小双堆）|
| Trie | 实现前缀树（LC 208）、单词搜索 II（LC 212）、自动补全 |

> 堆的核心是「**找大的用小堆，找小的用大堆**」（维护 K 个元素）；Trie 的核心是「前缀共享——公共前缀只存一次」。进阶刷题见 [专项练习](../../06-practice/)。
