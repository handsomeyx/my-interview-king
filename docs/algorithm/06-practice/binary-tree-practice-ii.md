---
title: 二叉树专项练习 II（构造与路径）
---

# 二叉树专项练习 II（构造与路径）

> 配套：[二叉树 I（基础遍历）](./binary-tree-practice-i/)。本篇讲二叉树的进阶——**构造树**（从遍历序列重建）和**路径问题**（最大路径和、路径总数）。这些题的共同骨架是**后序**：当前节点的结果依赖左右子树的结果回传。区别在三件事：**递归返回什么（构造的子树 / 标记 / 单枝贡献）**、**全局答案在哪里更新**、**子问题怎么切分**。

## 框架速记

```text
// 构造类：递归返回「建好的子树根」
TreeNode build(子问题边界) {
    if (边界空) return null;
    TreeNode root = new TreeNode(根值);
    root.left  = build(左子问题边界);
    root.right = build(右子问题边界);
    return root;
}

// 后序回传类：递归返回「当前节点的贡献」，过程中更新全局 ans
int dfs(node) {
    if (node == null) return 0;
    int l = dfs(node.left);
    int r = dfs(node.right);
    ans = max(ans, 用 l, r, node.val 组合);   // ← 全局更新
    return 只选一边的贡献;                     // ← 给父节点
}
```

三个钩子：**递归返回值（子树 / 标记 / 贡献）**、**全局答案更新位置**、**子问题边界切分**。

## 题目清单

> 精讲 1/2/3 三道，其余给出变化点供自行练习。

| # | 题目 | 难度 | 框架变化点 |
|---|---|---|---|
| 1 | [从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | 中 | 前序定根，中序分左右 |
| 2 | [从中序与后序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) | 中 | 同 1，后序定根（末尾） |
| 3 | [二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/) | 中 | 后序：左右回传标记 |
| 4 | [二叉搜索树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 简 | 利用 BST 性质，迭代往下 |
| 5 | [二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/) | 困 | 后序：单枝贡献 + 全局更新 |
| 6 | [路径总和 III](https://leetcode.cn/problems/path-sum-iii/) | 中 | 前缀和 + 回溯 |
| 7 | [验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/) | 中 | 传递 (min, max) 区间 |
| 8 | [把二叉搜索树转换为累加树](https://leetcode.cn/problems/convert-bst-to-greater-tree/) | 中 | 反中序（右→根→左）累加 |
| 9 | [二叉搜索树中的插入操作](https://leetcode.cn/problems/insert-into-a-binary-search-tree/) | 中 | BST 找位插入 |
| 10 | [删除二叉搜索树中的节点](https://leetcode.cn/problems/delete-node-in-a-bst/) | 中 | BST 删除 + 后继替换 |

---

## 例题 1：从前序与中序构造二叉树（LC 105，构造）

**题目**：给定前序 `preorder` 和中序 `inorder`，重建二叉树（值不重复）。

**如何套 + 变化点**：前序「根左右」，首元素一定是根。在中序里找到根的位置，左边是左子树、右边是右子树。递归对左右子树各做一遍。用 HashMap 存「值→中序下标」，O(1) 找根，避免每层 O(n) 扫。

```java
private int[] preorder;
private Map<Integer, Integer> inIndex = new HashMap<>();
public TreeNode buildTree(int[] preorder, int[] inorder) {
    this.preorder = preorder;
    for (int i = 0; i < inorder.length; i++) inIndex.put(inorder[i], i);
    return build(0, 0, inorder.length - 1);
}
private TreeNode build(int preRoot, int inLeft, int inRight) {
    if (inLeft > inRight) return null;
    TreeNode root = new TreeNode(preorder[preRoot]);
    int inRoot = inIndex.get(preorder[preRoot]);
    int leftSize = inRoot - inLeft;
    root.left  = build(preRoot + 1, inLeft, inRoot - 1);
    root.right = build(preRoot + leftSize + 1, inRoot + 1, inRight);
    return root;
}
```

**易错点**：
- **右子树在前序里的根下标是 `preRoot + leftSize + 1`**，不是 `preRoot + 1`。左子树在前序里占 `leftSize` 个位置（紧跟根），右子树根要跳过左子树。这是这题最容易算错的地方。
- 用 `inLeft > inRight` 判空（中序区间空），**不是 `preRoot >= preorder.length`**。前序根下标天然不会越界（由中序区间长度保证），用中序区间判空才对。

---

## 例题 2：最近公共祖先（LC 236，后序标记）

**题目**：找二叉树中 p 和 q 的最近公共祖先（LCA）。

**为什么后序**：LCA 必须等「左右子树都查过」才能判断当前节点是不是 LCA。如果 p、q 都在左子树 → LCA 在左子树（返回左结果）；都在右子树 → 在右子树；分两侧 → 当前节点就是 LCA。这种「依赖子树结果回传」正是后序。

**如何套 + 变化点**：dfs 返回「以当前节点为根的子树里，p 或 q 是否出现（返回那个节点，没找到返回 null）」。当前节点本身就是 p 或 q 直接返回自己；否则看左右回传——都非 null 说明分两侧，当前是 LCA；一侧非 null 说明两个都在那侧，返回那侧。

```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left == null) return right;   // 左没找到，结果在右
    if (right == null) return left;   // 右没找到，结果在左
    return root;                       // 两侧都非 null：当前是 LCA
}
```

**易错点**：
- **base case 顺序**：先判 `root == null`，再判 `root == p || root == q`。反了会在 null 上取 val 抛 NPE。
- `if (left == null) return right` 和 `if (right == null) return left` **不是 if-else**，是两个独立判断 + 末尾 return。两个都判完才确定 LCA，写成 if-else 会漏「两侧都非 null」的情况（直接返回 left 漏掉 root）。
- 这个解法**依赖 p、q 都在树里**。题目保证如此。如果可能不存在，得加额外校验（先搜一遍确认）。

---

## 例题 3：二叉树中的最大路径和（LC 124，后序贡献）

**题目**：二叉树每个节点有权重（可能负），找任意节点到任意节点的路径（不能分叉），使其权和最大。

**为什么贡献只取单枝**：路径不能「分叉」——一条路径到了某节点要么继续往上（走父节点），要么在此终止，不能既走左子又走右子（那是两条路径）。所以递归返回给父节点的贡献只能**选左或右较大者**，不能左右都带。但「以当前节点为最高点」的路径**可以同时走左右**（因为这是终点，不再上行），所以全局 ans 用「左贡献 + 右贡献 + 当前值」。

**如何套 + 变化点**：dfs 返回「以当前节点为终点、向上的单枝最大贡献」`max(左贡献, 右贡献, 0) + node.val`；过程中用 `node.val + 左贡献 + 右贡献` 更新全局 maxSum。

```java
private int maxSum = Integer.MIN_VALUE;
public int maxPathSum(TreeNode root) {
    gain(root);
    return maxSum;
}
private int gain(TreeNode node) {
    if (node == null) return 0;
    int leftGain  = Math.max(gain(node.left), 0);
    int rightGain = Math.max(gain(node.right), 0);
    maxSum = Math.max(maxSum, node.val + leftGain + rightGain);  // 当前为最高点
    return node.val + Math.max(leftGain, rightGain);             // 向上的单枝贡献
}
```

**易错点**：
- `maxSum` 初始 `Integer.MIN_VALUE`，**不是 0**。节点值可能全负（如 `[-3]`），最大路径和是负数，初始 0 会错返回 0。
- `Math.max(gain(...), 0)` —— **负贡献按 0 处理**。子树贡献为负时宁可不走（贡献 0，相当于从此节点重新开始）。漏掉 `max(..., 0)` 会被负子树拖累，错算成负路径。
- 返回给父的是 `node.val + max(leftGain, rightGain)`（**单枝**），但更新全局用的是 `node.val + leftGain + rightGain`（**双枝**）。两者不能混——返回单枝是为了「不分叉地向上」，全局双枝是「以此为终点」。写反会让父节点拿到双枝贡献，路径分叉，违反定义。

---

## 练习建议

按范式分组：
- 构造（递归返回子树根）：1、2
- LCA（后序标记回传）：3、4
- 路径（贡献 + 全局更新）：5、6
- BST 操作（利用有序性）：7、8、9、10

**如果时间只够做 3 道**：做 **1、3、5**——分别覆盖「构造 / LCA / 路径和」三种后序进阶范式。2 是 1 的镜像（后序定根），4 是 3 的 BST 简化（迭代），6 是 5 加前缀和。BST 那几道（7-10）可以单练，是「利用有序性」的另一条线。

## 下一步

本篇覆盖构造与路径（后序进阶）；剩下 7 道的变化点已在表格列出。BST 系列题（7-10）值得单独花时间，它们是「利用二叉搜索树有序性」的集中训练。卡题时回看 [二叉树 I](./binary-tree-practice-i/) 和本篇的「三个钩子」，对照「递归返回什么、全局在哪更新、子问题怎么切」。

## 做完之后试试

1. **盖住答案重新做一遍**：不看本文的解法提示，你能在 20 分钟内独立写出来吗？
2. **用一句话讲清楚**：如果让你给面试官讲这道题的思路，你会怎么说？（不能直接念代码）
3. **举一反三**：这道题的思路可以用来解决哪些其他题？（可以回头看看对应框架章节的内容）
