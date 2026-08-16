---
title: 二叉树专项练习 I（基础遍历）
---

# 二叉树专项练习 I（基础遍历）

> 配套：[数据结构·树](../02-data-structures/tree/)、[DFS/BFS 框架](../00-algorithm-frameworks/dfs-bfs/)。二叉树的所有题，骨架就一个——**遍历**。区别只在三件事：**用哪种遍历（前/中/后/层）、遍历到每个节点时做什么、结果在哪里汇总**。下面精讲 3 道覆盖三种遍历范式（迭代中序 / 层序 BFS / 后序回溯），再给 7 道变化点清单。

## 框架速记

```text
// 递归（前/中/后序只换 add 位置）
void traverse(TreeNode root) {
    if (root == null) return;
    // 前序：这里访问 root
    traverse(root.left);
    // 中序：这里访问 root
    traverse(root.right);
    // 后序：这里访问 root
}

// 层序（BFS，队列）
Queue<TreeNode> q = new LinkedList<>();
q.offer(root);
while (!q.isEmpty()) {
    int size = q.size();           // ← 每层开始前取
    for (int i = 0; i < size; i++) { /* 出队访问，子节点入队 */ }
}
```

三个钩子：**遍历方式（前/中/后/层）**、**访问时机**、**结果汇总位置**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/) | 简 | 迭代：栈模拟，一路左压栈 |
| 2 | [二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/) | 中 | BFS，逐层 size 控制 |
| 3 | [二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) | 简 | 后序：左右深 +1 |
| 4 | [平衡二叉树](https://leetcode.cn/problems/balanced-binary-tree/) | 简 | 后序：左右高差 ≤1 |
| 5 | [对称二叉树](https://leetcode.cn/problems/symmetric-tree/) | 简 | 双指针递归：左左 vs 右右 |
| 6 | [翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/) | 简 | 前序或后序：交换两子 |
| 7 | [二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/) | 简 | 后序：左右深度之和 |
| 8 | [合并二叉树](https://leetcode.cn/problems/merge-two-binary-trees/) | 简 | 前序：同位相加 |
| 9 | [路径总和](https://leetcode.cn/problems/path-sum/) | 简 | 前序 + 叶子判断 |
| 10 | [填充每个节点的下一个右侧节点指针](https://leetcode.cn/problems/populating-next-right-pointers-in-each-node/) | 中 | BFS，层内串接 |

---

## 例题 1：二叉树的中序遍历（LC 94，迭代）

**题目**：返回二叉树的中序遍历结果（左→根→右）。

**如何套 + 变化点**：递归中序最简（换 add 位置即可），但面试常考**迭代**。迭代用栈模拟：一路把左子压栈到底，pop 时访问，再转右子。

```java
public List<Integer> inorderTraversal(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode cur = root;
    while (cur != null || !stack.isEmpty()) {
        while (cur != null) {        // 一路左压栈
            stack.push(cur);
            cur = cur.left;
        }
        cur = stack.pop();           // pop 时访问
        res.add(cur.val);
        cur = cur.right;             // 转右子
    }
    return res;
}
```

**易错点**：
- 外层循环条件是 `cur != null || !stack.isEmpty()`，**两个用 `||` 不是 `&&`**。`&&` 会在 cur 转右为 null 但栈里还有节点时提前结束，漏遍历。正确语义是「还有路可走（cur）或还有节点待访问（栈）」。
- **访问时机是 `pop` 之后**，不是 `push` 时。push 时节点还没轮到（中序要先走完左子）；pop 意味着左子已处理完，轮到根。

---

## 例题 2：二叉树的层序遍历（LC 102，BFS）

**题目**：自顶而下、从左到右，逐层返回节点值。

**如何套 + 变化点**：标准 BFS，但要点是「**逐层**」——每层开始前先取 `size = q.size()`，按 size 出队。不取 size 就是普通 BFS（拍平成一维）。

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while (!q.isEmpty()) {
        int size = q.size();            // ← 进入层循环前取
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

**易错点**：
- `size` 必须**进入层循环前取一次**，循环里用 `i < size`。**不要写 `i < q.size()`**——队列在循环中不断 offer 子节点，`q.size()` 实时变，for 会跑飞，一层混进下一层的节点。
- **空子节点不入队**（`if (n.left != null)`）。null 入队后 poll 出来再 `.left` 会 NPE，且污染层级。

---

## 例题 3：二叉树的直径（LC 543，后序）

**为什么必须后序**：直径的定义是「树上任意两节点间路径的最长边数」。这条最长路径一定**经过某个节点 X 作为最高点**，长度 = X 的左子深度 + 右子深度。要知道 X 的左右深度，**必须等左右子树都算完**——这就是后序。前序时根先于子树，根本不知道左右有多深，算不出直径。

**如何套 + 变化点**：后序 DFS，函数返回「当前节点的最大单枝深度」（节点数）；过程中用「左深 + 右深 + 1」更新直径最大值（节点数），最后减 1 转边数。

```java
private int ans = 1;   // 直径（节点数），至少含根 1 个
public int diameterOfBinaryTree(TreeNode root) {
    depth(root);
    return ans - 1;    // 节点数 - 1 = 边数
}
private int depth(TreeNode node) {
    if (node == null) return 0;
    int l = depth(node.left);
    int r = depth(node.right);
    ans = Math.max(ans, l + r + 1);      // 经过当前节点的最长路径（节点数）
    return Math.max(l, r) + 1;            // 当前节点最大单枝深度
}
```

**易错点**：
- `ans` 必须**用实例变量（成员字段）或数组引用**，不能当参数传。Java 方法参数是值传递，递归深处更新的 ans 带不回上层。
- 直径的「单位」最容易绕。LC 543 要返回**边数**，但内部用**节点数**算（`l + r + 1`）更直观，最后 `return ans - 1`。如果直接按边数算（`l + r`），单节点树返回 0 是对的，但写 `l + r + 1` 会多 1——务必让「内部单位」和「返回单位」一致，写错就差 1。
- `return Math.max(l, r) + 1` 是给**父节点**用的（父节点的单枝深度 = 本节点最大枝 +1）。漏了 `+1` 会让整棵树深度算少，直径跟着错。

**对比**：例 1/2 是「遍历到就处理」，例 3 是「左右子结果回来后才处理」——这就是「遍历」和「后序回溯」的区别。

---

## 练习建议

按遍历范式分组：
- 迭代遍历（栈）：1（中序，必会迭代写法）
- 层序 BFS：2、10
- 后序回溯（深度/差/直径）：3、4、7
- 前序改造树：5、6、8
- 前序 + 叶子判断：9

**如果时间只够做 3 道**：做 **1、2、7**——分别覆盖「迭代中序 / 层序 BFS / 后序回溯」三种遍历范式，做完二叉树基础遍历的主干就拿下了，其余题都是这三种的变体（5/6/8 是前序换访问动作，3/4 是 7 的简化）。

## 下一步

二叉树专项 II 会讲后序的进阶（构造、最近公共祖先、路径和）。本篇覆盖基础遍历；剩下 7 道的变化点已在表格列出。卡题时回看 [DFS/BFS 框架](../00-algorithm-frameworks/dfs-bfs/)，对照「遍历方式 + 访问时机 + 汇总位置」三处钩子。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
