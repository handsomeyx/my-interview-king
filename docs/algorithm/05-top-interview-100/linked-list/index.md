---
problems:
  - title: 反转链表
    url: https://leetcode.cn/problems/reverse-linked-list/
    difficulty: easy
  - title: 合并两个有序链表
    url: https://leetcode.cn/problems/merge-two-sorted-lists/
    difficulty: easy
  - title: 链表的中间节点
    url: https://leetcode.cn/problems/middle-of-the-linked-list/
    difficulty: easy
  - title: 环形链表
    url: https://leetcode.cn/problems/linked-list-cycle/
    difficulty: easy
---

# 链表类 Top 题

链表是一种常见的数据结构，在面试中经常出现。本章节将介绍链表类的高频面试题，包括链表的基本操作、链表的反转、链表的环检测等。

## 1. 反转链表

### 题目描述

反转一个单链表。

### 示例

```
输入：1->2->3->4->5->NULL
输出：5->4->3->2->1->NULL
```

### 解题思路

- **迭代**：使用三个指针（prev、current、next）来反转链表
- **递归**：递归地反转链表的剩余部分

### 代码实现

```java
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        while (current != null) {
            ListNode nextTemp = current.next;
            current.next = prev;
            prev = current;
            current = nextTemp;
        }
        return prev;
    }
}

// 测试示例
// 输入: 1->2->3->4->5->NULL
// 输出: 5->4->3->2->1->NULL
```

## 2. 合并两个有序链表

### 题目描述

将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

### 示例

```
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

### 解题思路

- **迭代**：使用虚拟头节点，比较两个链表的节点值，将较小的节点添加到新链表中
- **递归**：递归地比较两个链表的节点值，将较小的节点作为新链表的头节点

### 代码实现

```java
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        // 虚拟头节点
        ListNode dummy = new ListNode(-1);
        ListNode current = dummy;
        
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) {
                current.next = l1;
                l1 = l1.next;
            } else {
                current.next = l2;
                l2 = l2.next;
            }
            current = current.next;
        }
        
        // 处理剩余节点
        if (l1 != null) {
            current.next = l1;
        }
        if (l2 != null) {
            current.next = l2;
        }
        
        return dummy.next;
    }
}

// 测试示例
// 输入: l1 = [1,2,4], l2 = [1,3,4]
// 输出: [1,1,2,3,4,4]
```

## 3. 链表的中间节点

### 题目描述

给定一个头结点为 `head` 的非空单链表，返回链表的中间结点。

如果有两个中间结点，则返回第二个中间结点。

### 示例

```
输入：[1,2,3,4,5]
输出：此列表中的结点 3 (序列化形式：[3,4,5])

输入：[1,2,3,4,5,6]
输出：此列表中的结点 4 (序列化形式：[4,5,6])
```

### 解题思路

- **快慢指针**：使用快慢指针，快指针每次走两步，慢指针每次走一步，当快指针到达链表末尾时，慢指针指向的就是中间节点

### 代码实现

```java
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public ListNode middleNode(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }
}

// 测试示例
// 输入: [1,2,3,4,5]
// 输出: 3
// 输入: [1,2,3,4,5,6]
// 输出: 4
```

## 4. 链表中倒数第 k 个节点

### 题目描述

输入一个链表，输出该链表中倒数第k个节点。为了符合大多数人的习惯，本题从1开始计数，即链表的尾节点是倒数第1个节点。

### 示例

```
输入：1->2->3->4->5, k = 2
输出：4
```

### 解题思路

- **快慢指针**：使用快慢指针，快指针先走k步，然后快慢指针同时走，当快指针到达链表末尾时，慢指针指向的就是倒数第k个节点

### 代码实现

```java
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public ListNode getKthFromEnd(ListNode head, int k) {
        ListNode slow = head;
        ListNode fast = head;
        
        // 快指针先走 k 步
        for (int i = 0; i < k; i++) {
            if (fast == null) {
                return null;
            }
            fast = fast.next;
        }
        
        // 快慢指针同时走
        while (fast != null) {
            slow = slow.next;
            fast = fast.next;
        }
        
        return slow;
    }
}

// 测试示例
// 输入: 1->2->3->4->5, k = 2
// 输出: 4
```

## 5. 环形链表

### 题目描述

给定一个链表，判断链表中是否有环。

### 示例

```
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。

输入：head = [1,2], pos = 0
输出：true
解释：链表中有一个环，其尾部连接到第一个节点。

输入：head = [1], pos = -1
输出：false
解释：链表中没有环。
```

### 解题思路

- **快慢指针**：使用快慢指针，快指针每次走两步，慢指针每次走一步，如果链表有环，快慢指针最终会相遇

### 代码实现

```java
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                return true;
            }
        }
        return false;
    }
}

// 测试示例
// 输入: head = [3,2,0,-4], pos = 1
// 输出: true
// 输入: head = [1,2], pos = 0
// 输出: true
// 输入: head = [1], pos = -1
// 输出: false
```

## 总结

链表类的高频面试题主要包括：

1. **链表的基本操作**：反转链表、合并两个有序链表
2. **链表的查找**：链表的中间节点、链表中倒数第 k 个节点
3. **链表的环检测**：环形链表

这些题目涵盖了链表的常见操作和技巧，掌握这些题目对于应对面试中的链表相关问题非常有帮助。