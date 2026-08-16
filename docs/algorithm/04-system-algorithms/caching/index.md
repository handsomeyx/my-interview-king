---
problems:
  - title: LRU 缓存
    url: https://leetcode.cn/problems/lru-cache/
    difficulty: medium
  - title: LFU 缓存
    url: https://leetcode.cn/problems/lfu-cache/
    difficulty: hard
---

# 缓存算法

缓存是提高系统性能的重要手段，而缓存替换算法则决定了在缓存容量有限的情况下，如何选择要淘汰的缓存项。本章节将介绍常见的缓存替换算法，包括LRU和LFU。

## LRU (Least Recently Used)

### 基本概念

LRU（最近最少使用）算法是一种基于访问时间的缓存替换算法，当缓存容量达到上限时，优先淘汰最久未被访问的缓存项。

### 工作原理

1. 维护一个双向链表，记录缓存项的访问顺序
2. 当访问一个缓存项时，将其移到链表头部
3. 当缓存容量达到上限时，淘汰链表尾部的缓存项

### 实现

使用哈希表和双向链表的组合实现：
- 哈希表：用于快速查找缓存项
- 双向链表：用于维护缓存项的访问顺序

### 代码实现

```python
class LRUCache:
    def __init__(self, capacity):
        """
        初始化LRU缓存
        :param capacity: 缓存容量
        """
        self.capacity = capacity
        self.cache = {}  # 键值对，值为(值, 节点)
        # 双向链表节点
        class Node:
            def __init__(self, key, value):
                self.key = key
                self.value = value
                self.prev = None
                self.next = None
        self.Node = Node
        # 虚拟头尾节点
        self.head = self.Node(0, 0)
        self.tail = self.Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node):
        """在链表头部添加节点"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """移除节点"""
        prev = node.prev
        new = node.next
        prev.next = new
        new.prev = prev
    
    def _move_to_head(self, node):
        """将节点移到链表头部"""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self):
        """移除链表尾部节点"""
        res = self.tail.prev
        self._remove_node(res)
        return res
    
    def get(self, key):
        """
        获取缓存项
        :param key: 键
        :return: 值，如果不存在返回-1
        """
        if key in self.cache:
            node = self.cache[key]
            # 移到链表头部
            self._move_to_head(node)
            return node.value
        return -1
    
    def put(self, key, value):
        """
        添加缓存项
        :param key: 键
        :param value: 值
        """
        if key in self.cache:
            # 更新值并移到链表头部
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # 创建新节点
            node = self.Node(key, value)
            self.cache[key] = node
            self._add_node(node)
            
            # 检查容量
            if len(self.cache) > self.capacity:
                # 移除尾部节点
                tail = self._pop_tail()
                del self.cache[tail.key]

# 测试示例
lru = LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
print(lru.get(1))  # 输出: 1
lru.put(3, 3)  # 淘汰2
print(lru.get(2))  # 输出: -1
lru.put(4, 4)  # 淘汰1
print(lru.get(1))  # 输出: -1
print(lru.get(3))  # 输出: 3
print(lru.get(4))  # 输出: 4
```

## LFU (Least Frequently Used)

### 基本概念

LFU（最不经常使用）算法是一种基于访问频率的缓存替换算法，当缓存容量达到上限时，优先淘汰访问频率最低的缓存项。

### 工作原理

1. 维护一个频率字典，记录每个频率对应的缓存项链表
2. 维护一个最小频率变量，记录当前最低的访问频率
3. 当访问一个缓存项时，增加其频率，并将其移到对应频率的链表中
4. 当缓存容量达到上限时，淘汰最小频率链表中的缓存项

### 实现

使用哈希表和双向链表的组合实现：
- 缓存字典：用于快速查找缓存项
- 频率字典：记录每个频率对应的缓存项链表
- 最小频率变量：记录当前最低的访问频率

### 代码实现

```java
import java.util.HashMap;
import java.util.Map;

public class LFUCache {
    private int capacity;
    private int size;
    private int minFreq;
    private Map<Integer, Node> cache;
    private Map<Integer, DoublyLinkedList> freqMap;
    
    // 双向链表节点
    private static class Node {
        int key;
        int value;
        int freq;
        Node prev;
        Node next;
        
        Node(int key, int value) {
            this.key = key;
            this.value = value;
            this.freq = 1;
        }
    }
    
    // 双向链表
    private static class DoublyLinkedList {
        Node head;
        Node tail;
        
        DoublyLinkedList() {
            head = new Node(0, 0);
            tail = new Node(0, 0);
            head.next = tail;
            tail.prev = head;
        }
        
        void addNode(Node node) {
            node.prev = head;
            node.next = head.next;
            head.next.prev = node;
            head.next = node;
        }
        
        void removeNode(Node node) {
            Node prev = node.prev;
            Node next = node.next;
            prev.next = next;
            next.prev = prev;
        }
        
        boolean isEmpty() {
            return head.next == tail;
        }
    }
    
    public LFUCache(int capacity) {
        """
        初始化LFU缓存
        :param capacity: 缓存容量
        """
        this.capacity = capacity;
        this.size = 0;
        this.minFreq = 0;
        this.cache = new HashMap<>();
        this.freqMap = new HashMap<>();
    }
    
    private void updateFreq(int key, Integer value) {
        """更新缓存项的频率"""
        Node node = cache.get(key);
        int oldFreq = node.freq;
        
        // 如果提供了新值，更新值
        if (value != null) {
            node.value = value;
        }
        
        // 从旧频率链表中移除
        DoublyLinkedList oldList = freqMap.get(oldFreq);
        oldList.removeNode(node);
        if (oldList.isEmpty()) {
            freqMap.remove(oldFreq);
            // 如果旧频率是最小频率，更新最小频率
            if (oldFreq == minFreq) {
                minFreq++;
            }
        }
        
        // 增加频率
        node.freq++;
        int newFreq = node.freq;
        
        // 添加到新频率链表
        freqMap.putIfAbsent(newFreq, new DoublyLinkedList());
        freqMap.get(newFreq).addNode(node);
    }
    
    public int get(int key) {
        """
        获取缓存项
        :param key: 键
        :return: 值，如果不存在返回-1
        """
        if (cache.containsKey(key)) {
            // 更新频率
            updateFreq(key, null);
            return cache.get(key).value;
        }
        return -1;
    }
    
    public void put(int key, int value) {
        """
        添加缓存项
        :param key: 键
        :param value: 值
        """
        if (capacity == 0) {
            return;
        }
        
        if (cache.containsKey(key)) {
            // 更新值和频率
            updateFreq(key, value);
        } else {
            // 检查容量
            if (size >= capacity) {
                // 淘汰最小频率的缓存项
                DoublyLinkedList minList = freqMap.get(minFreq);
                // 移除链表尾部节点（最久未使用的）
                Node node = minList.tail.prev;
                minList.removeNode(node);
                cache.remove(node.key);
                size--;
                // 如果最小频率链表为空，删除该频率
                if (minList.isEmpty()) {
                    freqMap.remove(minFreq);
                }
            }
            
            // 创建新节点
            Node node = new Node(key, value);
            cache.put(key, node);
            freqMap.putIfAbsent(1, new DoublyLinkedList());
            freqMap.get(1).addNode(node);
            size++;
            // 重置最小频率为1
            minFreq = 1;
        }
    }
    
    // 测试示例
    public static void main(String[] args) {
        LFUCache lfu = new LFUCache(2);
        lfu.put(1, 1);
        lfu.put(2, 2);
        System.out.println(lfu.get(1));  // 输出: 1 (频率变为2)
        lfu.put(3, 3);  // 淘汰频率为1的2
        System.out.println(lfu.get(2));  // 输出: -1
        System.out.println(lfu.get(3));  // 输出: 3 (频率变为2)
        lfu.put(4, 4);  // 淘汰频率为2的1
        System.out.println(lfu.get(1));  // 输出: -1
        System.out.println(lfu.get(3));  // 输出: 3 (频率变为3)
        System.out.println(lfu.get(4));  // 输出: 4 (频率变为2)
    }
}
```

## 总结

缓存替换算法是缓存系统的核心，不同的缓存替换算法有不同的特点和适用场景：

- **LRU**：基于访问时间，优先淘汰最久未被访问的缓存项，适用于访问模式有时间局部性的场景
- **LFU**：基于访问频率，优先淘汰访问频率最低的缓存项，适用于访问模式有频率局部性的场景

在实际应用中，应根据具体的访问模式选择合适的缓存替换算法，以提高缓存的命中率和系统性能。