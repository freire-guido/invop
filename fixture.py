from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver("CBC")

    if not solver:
        return

    # Equipos
    E = ["RIV", "BOC", "IND", "RAC", "SLO", "DYJ", "ATU", "VEL", "HUR", "UNI", "ALD", "TAL", "BAN",
         "LAN", "GOD", "NOB", "TIG", "EST", "CEN", "COL", "SAN", "GYE", "SMT", "PAT", "BEL", "ARG"]
    F = range(1, 26)

    # Variables
    x = {(i, j, f): solver.BoolVar(f'x[{i},{j},{f}]') for i in E for j in E for f in F}

    print("Number of variables =", solver.NumVariables())

    # Restricciones
    # Cada equipo juega un partido por fecha
    for i in E:
        for f in F:
            solver.Add(sum(x[i, j, f] + x[j, i, f] for j in E) == 1)

    # Cada partido se juega una vez, en una de sus dos localias
    for i in E:
        for j in E:
            if i != j:
                solver.Add(sum(x[i, j, f] + x[j, i, f] for f in F) == 1)

    # No se juega contra si mismo
    for i in E:
        for f in F:
            solver.Add(x[i, i, f] == 0)

    # Balance de partidos de local y visitante
    for i in E:
        for f in F:
            solver.Add(sum(x[i, j, f] for j in E) <= 13)
            solver.Add(sum(x[j, i, f] for j in E) <= 13)

    # No se juegan tres partidos seguidos de local
    for i in E:
        for f in range(1, 24):  
            solver.Add(sum(x[i, j, f] + x[i, j, f+1] + x[i, j, f+2] for j in E) <= 2)

    # No se juegan tres partidos seguidos de visitante
    for i in E:
        for f in range(1, 24):  
            solver.Add(sum(x[j, i, f] + x[j, i, f+1] + x[j, i, f+2] for j in E) <= 2)

    print("Number of constraints =", solver.NumConstraints())

    # Solve the problem
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        for i, j, f in x:
            if x[i, j, f].solution_value() == 1:
                print(f"Match between {i} and {j} on date {f}")
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")

if __name__ == "__main__":
    main()
