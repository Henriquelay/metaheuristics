An optimization problem where the [[continuous variables|variables are continuous]] is called a **continuous optimization problem**.

# Examples

## Find the quadratic with the smallest perimeter with $area = 1000m^2$

$$
\begin{aligned}
\textit{Min } p &= 2x + 2y \\
\textit{subject to } xy &= 1000 \\
x, y &\geq 0
\end{aligned}
$$

This is not a Linear Programming problem, because the objective function is not linear. This is a continuous optimization problem, because the variables are continuous (area and perimeter can take any value in the interval $[0, \infty]$).

Solving analytically through derivatives:

$$
\begin{aligned}
y &= \frac{1000}{x} \\
p &= 2x + 2\frac{1000}{x} \\
p' &= 2 - 2\frac{1000}{x^2} \\
&\text{The point of minimum is where } p' = 0 \\
x &= \sqrt{1000} = 31.623 \\
\text{therefore } x &\approx 31.623 \text{ with } y \approx 31.623 \\
\text{and } p &\approx 126.5
\end{aligned}
$$

In a sea of problems and solutions, we are interested in finding not **a** solution, but the **best** solution given the problem's constraints. In this case, the best solution is the one that minimizes the perimeter.
