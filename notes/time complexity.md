Time needed to solve a given instance $\pi$ of $\Pi$.

Execution time will be defined in terms of the input.

> It will not depend on the nature of the input data but on what is conventional to call “size” of the instance.

# Example: Sorting a vector

The determining factor is the number of elements in the vector, and not what kind of elements are in the vector.

# Worst-case time complexity

The time complexity when taking into account all the instances of the problem of a given size. Typically measured in terms of the size of the instance with neglected constants.

Notation: $O$ (Big-O).

# Example: In a vector

| Problem  | Time complexity  |
|---:|:---|
| Largest/smallest element  | $O(n)$  |
| Sequential search  | $O(n)$  |
| Binary search (sorted vector)  | $O(\log n)$  |
| Naive sorting  | $O(n^2)$  |
| Sorting | $O(n \log n)$ |

# Example: Two square $n \times n$ matrices

| Problem  | Time complexity  |
|---:|:---|
| Matrix addition  | $O(n^2)$  |
| Matrix multiplication  | $O(n^3)$  |

# Not so fast…

The distinction between efficient polynomial-time algorithms and inefficient exponential-time algorithms have some exceptions:
* A $2^n$ algorithm is faster than a $n^5$ for $n \leq 20$.
* There are exponential-time algorithms that are very useful in practice:
    - The Simplex algorithm is exponential in the worst case, but it is very fast in practice.

But on practice, polynomial-time algorithms tend to have degree 3 or less and coefficients that are small. $n^100$ or $10^99 n^2$ in general do not happen.
