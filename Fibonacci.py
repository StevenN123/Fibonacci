"""
Fibonacci Numbers - Dynamic Programming Implementation
Author: Steven N
Description: Four different approaches to calculate Fibonacci numbers,
             demonstrating key DP concepts
"""

import time
from functools import lru_cache

def fib_naive(n):
    """
    Approach 1: Naive Recursive - O(2ⁿ) time
    
    This is the direct translation of the mathematical definition,
    but it's extremely inefficient because it recomputes the same
    values many times.
    
    Args:
        n: Position in Fibonacci sequence
    
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)


def fib_memoization(n, memo=None):
    """
    Approach 2: Top-Down DP with Memoization - O(n) time, O(n) space
    
    Memoization stores already computed results in a dictionary,
    so each Fibonacci number is computed only once.
    
    Args:
        n: Position in Fibonacci sequence
        memo: Dictionary storing computed values
    
    Returns:
        nth Fibonacci number
    """
    if memo is None:
        memo = {}
    
    # Base cases
    if n <= 1:
        return n
    
    # Check if already computed
    if n in memo:
        return memo[n]
    
    # Compute and store
    memo[n] = fib_memoization(n-1, memo) + fib_memoization(n-2, memo)
    return memo[n]


# Python's built-in memoization decorator
@lru_cache(maxsize=None)
def fib_lru_cache(n):
    """
    Approach 2b: Using Python's built-in LRU cache decorator
    """
    if n <= 1:
        return n
    return fib_lru_cache(n-1) + fib_lru_cache(n-2)


def fib_tabulation(n):
    """
    Approach 3: Bottom-Up DP with Tabulation - O(n) time, O(n) space
    
    Tabulation builds the solution from the base cases up,
    filling a table iteratively without recursion.
    
    Args:
        n: Position in Fibonacci sequence
    
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    
    # Create DP table
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    # Build table bottom-up
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]


def fib_space_optimized(n):
    """
    Approach 4: Space-Optimized DP - O(n) time, O(1) space
    
    Since each Fibonacci number only depends on the previous two,
    we don't need to store the entire table - just two variables.
    
    Args:
        n: Position in Fibonacci sequence
    
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    
    prev2 = 0  # F(i-2)
    prev1 = 1  # F(i-1)
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


def fib_matrix(n):
    """
    Approach 5: Matrix Exponentiation - O(log n) time, O(1) space
    
    Uses the fact that:
    [F(n+1) F(n)  ] = [1 1]^n
    [F(n)   F(n-1)]   [1 0]
    
    Args:
        n: Position in Fibonacci sequence
    
    Returns:
        nth Fibonacci number
    """
    if n <= 1:
        return n
    
    def matrix_multiply(a, b):
        return [
            [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
            [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
        ]
    
    def matrix_power(matrix, n):
        if n == 1:
            return matrix
        
        if n % 2 == 0:
            half = matrix_power(matrix, n // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, n - 1))
    
    base = [[1, 1], [1, 0]]
    result = matrix_power(base, n)
    return result[0][1]


def fib_golden_ratio(n):
    """
    Approach 6: Golden Ratio Formula - O(1) time, O(1) space
    
    Uses Binet's formula: F(n) = (φⁿ - ψⁿ)/√5
    where φ = (1+√5)/2 (golden ratio), ψ = (1-√5)/2
    
    Note: This may have precision issues for large n.
    
    Args:
        n: Position in Fibonacci sequence
    
    Returns:
        nth Fibonacci number (as integer)
    """
    phi = (1 + 5**0.5) / 2
    psi = (1 - 5**0.5) / 2
    return int((phi**n - psi**n) / 5**0.5)


def fib_generator(n):
    """
    Generate Fibonacci sequence up to n using generator
    
    Args:
        n: Number of Fibonacci numbers to generate
    
    Yields:
        Fibonacci numbers one by one
    """
    a, b = 0, 1
    for _ in range(n + 1):
        yield a
        a, b = b, a + b


def print_fib_sequence(n):
    """Print the entire Fibonacci sequence up to n"""
    print(f"\nFibonacci sequence up to F({n}):")
    print("-" * 40)
    for i, fib_num in enumerate(fib_generator(n)):
        print(f"F({i}) = {fib_num}")


def compare_approaches(n):
    """Compare all approaches and measure execution time"""
    print("\n" + "=" * 70)
    print(f"COMPARING ALL APPROACHES FOR n = {n}")
    print("=" * 70)
    
    approaches = [
        ("Memoization", fib_memoization),
        ("LRU Cache", fib_lru_cache),
        ("Tabulation", fib_tabulation),
        ("Space Optimized", fib_space_optimized),
        ("Matrix Exponentiation", fib_matrix),
        ("Golden Ratio", fib_golden_ratio)
    ]
    
    # Don't include naive for large n
    if n <= 35:
        approaches.insert(0, ("Naive Recursive", fib_naive))
    
    results = {}
    
    for name, func in approaches:
        # Clear cache for memoization approaches
        if name == "LRU Cache":
            fib_lru_cache.cache_clear()
        
        # Time the execution
        start = time.time()
        result = func(n)
        end = time.time()
        
        results[name] = {
            "result": result,
            "time": (end - start) * 1000  # Convert to milliseconds
        }
        
        print(f"\n{name}:")
        print(f"  Result: F({n}) = {result}")
        print(f"  Time: {results[name]['time']:.4f} ms")
    
    # Find the fastest approach
    fastest = min(results.items(), key=lambda x: x[1]['time'])
    print(f"\n" + "=" * 70)
    print(f"✅ Fastest: {fastest[0]} ({fastest[1]['time']:.4f} ms)")
    print("=" * 70)


def count_calls_decorator(func):
    """Decorator to count function calls"""
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls_decorator
def fib_naive_count(n):
    """Naive recursive with call counting"""
    if n <= 1:
        return n
    return fib_naive_count(n-1) + fib_naive_count(n-2)


def demonstrate_recursion_tree():
    """Demonstrate the recursion tree explosion"""
    print("\n" + "=" * 70)
    print("RECURSION TREE ANALYSIS")
    print("=" * 70)
    
    for n in [5, 10, 20, 30]:
        fib_naive_count.calls = 0
        result = fib_naive_count(n)
        print(f"\nn = {n}: F({n}) = {result}")
        print(f"  Recursive calls: {fib_naive_count.calls:,}")
        
        # Compare with memoization
        fib_lru_cache.cache_clear()
        start = time.time()
        result_memo = fib_lru_cache(n)
        cache_info = fib_lru_cache.cache_info()
        print(f"  Memoization calls: {cache_info.hits + cache_info.misses}")
        print(f"  Cache hits: {cache_info.hits}, misses: {cache_info.misses}")


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("FIBONACCI NUMBERS - DYNAMIC PROGRAMMING DEMONSTRATION")
    print("=" * 70)
    
    # Test with n = 10
    n = 10
    
    print(f"\nCalculating Fibonacci({n}) using different approaches:")
    print("-" * 50)
    
    # Approach 1: Naive (only for small n)
    if n <= 30:
        print(f"Naive: {fib_naive(n)}")
    
    # Approach 2: Memoization
    print(f"Memoization: {fib_memoization(n)}")
    
    # Approach 3: LRU Cache
    print(f"LRU Cache: {fib_lru_cache(n)}")
    
    # Approach 4: Tabulation
    print(f"Tabulation: {fib_tabulation(n)}")
    
    # Approach 5: Space Optimized
    print(f"Space Optimized: {fib_space_optimized(n)}")
    
    # Approach 6: Matrix Exponentiation
    print(f"Matrix: {fib_matrix(n)}")
    
    # Approach 7: Golden Ratio
    print(f"Golden Ratio: {fib_golden_ratio(n)}")
    
    # Print the entire sequence
    print_fib_sequence(n)
    
    # Compare approaches for different n
    for test_n in [10, 20, 30]:
        compare_approaches(test_n)
    
    # Demonstrate recursion tree explosion
    demonstrate_recursion_tree()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
    1. Naive Recursive: O(2ⁿ) time - Exponential explosion!
    2. Memoization: O(n) time, O(n) space - Top-down DP
    3. Tabulation: O(n) time, O(n) space - Bottom-up DP
    4. Space Optimized: O(n) time, O(1) space - Best for simple recurrences
    5. Matrix Exponentiation: O(log n) time - Mathematical optimization
    6. Golden Ratio: O(1) time - But precision issues for large n
    
    For n=100:
    - Naive: Would take billions of years
    - DP approaches: Microseconds
    - Matrix: Logarithmic time
    """)
