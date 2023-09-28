Local Search is a metaheuristic optimization algorithm that iteratively improves a candidate solution by making small modifications to it. The method comprises slicing the search space to a limited subset of the original, limiting the needed time to search. The algorithm starts with an initial solution and then repeatedly makes small changes to it, evaluating the new solution and accepting it if it is better than the previous one. If the new solution is worse, it may still be accepted with a certain probability, allowing the algorithm to escape from local optima.

One example of Local Search is the [[Hill Climbing]] algorithm, which starts with an initial solution and then repeatedly makes small modifications to it, always accepting the new solution if it is better than the previous one. The algorithm stops when no further improvements can be made, which may result in a local optimum.

# Local Search vs Gradient Descent

Local Search can seem very similar to Gradient Descent (_método do Gradiente_) algorithms, both being iterated methods of optimization, but one key difference is that Gradient Descent relies solely on the Loss function, while Local Search relies on the explicit exploration of the search space, so it can also use other information, such as the structure of the search space, it also does not require the objective function to be differentiable. This makes Local Search applicable to a broader range of problems.

# Step-by-step

You will need: a definition of the search space, a definition of the objective function, and a definition of the neighborhood function.

To perform Local Search, we need to do the following steps:
1. Start the search in any point of the search space -- techniques for choosing the initial solution are dependent on domain knowledge and are not covered here.
2. Move to a neighboring solution. There should be relatively few neighboring solutions. Each move is determined by a decision based simply on local knowledge.

Repeat step 2 until a stopping criterion (time bound or precision) is met.

## Neighborhood function

Good neighborhood functions are those that can be computed efficiently and that allow the algorithm to explore a broad portion of the search space. The neighborhood function should be defined in such a way that it is possible to move from any solution to any other solution in a finite number of steps. The definition of a good neighborhood function is key for the performance of the algorithm.

This introduces a notion of proximity between solutions, which is used to define the neighborhood function. The neighborhood function is a function that takes a solution as input and returns a set of neighboring solutions.

A neighborhood relation induces a graph on the search space, where each solution is a node and there is an edge between two solutions if they are neighbors. The neighborhood function is used to define the neighborhood relation, which in turn is used to define the neighborhood graph.

It is common for neighborhood relationship to be symmetric, and also common for all the vertices to have the same number of neighbors (making the graph regular).

# Shortcomings
* Premature convergence on the first local optima found.
* Sensitive to starting solution.
* Sensitive to neighborhood function.
* Sensitive to search strategy.
* May require an exponential number of steps to find the optimal solution (!!)
# Improvements

There are alterations to try to lessen the impact of the shortcomings:

* Random restarts: run the algorithm multiple times with different starting solutions.
* Random walk: instead of always moving to the best neighbor, move to a random neighbor.
* Multiple neighborhoods: When reaching a local optimum, switch to a different neighborhood.
* [[Simulated annealing]]: accept worse solutions with a certain probability, which is decreased over time.
* [[Tabu search]]: keep a list of recently visited solutions and avoid visiting them again.
* [[Guided local search]]: use a penalty function to guide the search towards promising regions of the search space.
# Considerations

Typically, these are “weak” algorithms, in the sense that they do not guarantee that the solution found is optimal. It also cannot determine if optimal solution exist. It can move to the same solution more than once.

See also: https://en.wikipedia.org/wiki/Local_search_(optimization)
