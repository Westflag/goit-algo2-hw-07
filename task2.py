import timeit
import matplotlib.pyplot as plt
import pandas as pd

# Reusing the Node and original SplayTree from the user's version
class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        if data < current_node.data:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, data):
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child

# Adapted SplayTree for Fibonacci
class FibonacciSplayTree(SplayTree):
    def insert(self, n, fib_n):
        node = Node((n, fib_n))
        if self.root is None:
            self.root = node
        else:
            self._insert_node((n, fib_n), self.root)

    def _insert_node(self, data, current_node):
        if data[0] < current_node.data[0]:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find_value(self, n):
        node = self.root
        while node is not None:
            if n < node.data[0]:
                node = node.left_node
            elif n > node.data[0]:
                node = node.right_node
            else:
                self._splay(node)
                return node.data[1]
        return None

def fibonacci_splay(n, tree: FibonacciSplayTree):
    cached = tree.find_value(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val

# LRU Fibonacci for comparison
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Performance measurement
fibonacci_numbers = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in fibonacci_numbers:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=3) / 3
    lru_times.append(lru_time)

    tree = FibonacciSplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=3) / 3
    splay_times.append(splay_time)

# Save to DataFrame
df = pd.DataFrame({
    "n": fibonacci_numbers,
    "LRU Cache Time (s)": lru_times,
    "Splay Tree Time (s)": splay_times
})

print("Fibonacci Time Comparison (Final)")
print(df)

# Plot
plt.figure()
plt.plot(fibonacci_numbers, lru_times, marker='o', label="LRU Cache")
plt.plot(fibonacci_numbers, splay_times, marker='x', label="Splay Tree")
plt.xlabel("n (Fibonacci number index)")
plt.ylabel("Average Execution Time (seconds)")
plt.title("Fibonacci Computation: LRU Cache vs Splay Tree (Final)")
plt.legend()
plt.grid(True)
plt.show()
