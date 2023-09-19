Problems we are interested in:

* [[Improve material usage in manufacturing]]
* [[Optimize time for realization of tasks and operations]]
* [[Transport more material through better routes]]
* [[Decrease loss chance; increase profits; decrease costs]]
* …

On these problems, we are not contempt on only having one of the possible solutions, but the ones that also optimize the goals of interest.

In an **optimization problem**, we are interested in finding the best solution between all of those solutions that satisfy the constraints of the problem. Depending on the nature of the variables, the problem can be classified as a [[continuous optimization problem]] or a [[discrete optimization problem]].

Combinatory problems appear in diverse areas of Computer Science and in other disciplines where computational methods applies.

* Finding the smallest route roundtrip (TSP)
* Routing:
    - Of packets in a network
    - Of vehicles in a fleet (VRP)
* Planning
* Scheduling
    - Programming of tasks in a production line

Finally, combination problems involve on finding a *grouping*, a *set*, or an *attribution* of a *finite and discrete set of elements* that satisfies the constraints.
Candidate solutions are:
* Combinations of solution components
* An attempt to generate a solution
* May not satisfy all constraints.
# Example

## TSP

Data: sets of points on euclidean space.
Task: Find the shortest roundtrip.
* A path connecting all points maps to a sequence of points (*attribution* of points to a position sequence)
* Component of the solution: segment of path consisting of two points that will be visited consecutively.
* Candidate solution: A roundtrip path.
  + A particular approach could considerate a path that visits a point more than once.
* Solution: A minimum-sized roundtrip.

## Scheduling

You may consider the scheduling problem an *attribution* problem, where:
* Components of the solution are events to be scheduled.
* Values attributed to the events maps to the time when the event will occur.

Typically, there is a huge amount of candidate solutions.

For most combinatory problems, the space of potential solutions for a given instance of the problem is at least exponential in the size of the input.

# Example

## TSP

Given a set of $n$ cities and a distance $d_{ij}$ between each pair of cities $i$ and $j$, find a roundtrip of minimum length that visits each city exactly once.

What is the number of solutions?
Given that the starting city is arbitrary, there exists $(n-1)!$ viable solutions.
If we consider the distance between all cities to be the same, this gets reduced to $(n-1)!/2$.
There is $(n-1)!$ routes and the total distance in each route involves $n$ additions. Therefore, the total number of additions is $n!$.

In an instance with $n = 50$, the total number of additions would be $50! \approx 10^{64}$.
In a computer that executes $10^9$ additions per second, it would take $10^{45}$ centuries to execute the additions alone. For this reason, complete enumeration is impossible.

# Classes of Combinatory Problems

## Decision problems

Is there a solution that satisfies all constraints?

### Result: Yes or No

## Optimization problems

Given all structure satisfying a property, which one optimizes a given objective function?

### Result: A viable optimal solution

## Example: TSP

### Decision problem

Is there a route for all cities in $N$ that start and end in the same city, which length is less or equal than $k$?

### Optimization problem

Find a route for all cities in $N$ that start and end in the same city, with the minimum length.
