Can be found on very places:
* High Schools (STP)
* Universities (UCTP)
* Exams (UETP)

The problem is NP-complete for most formulations (Schaerf [1995]), that vary from university to university. The difficulty increases with the number of constraints.

# Problem definition

The International Series of Conferences on the Practice and Theory of Automated Timetabling (PATAT) organize contests of Education Timetabling Problems (ETP) to evaluate the performance of algorithms, with the goal to generate research with different approaches and fill the gaps between the state-of-the-art and the state-of-the-practice.

The International Timetabling Competition (ITC) does the same

## ITC formulations

It has been based on ITC-2007. Each instance has the following characteristics:
* Days, hours and periods
* Courses and teachers
* Rooms
* Syllabus
* Unailabilities

$T$ is a solution (or Timetable) for the problem:
* $d$ is the numbers lecture days on the week that $T(d = 2)$
* Each day is divided in $q$ periods ($q = 2$)
* $nr$ is the number of available rooms ($nr = 2$)

$T$ represents the allocation of all lectures of all courses to a timetable $t$

| Room | Day 0 | Day 1 |
|------|-------|-------|
|      | $p_0$ | $p_1$ |
| $r_0$ |      |       |
| $r_1$ |  $t$ |       |

### Example

```
Name: Toy3
Courses: 3
Rooms: 2
Days: 2
Periods_per_day: 2
Curricula: 2
Constraints: 2

COURSES:
DiscMath Edmar 2 2 40
CompProg Geraldo 2 2 35
GraphThe Edmar 2 3 20

ROOMS:
rA 38
rB 32

CURRICULA:
Cur1 2 DiscMath CompProg
Cur2 1 GraphThe

UNAVAILABILITY_CONSTRAINTS:
CompProg 0 0
CompProg 1 1
END.
```

## Strong restrictions

* H1: Lectures
* H2: Rooms occupancy
* H3: Conflicts: Professors, Curricula
* H4: Availability

## Weak restrictions

* S1: Room capacity
* S2: Room stability
* S3: Minimum working days
* S4: Isolated lectures

## Definition:

Minimize $f(s) = f_\text{Strong}(s) + f_\text{Weak}(s)$

If $s$ is a feasible solution, $f(s) = 0$.
$f_\text{Weak}(s) = \sum_{i=1}^4 \alpha_i \omega_i(s)$.
$\alpha_i$ is the weight of the soft constraint $i$.
$\omega_i(s)$ is the total count of violations of the soft constraint $i$.
$\alpha_1 = 1, \alpha_2 = 1, \alpha_3 = 5, \alpha_4 = 2$.
