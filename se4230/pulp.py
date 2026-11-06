from pulp import LpVariable, LpProblem, LpMaximize, lpSum

problem = LpProblem("Choco Profit", LpMaximize)
w = LpVariable("white chocolate")
d = LpVariable("dark chocolate")
problem += 5 * d + 2 * w
problem += d >= 0
problem += w >= 0
problem += d <= 3
problem += w <= 6
problem += d + w <= 8
problem += d + 2 * w <= 5

problem.solve()
print(d,w)