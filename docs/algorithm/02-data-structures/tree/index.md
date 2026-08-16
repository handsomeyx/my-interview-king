# 树形结构

> 二叉树、BST、红黑树、B+树——四大面试核心树结构。本文讲「原理 + Java 实现 + 易错点」，不是空泛列举。配套：[专项·二叉树练习](../../06-practice/binary-tree-practice-i/)。

---

## 二叉树

### 定义 + Java 表示

```java
class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}
```

### 四种遍历

| 遍历 | 顺序 | 递归位置 | 经典用途 |
|---|---|---|---|
| 前序 | 根→左→右 | 处理在「递归前」 | 拷贝树、序列化 |
| 中序 | 左→根→右 | 处理在「两次递归间」 | BST 得到有序序列 |
| 后序 | 左→右→根 | 处理在「递归后」 | 高度、直径、删除树 |
| 层序 | 上→下、左→右 | BFS 队列 | 层级统计 |

```java
// 递归框架（三种遍历只换 print 位置）
void traverse(TreeNode root) {
    if (root == null) return;
    // 前序位置：System.out.println(root.val);
    traverse(root.left);
    // 中序位置：System.out.println(root.val);
    traverse(root.right);
    // 后序位置：System.out.println(root.val);
}

// 层序（BFS）
List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new ArrayDeque<>();
    q.offer(root);
    while (!q.isEmpty()) {
        int size = q.size();               // ← 每层前取
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode n = q.poll();
            level.add(n.val);
            if (n.left != null) q.offer(n.left);
            if (n.right != null) q.offer(n.right);
        }
        res.add(level);
    }
    return res;
}
```

### 易错点

- **前序 = 自顶向下**（先处理根再递归子树，适合「传参向下」——如求深度用参数传递）；**后序 = 自底向上**（先递归子树再处理根，适合「收集子树结果」——如求高度用返回值）。选错遍历方向，代码写不出来。
- **层序 `size` 在层循环前取一次**，不是 `i < q.size()`（队列在变）。见 [DFS/BFS 练习](../../06-practice/dfs-bfs-practice-i/) Q2。
- **空树 `root == null`** 的 base case 容易漏，导致 NPE。

---

## 二叉搜索树（BST）

### 性质

左子树所有值 < 根 < 右子树所有值。**中序遍历得到升序序列**（这是 BST 最有用的性质）。

### 增删查

```java
// 查
TreeNode search(TreeNode root, int val) {
    while (root != null && root.val != val) {
        root = val < root.val ? root.left : root.right;
    }
    return root;
}

// 删（最复杂——三情况）
TreeNode delete(TreeNode root, int key) {
    if (root == null) return null;
    if (key < root.val) root.left = delete(root.left, key);
    else if (key > root.val) root.right = delete(root.right, key);
    else {
        // 情况 1/2：只有一子或无子
        if (root.left == null) return root.right;
        if (root.right == null) return root.left;
        // 情况 3：两子都有——找右子树最小值替换，再删右子树最小值
        TreeNode min = root.right;
        while (min.left != null) min = min.left;
        root.val = min.val;
        root.right = delete(root.right, min.val);
    }
    return root;
}
```

### 易错点

- **删除的三情况**：无子（直接删）、一子（子顶上）、两子（找右子树**最小值**替换 + 递归删右子树最小值）。两子情况最常考，也是最常写错的——用「前驱」（左子树最大值）也行，但约定俗成用「后继」（右子树最小值）。
- **BST 可能退化成链表**（有序插入 → 每个节点只有右子 → 高度 n → 查找 O(n)）。这就是为什么需要平衡树（AVL / 红黑树）。

---

## 红黑树

### 为什么不用 AVL（先讲为什么）

AVL 树严格平衡（左右高差 ≤1），查询极快（高度 log n 很矮）。但**插入/删除时旋转多**（可能一路旋到根），写密集场景开销大。红黑树**弱平衡**（保证最长路径 ≤2×最短路径），查询比 AVL 略慢（高一点），但**插入/删除旋转少**——综合更好。

**一句话**：AVL 查询优先（读多写少），红黑树综合优先（读写均衡）。Java 的 TreeMap/HashMap 桶树化都用红黑树。

### 五大性质

1. 节点非红即黑。
2. 根是黑。
3. 叶子（NIL）是黑。
4. 红节点的子必须是黑（不能连续两个红）。
5. 任一节点到其所有叶子的路径，**黑节点数相同**（叫「黑高」）。

### 易错点

- **面试不要求手写红黑树**（几十行旋转 + 染色，记不住），但要答出：五条性质、为什么用红黑不用 AVL（上面那段）、用在哪（Java TreeMap/HashMap 桶树化、C++ STL map/set、Linux CFS 调度器、epoll）。
- **HashMap 桶树化阈值 8** 不是红黑树的规定，是 HashMap 的选择（泊松分布下冲突到 8 的概率极低）。见 [集合框架](../../../java/basics/collection) Q1。

---

## B+树

### 为什么数据库索引用 B+树（不是红黑树/AVL/B 树）

红黑树/AVL 是**二叉**树——每个节点最多 2 子，千万数据要 20+ 层，**磁盘 IO 20+ 次**。B+树是**多叉**树（每节点几百子），千万数据只需 3 层，**3 次 IO**。

B+树 vs B 树：
- B 树：非叶子**也存数据**。范围查询要中序遍历多棵子树，IO 多。
- B+树：**所有数据都在叶子 + 叶子间链表**。范围查询定位起点后沿链表顺序扫，IO 少。且非叶子只存索引，一个节点能放更多 key → 树更矮。

**一句话**：B+树 = 多叉（树矮 IO 少）+ 叶子链表（范围查询快），完美匹配数据库场景。

### 易错点

- **B+树的非叶子不存数据**（只存索引用于路由），B 树的非叶子**也存数据**。这是两者最核心区别。
- **B+树叶子链表**是范围查询（`between`/`>`）快的关键——叶子层顺序扫，不用回溯。这是 MySQL InnoDB 索引选 B+树的根本原因。详见 [MySQL 索引](../../../java/mysql/indexing) Q1。

---

## 面试高频：树结构怎么考

| 树型 | 高频考法 |
|---|---|
| 二叉树 | 遍历（递归/迭代）、最大深度、直径、层序、路径总和、最近公共祖先 |
| BST | 验证 BST、删除节点、第 K 小、修剪 BST |
| 红黑树 | 性质 + 用在哪（不手写） |
| B+树 | 为什么数据库用、vs B 树、vs 红黑树 |
| Trie | 前缀匹配、自动补全（见 [堆与前缀树](../heap-and-trie/)） |

> 树的核心思维是**递归**——「当前节点做什么 + 左右子树递归」。掌握递归框架（前/中/后序的三个位置），树题就通了一半。进阶刷题见 [专项·二叉树 I/II](../../06-practice/binary-tree-practice-i/)。
