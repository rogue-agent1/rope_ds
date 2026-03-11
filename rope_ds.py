#!/usr/bin/env python3
"""rope_ds - Rope data structure for efficient text editing (split, concat, insert, delete).

Usage: python rope_ds.py [--demo]
"""
import sys

class RopeNode:
    __slots__ = ('text','left','right','weight')
    def __init__(self, text=None, left=None, right=None):
        if text is not None:
            self.text = text; self.left = None; self.right = None
            self.weight = len(text)
        else:
            self.text = None; self.left = left; self.right = right
            self.weight = rope_length(left) if left else 0

def rope_length(node):
    if node is None: return 0
    if node.text is not None: return len(node.text)
    return node.weight + rope_length(node.right)

def rope_index(node, i):
    if node is None: raise IndexError(i)
    if node.text is not None:
        return node.text[i]
    if i < node.weight:
        return rope_index(node.left, i)
    return rope_index(node.right, i - node.weight)

def rope_concat(left, right):
    if left is None: return right
    if right is None: return left
    return RopeNode(left=left, right=right)

def rope_split(node, i):
    if node is None: return None, None
    if node.text is not None:
        return (RopeNode(node.text[:i]) if i > 0 else None,
                RopeNode(node.text[i:]) if i < len(node.text) else None)
    if i <= node.weight:
        left_l, left_r = rope_split(node.left, i)
        return left_l, rope_concat(left_r, node.right)
    else:
        right_l, right_r = rope_split(node.right, i - node.weight)
        return rope_concat(node.left, right_l), right_r

def rope_insert(node, i, text):
    left, right = rope_split(node, i)
    new = RopeNode(text)
    return rope_concat(rope_concat(left, new), right)

def rope_delete(node, start, length):
    left, rest = rope_split(node, start)
    _, right = rope_split(rest, length)
    return rope_concat(left, right)

def rope_to_string(node):
    if node is None: return ""
    if node.text is not None: return node.text
    return rope_to_string(node.left) + rope_to_string(node.right)

def rope_depth(node):
    if node is None: return 0
    if node.text is not None: return 1
    return 1 + max(rope_depth(node.left), rope_depth(node.right))

def rope_from_string(s, leaf_size=8):
    if len(s) <= leaf_size:
        return RopeNode(s)
    mid = len(s) // 2
    return RopeNode(left=rope_from_string(s[:mid], leaf_size),
                    right=rope_from_string(s[mid:], leaf_size))

def rope_report(node, start, length):
    """Extract substring."""
    _, rest = rope_split(node, start)
    result, _ = rope_split(rest, length)
    return rope_to_string(result)

def main():
    text = "Hello, World! This is a rope data structure demo."
    rope = rope_from_string(text, leaf_size=8)
    print(f"Original: \"{text}\"")
    print(f"Length: {rope_length(rope)}, Depth: {rope_depth(rope)}")
    print(f"Rebuilt: \"{rope_to_string(rope)}\"")
    print(f"Index 7: '{rope_index(rope, 7)}'")
    # Insert
    rope = rope_insert(rope, 13, " Beautiful")
    print(f"\nAfter insert ' Beautiful' at 13:")
    s = rope_to_string(rope)
    print(f"  \"{s}\" (len={rope_length(rope)})")
    # Delete
    rope = rope_delete(rope, 0, 7)
    print(f"\nAfter delete [0:7]:")
    print(f"  \"{rope_to_string(rope)}\"")
    # Substring
    sub = rope_report(rope, 0, 15)
    print(f"\nSubstring [0:15]: \"{sub}\"")
    # Split and concat
    left, right = rope_split(rope, 10)
    print(f"\nSplit at 10:")
    print(f"  Left:  \"{rope_to_string(left)}\"")
    print(f"  Right: \"{rope_to_string(right)}\"")
    merged = rope_concat(right, left)
    print(f"  Swapped: \"{rope_to_string(merged)}\"")
    # Stress test
    print(f"\nStress test: 1000 random inserts...")
    import random
    r = rope_from_string("START")
    for i in range(1000):
        pos = random.randint(0, rope_length(r))
        r = rope_insert(r, pos, f"[{i}]")
    print(f"  Length: {rope_length(r)}, Depth: {rope_depth(r)}")
    s = rope_to_string(r)
    assert len(s) == rope_length(r)
    print(f"  Integrity: OK")

if __name__ == "__main__":
    main()
