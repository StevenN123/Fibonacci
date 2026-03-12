"""
Fibonacci Numbers - Dynamic Programming Implementation
Author: Steven N
Description: Four different approaches to calculate Fibonacci numbers,
             demonstrating key DP concepts
"""

import time
from functools import lru_cache

# =============================================================================
# APPROACH 1: NAIVE RECURSIVE - Time O(2ⁿ), Space O(n) stack
# =============================================================================

def fib_naive(n):
    """
    Naive recursive implementation - directly follows mathematical definition
    
    Visual representation for n=4:
                     F(4)
                    /    \
                F(3)      F(2)
               /    \    /    \
            F(2)   F(1) F(1) F(0)
           /    \
        F(1)   F(0)
    
    Notice F(2) is calculated multiple times! This is the inefficiency.
    """
    # Base case: F(0) = 0, F(1) = 1
    if n <= 1:
        return n
    
    # Recursive case: F(n) = F(n-1) + F(n-2)
    # Each call spawns two more calls, creating exponential growth
    return fib_naive(n-1) + fib_naive(n-2)


# =============================================================================
# APPROACH 2: TOP-DOWN DP WITH MEMOIZATION - Time O(n), Space O(n)
# =============================================================================

def fib_memoization(n, memo=None):
    """
    Memoization stores computed results in a dictionary (cache)
    Think of it as taking notes while solving - never recompute what you already know!
    
    For n=5, the call tree becomes:
    F(5) -> F(4) -> F(3) -> F(2) -> F(1), F(0)
         -> F(3) (retrieved from cache, not recomputed!)
    """
    # Initialize memo dictionary on first call
    # This dictionary will store {n: fibonacci_value} pairs
    if memo is None:
        memo = {}
    
    # Base case: F(0) = 0, F(1) = 1
    if n <= 1:
        return n
    
    # Check if we've already calculated this value
    # This is the "memoization" part - looking at our notes before working
    if n in memo:
        return memo[n]  # Return cached value immediately - no recalculation!
    
    # If not in cache, calculate it recursively and store it
    # The recursion will first calculate smaller values and store them
    memo[n] = fib_memoization(n-1, memo) + fib_memoization(n-2, memo)
    
    # Return the newly calculated and stored value
    return memo[n]


# =============================================================================
# APPROACH 2B: PYTHON'S BUILT-IN MEMOIZATION - Time O(n), Space O(n)
# =============================================================================

@lru_cache(maxsize=None)  # Decorator automatically handles caching
def fib_lru_cache(n):
    """
    Python's functools.lru_cache provides automatic memoization
    LRU = Least Recently Used - but with maxsize=None, it stores everything
    
    This is the same as fib_memoization, but Python manages the cache for us!
    """
    # Base case: F(0) = 0, F(1) = 1
    if n <= 1:
        return n
    
    # Recursive case - Python automatically:
    # 1. Checks if (n-1) and (n-2) are in cache before computing
    # 2. Stores results in cache after computing
    return fib_lru_cache(n-1) + fib_lru_cache(n-2)


# =============================================================================
# APPROACH 3: BOTTOM-UP DP WITH TABULATION - Time O(n), Space O(n)
# =============================================================================

def fib_tabulation(n):
    """
    Tabulation builds the solution from the ground up (bottom to top)
    Instead of starting from n and going down, we start from 0 and build up
    
    Visual representation for n=5:
    Step 1: dp[0] = 0 (we know this)
    Step 2: dp[1] = 1 (we know this)
    Step 3: dp[2] = dp[1] + dp[0] = 1 + 0 = 1
    Step 4: dp[3] = dp[2] + dp[1] = 1 + 1 = 2
    Step 5: dp[4] = dp[3] + dp[2] = 2 + 1 = 3
    Step 6: dp[5] = dp[4] + dp[3] = 3 + 2 = 5
    
    Table after computation: [0, 1, 1, 2, 3, 5]
    """
    # Handle base cases immediately
    if n <= 1:
        return n
    
    # Create a table (list) to store all Fibonacci numbers up to n
    # We need n+1 slots because we want index n to be the nth number
    dp = [0] * (n + 1)
    
    # Initialize known values (base cases)
    dp[0] = 0  # F(0) = 0
    dp[1] = 1  # F(1) = 1
    
    # Build the table bottom-up: each new value depends on previous two
    # This is "tabulation" - filling a table iteratively
    for i in range(2, n + 1):
        # Current Fibonacci = sum of previous two
        dp[i] = dp[i-1] + dp[i-2]
    
    # Return the nth Fibonacci number from our table
    return dp[n]


# =============================================================================
# APPROACH 4: SPACE-OPTIMIZED DP - Time O(n), Space O(1)
# =============================================================================

def fib_space_optimized(n):
    """
    Space optimization: We only need the last two values, not the whole table!
    Like climbing stairs - you only need to remember the last two steps
    
    For n=5, the variables evolve like this:
    Start:  prev2=0, prev1=1
    i=2:    current = 1+0=1, then prev2=1, prev1=1
    i=3:    current = 1+1=2, then prev2=1, prev1=2
    i=4:    current = 2+1=3, then prev2=2, prev1=3
    i=5:    current = 3+2=5, then prev2=3, prev1=5
    Return prev1 = 5
    """
    # Handle base cases immediately
    if n <= 1:
        return n
    
    # We only store the two most recent values
    # Think of these as two pointers moving along the sequence
    prev2 = 0  # This is F(i-2) - the number two steps back
    prev1 = 1  # This is F(i-1) - the previous number
    
    # Iterate from 2 to n, updating our two variables
    for i in range(2, n + 1):
        # Calculate current Fibonacci number
        current = prev1 + prev2
        
        # Shift our window: move both pointers forward
        # The previous prev2 is now forgotten (garbage collected)
        prev2 = prev1  # Old prev1 becomes the new prev2
        prev1 = current  # Current becomes the new prev1
    
    # prev1 now holds F(n)
    return prev1


# =============================================================================
# APPROACH 5: MATRIX EXPONENTIATION - Time O(log n), Space O(1)
# =============================================================================

def fib_matrix(n):
    """
    Matrix exponentiation uses the mathematical property:
    [F(n+1) F(n)  ] = [1 1]^n
    [F(n)   F(n-1)]   [1 0]
    
    This allows us to compute F(n) in O(log n) time using exponentiation by squaring!
    Like calculating 2^8 by squaring: 2^2=4, 4^2=16, 16^2=256 (3 steps instead of 8)
    """
    # Handle base cases
    if n <= 1:
        return n
    
    def matrix_multiply(a, b):
        """
        Multiply two 2x2 matrices
        [a00 a01] * [b00 b01] = [a00*b00 + a01*b10, a00*b01 + a01*b11]
        [a10 a11]   [b10 b11]   [a10*b00 + a11*b10, a10*b01 + a11*b11]
        """
        return [
            [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
            [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
        ]
    
    def matrix_power(matrix, power):
        """
        Raise matrix to the given power using divide-and-conquer
        If power is even: M^p = (M^(p/2))^2
        If power is odd: M^p = M * M^(p-1)
        """
        if power == 1:
            return matrix
        
        if power % 2 == 0:  # Even power
            half = matrix_power(matrix, power // 2)
            return matrix_multiply(half, half)
        else:  # Odd power
            return matrix_multiply(matrix, matrix_power(matrix, power - 1))
    
    # Base matrix that generates Fibonacci numbers
    base_matrix = [[1, 1], [1, 0]]
    
    # Raise base matrix to the nth power
    result_matrix = matrix_power(base_matrix, n)
    
    # The top-right element (or bottom-left) contains F(n)
    return result_matrix[0][1]


# =============================================================================
# APPROACH 6: GOLDEN RATIO (BINET'S FORMULA) - Time O(1), Space O(1)
# =============================================================================

def fib_golden_ratio(n):
    """
    Binet's Formula: F(n) = (φⁿ - ψⁿ)/√5
    where φ = (1+√5)/2 ≈ 1.618 (golden ratio)
    and ψ = (1-√5)/2 ≈ -0.618
    
    This is a closed-form solution - we can compute F(n) directly!
    But floating-point precision limits its accuracy for large n.
    """
    # Calculate the golden ratio (φ) and its conjugate (ψ)
    sqrt5 = 5 ** 0.5  # √5 ≈ 2.236
    phi = (1 + sqrt5) / 2  # Golden ratio ≈ 1.618
    psi = (1 - sqrt5) / 2  # Conjugate ≈ -0.618
    
    # Apply Binet's formula and round to nearest integer
    # We use int() to convert from float to integer
    return int((phi**n - psi**n) / sqrt5)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def fib_generator(n):
    """
    Generate Fibonacci sequence up to n using a generator
    This is memory-efficient as it yields one value at a time
    """
    a, b = 0, 1  # Start with F(0) and F(1)
    for _ in range(n + 1):  # Loop n+1 times to include F(n)
        yield a  # Yield current value
        a, b = b, a + b  # Update for next iteration (simultaneous assignment)


def print_fib_sequence(n):
    """Print the entire Fibonacci sequence up to n"""
    print(f"\nFibonacci sequence up to F({n}):")
    print("-" * 40)
    for i, fib_num in enumerate(fib_generator(n)):
        print(f"F({i}) = {fib_num}")


def count_calls_decorator(func):
    """Decorator to count function calls - useful for demonstrating recursion"""
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls_decorator
def fib_naive_count(n):
    """Naive recursive with call counting to show exponential explosion"""
    if n <= 1:
        return n
    return fib_naive_count(n-1) + fib_naive_count(n-2)


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
    
    # Only include naive for small n (it's too slow for large n)
    if n <= 35:
        approaches.insert(0, ("Naive Recursive", fib_naive))
    
    results = {}
    
    for name, func in approaches:
        # Clear cache for LRU Cache approach
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
    
    # Find and display the fastest approach
    fastest = min(results.items(), key=lambda x: x[1]['time'])
    print(f"\n" + "=" * 70)
    print(f" Fastest: {fastest[0]} ({fastest[1]['time']:.4f} ms)")
    print("=" * 70)


def demonstrate_recursion_tree():
    """Demonstrate how the naive approach's recursion tree explodes"""
    print("\n" + "=" * 70)
    print("RECURSION TREE ANALYSIS - SHOWING EXPONENTIAL GROWTH")
    print("=" * 70)
    print("\nThe naive approach recalculates the same values multiple times:")
    
    for n in [5, 10, 20, 30]:
        # Reset call counter
        fib_naive_count.calls = 0
        
        # Calculate Fibonacci using naive approach with counting
        result = fib_naive_count(n)
        
        print(f"\nn = {n}: F({n}) = {result}")
        print(f"  Naive recursive calls: {fib_naive_count.calls:,}")
        print(f"  Theoretical minimum calls (with memoization): {n+1}")
        print(f"  Explosion factor: {fib_naive_count.calls/(n+1):.1f}x more calls!")
        
        # Show the difference with memoization
        if n <= 30:
            fib_lru_cache.cache_clear()
            result_memo = fib_lru_cache(n)
            cache_info = fib_lru_cache.cache_info()
            print(f"  Memoization calls: {cache_info.hits + cache_info.misses}")
            print(f"  Cache hits: {cache_info.hits}, misses: {cache_info.misses}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FIBONACCI NUMBERS - DYNAMIC PROGRAMMING DEMONSTRATION")
    print("=" * 70)
    print("\nThis program demonstrates 6 different ways to calculate Fibonacci numbers,")
    print("highlighting key Dynamic Programming concepts along the way.\n")
    
    # Test with a small number to show all approaches work
    n = 10
    
    print(f"\nCalculating Fibonacci({n}) using different approaches:")
    print("-" * 50)
    
    # Only run naive if n is small enough
    if n <= 30:
        print(f"Naive Recursive: {fib_naive(n)} - This recalculates values many times!")
    
    print(f"Memoization: {fib_memoization(n)} - Stores results in a cache")
    print(f"LRU Cache: {fib_lru_cache(n)} - Python's automatic memoization")
    print(f"Tabulation: {fib_tabulation(n)} - Builds table from bottom up")
    print(f"Space Optimized: {fib_space_optimized(n)} - Uses only O(1) extra space")
    print(f"Matrix Exponentiation: {fib_matrix(n)} - Uses O(log n) time!")
    print(f"Golden Ratio: {fib_golden_ratio(n)} - Direct formula, but precision issues for large n")
    
    # Show the entire sequence
    print_fib_sequence(n)
    
    # Compare performance for different input sizes
    for test_n in [10, 20, 30]:
        compare_approaches(test_n)
    
    # Demonstrate the recursion tree explosion concept
    demonstrate_recursion_tree()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHTS - DYNAMIC PROGRAMMING PRINCIPLES")
    print("=" * 70)
    print("""
     Time & Space Complexity Summary:
    
    1. Naive Recursive: O(2ⁿ) time, O(n) stack
        Problem: Exponential explosion from redundant calculations!
       
    2. Memoization: O(n) time, O(n) space
        Key Insight: Cache results to avoid recomputation (Top-down DP)
       
    3. Tabulation: O(n) time, O(n) space
        Key Insight: Build solution iteratively from base cases (Bottom-up DP)
       
    4. Space Optimized: O(n) time, O(1) space
        Key Insight: Only store what's necessary for next calculation
       
    5. Matrix Exponentiation: O(log n) time, O(1) space
        Key Insight: Mathematical properties enable logarithmic time!
       
    6. Golden Ratio: O(1) time, O(1) space
        Key Insight: Closed-form solution, but floating-point precision limits
    
     The takeaway: The right approach depends on your constraints!
    """)
