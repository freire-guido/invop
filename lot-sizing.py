from ortools.linear_solver import pywraplp

def main():
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        return

    # Sets
    T = range(1, 6)
    W = range(6)

    # Parameters
    d = {1: 10, 2: 10, 3: 10, 4: 10, 5: 10}
    c = {1: 8, 2: 9, 3: 7, 4: 11, 5: 12}

    # Variables
    x = {t: solver.NumVar(0.0, solver.infinity(), f'x[{t}]') for t in T}
    s = {w: solver.NumVar(0.0, solver.infinity(), f's[{w}]') for w in W}

    print("Number of variables =", solver.NumVariables())

    # Objective function
    objective = solver.Objective()
    for t in T:
        objective.SetCoefficient(x[t], c[t])
        objective.SetCoefficient(s[t], 1.5)
    objective.SetMinimization()

    # Constraints
    for t in T:
        solver.Add(s[t] == s[t-1] + x[t] - d[t] if t > 0 else s[t] == x[t])
        solver.Add(x[t] <= 17)
        solver.Add(s[t] <= 12)
        solver.Add(s[t] >= 4)

    solver.Add(s[0] == 0)

    print("Number of constraints =", solver.NumConstraints())

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", objective.Value())
        for t in T:
            print(f"x[{t}] =", x[t].solution_value())
        for w in W:
            print(f"s[{w}] =", s[w].solution_value())
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")

if __name__ == "__main__":
    main()
