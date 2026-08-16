# 线性结构

> 数组、链表、栈、队列——四大基础线性结构。本文讲「原理 + Java 实现 + 面试易错点」，不是空泛的优缺点对比。配套：[刷题专项·链表类 Top 题](../../05-top-interview-100/linked-list/)。

---

## 数组

### 原理

连续内存 + 索引访问。`a[i]` 的地址 = 基址 + i × 元素大小，所以 O(1) 随机访问。代价：插入/删除中间元素要搬移后续（O(n)），大小固定（动态数组靠扩容）。

### Java 实现：ArrayList

ArrayList 是「动态数组」——底层 `Object[] elementData`，容量不够时扩容。

```java
// ArrayList 扩容核心（JDK 8+）
private int newCapacity(int minCapacity) {
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + (oldCapacity >> 1);  // 1.5 倍
    return newCapacity;
}
```

### 易错点

- **ArrayList 默认容量 10**（首次 add 才分配，不是 new 时），**扩容 1.5 倍**（`oldCap + oldCap >> 1`）。HashMap 扩容 2 倍，别混。
- **随机访问 O(1)**（下标），但**中间插入/删除 O(n)**（搬移）。频繁中间增删该用 LinkedList？不一定（见下）。
- **`subList` 返回视图**（改子表影响原表），不是副本——很多人踩坑。

## 链表

### 原理

非连续存储，节点（value + next）串起来。单链表（只 next）、双向链表（prev + next）、循环链表（尾指头）。

插入/删除 O(1)（改指针），但**前提是已定位到位置**；随机访问 O(n)（从头遍历）。

### Java 实现：手写单链表反转

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

// 反转链表（迭代，三指针）
ListNode reverse(ListNode head) {
    ListNode prev = null, cur = head;
    while (cur != null) {
        ListNode next = cur.next;
        cur.next = prev;
        prev = cur;
        cur = next;
    }
    return prev;
}
```

### Java 的 LinkedList

`java.util.LinkedList` 是**双向链表**（同时实现 List 和 Deque）。但实际项目几乎不用它做 List（见下「ArrayList vs LinkedList 实战」）。

### 易错点

- **虚拟头节点（dummy）**：链表题（删除/插入头、合并）用 dummy 简化边界，不用单独处理头。
- **快慢指针**：找中点（快 2 慢 1）、判环（快慢相遇）、删倒数第 N（快先走 N 步）。
- **ArrayList vs LinkedList 实战**：教科书说「频繁增删用 LinkedList」——实际**几乎总选 ArrayList**。理由：LinkedList「插入 O(1)」要求已定位，但 `list.add(index, e)` 要先遍历到 index（O(n)），整体仍 O(n)；且 ArrayList 内存连续、CPU 缓存友好，实测复杂度相同时也快几倍。详见 [集合框架](../../../java/basics/collection) Q10。

## 栈

### 原理

后进先出（LIFO）。只在栈顶压入/弹出。

### Java 实现

```java
Deque<Integer> stack = new ArrayDeque<>();   // 推荐
stack.push(1);     // 压栈
stack.pop();       // 弹栈
stack.peek();      // 查看栈顶
```

### 易错点

- **别用 `java.util.Stack`**：它继承 Vector、每个方法 synchronized，性能差。JDK 官方推荐用 **`ArrayDeque` 当栈**（数组实现，更快）。
- **栈的经典应用**：括号匹配（LC 20）、表达式求值、单调栈（下一个更大元素 LC 496、柱状图最大矩形 LC 84）、DFS 非递归、函数调用栈。
- **单调栈**是栈最难的应用——核心「栈里维护单调性，遇到破坏者就弹出处理」。见 [优化算法](../../03-algorithm-patterns/optimization/)。

## 队列

### 原理

先进先出（FIFO）。队尾入、队头出。

### Java 实现

```java
Queue<Integer> q = new ArrayDeque<>();       // 普通队列
q.offer(1);   // 入队
q.poll();     // 出队
q.peek();     // 查看队头

// 阻塞队列（生产者-消费者）
BlockingQueue<String> bq = new LinkedBlockingQueue<>();

// 优先队列（堆）
PriorityQueue<Integer> pq = new PriorityQueue<>();   // 默认小顶堆
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());  // 大顶堆
```

### 易错点

- **ArrayDeque vs LinkedList 当队列**：ArrayDeque 更快（数组 + 缓存友好），LinkedList 慢。优先 ArrayDeque。
- **PriorityQueue 不是 FIFO**——按优先级出（堆）。默认小顶堆，大顶堆传 `Comparator.reverseOrder()`。
- **阻塞队列**（LinkedBlockingQueue / ArrayBlockingQueue）用于生产者-消费者，`put`/`take` 阻塞。**线程池的 workQueue 就是它**（见 [并发·线程池](../../../java/concurrent/thread-pool)）。

---

## 面试高频：线性结构怎么考

| 结构 | 高频考法 |
|---|---|
| 数组 | 双指针、前缀和、差分、滑动窗口 |
| 链表 | 反转、合并、判环、找中点、LRU（双向链表+HashMap） |
| 栈 | 括号匹配、单调栈、表达式求值、DFS |
| 队列 | BFS 层序、单调队列（滑动窗口最大值 LC 239）、堆（Top K） |

> 线性结构本身简单，**难的是组合应用**（HashMap = 数组+链表+红黑树；LRU = 双向链表+HashMap；单调栈 = 栈+贪心）。掌握基础 + 刷组合题，才是面试的考法。进阶刷题见 [专项练习](../../06-practice/)。
