Guided Local Search (GLS) is a metaheuristic optimization algorithm that modifies the behavior of Local Search by incorporating a penalty function that guides the search towards promising regions of the search space. The penalty function assigns a penalty to each solution based on its distance from a set of reference solutions, which are typically obtained by running the algorithm multiple times with different initial solutions.

The penalty function is used to modify the objective function of the Local Search algorithm, so that the search is biased towards solutions that are closer to the reference solutions. This helps to avoid getting stuck in local optima and to explore a broad portion of the search space.

GLS can be seen as a combination of two phases: a Local Search phase and a Penalty phase. In the Local Search phase, the algorithm iteratively improves a candidate solution by making small modifications to it, as in the standard Local Search algorithm. In the Penalty phase, the algorithm evaluates the solution using the penalty function and modifies the objective function accordingly, before returning to the Local Search phase.

Overall, Guided Local Search is a powerful optimization algorithm that combines the strengths of Local Search with the ability to explore a broad portion of the search space.



See also: https://en.wikipedia.org/wiki/Guided_local_search
