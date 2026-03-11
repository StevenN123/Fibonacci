# Fibonacci

Fibonacci numbers are used fully using a variety of dynamic programming methods. Key DP ideas including space optimization, tabulation, and memoization are demonstrated in this project.

## Problem Description

The Fibonacci sequence is defined as:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for n > 1

Calculate the nth Fibonacci number efficiently using dynamic programming.

### Example
**Input:** n = 10  
**Output:** 55

**Sequence up to n=10:**
F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, F(6)=8, F(7)=13, F(8)=21, F(9)=34, F(10)=55

## ⚙️ Algorithm Analysis

### Time & Space Complexity Comparison

| Approach | Time Complexity | Space Complexity | Pros | Cons |
|----------|----------------|------------------|------|------|
| Naive Recursive | O(2ⁿ) | O(n) stack | Simple, direct | Extremely slow |
| Memoization | O(n) | O(n) | Only computes needed values | Recursive overhead |
| Tabulation | O(n) | O(n) | No recursion | Computes all values |
| Space Optimized | O(n) | O(1) | Best space efficiency | Only for simple recurrences |
| Matrix Exponentiation | O(log n) | O(1) | Logarithmic time | Complex implementation |
| Golden Ratio | O(1) | O(1) | Constant time | Precision issues |

## 💻 Complete Python Implementation

### Approach 1: Naive Recursion (Exponential)
```python
def fib_naive(n):
    """
    Naive recursive implementation - Exponential time O(2ⁿ)
    
    This is the mathematical definition, but it's extremely inefficient because it recomputes the same values many times.
    """
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)

# Example: fib_naive(5) makes 15 recursive calls!
# fib_naive(10) makes 177 calls!
# fib_naive(30) makes 2.6 million calls!
