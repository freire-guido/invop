from ortools.linear_solver import pywraplp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Total
K = 100
N = 50
# Porcentajes de admisión
m = 30
r = 60
q = 80

def modelo_master(M, R, Q, scores, m, r, q, N, model=1):
    """
    pre:
        ya están ordenados los chabones por score decreciente
    """
    M = np.array(M)
    R = np.array(R)
    Q = np.array(Q)
    
    K = len(scores)
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Variables
    x = {}
    for i in range(K):
        x[i] = solver.BoolVar(f'x[{i}]')

    # Restricciones
    solver.Add(solver.Sum([x[i] for i in range(K)]) == N)
    solver.Add(solver.Sum([x[i] for i in M.nonzero()[0]]) >= m * N/100)
    solver.Add(solver.Sum([x[i] for i in R.nonzero()[0]]) >= r * N/100)
    solver.Add(solver.Sum([x[i] for i in Q.nonzero()[0]]) >= q * N/100)

    if model == 1:
        solver.Maximize(solver.Sum([scores[i] * x[i] for i in range(K)]))
    elif model == 2:
        solver.Minimize(solver.Sum([ i * x[i] for i in range(K)]))
    elif model ==3:
        y = solver.IntVar(0, K, 'y')

        for i in range(K):
            solver.Add(i * x[i] <= y)

        # Objective Function
        solver.Minimize(y + 0.0002 * solver.Sum([ i * x[i] for i in range(K)]))

    return solver, x

def generar_instancia(K, m_pob = 0.5, r_pob = 0.7, q_pob = 0.8):
    M = np.random.uniform(0, 1, K) < m_pob
    R = np.random.uniform(0, 1, K) < r_pob
    Q = np.random.uniform(0, 1, K) < q_pob
    Habilidad = np.random.normal(1000,100,K)
    df = pd.DataFrame(np.array([M,R,Q,Habilidad]).T,columns=['Mujer','Interior','Pobres','Habilidad'])
    df['Score'] = df['Habilidad'] + df['Mujer'] * (-100) + df['Interior'] * (-100) + df['Pobres'] * (-100)
    df = df.sort_values(by='Score', ascending=False)
    df = df.reset_index(drop=True)
    return df


def admitir(m=m,r=r,q=q,N=N, modelo = 3, cupo = True):
    if cupo == False:
        m = r = q = 0
    else:
        m = r = q = 30
    df = generar_instancia(K)
    solver, x = modelo_master(df['Mujer'], df['Interior'], df['Pobres'], df['Score'], m, r, q, N, modelo)
    status = solver.Solve()
    X = np.zeros(K)
    if status == pywraplp.Solver.OPTIMAL:
        for t in range(K):
            if x[t].solution_value() != 0:
                X[t] = x[t].solution_value()
    #else:
        #print("The problem does not have an optimal solution.")
    df['X'] = X
    return df


average_Habilidad_cupos = []
i=0
while i < 100:
    df = admitir(m=0.3,q=0,r=0,cupo=True, modelo=3)
    if sum(df['X'])==50:
        average_Habilidad_cupos += [np.mean(df['Habilidad'][df['X']==1])]
        i +=1


average_Habilidad_sin_cupos = []
i=0
while i < 100:
    df = admitir(cupo=False, modelo=3)
    if sum(df['X'])==50:
        average_Habilidad_sin_cupos += [np.mean(df['Habilidad'][df['X']==1])]
        i +=1


#plt.hist(average_Habilidad_cupos,bins = range(100,125),label='con cupos',alpha=0.6,density = True)
#plt.hist(average_Habilidad_sin_cupos,bins = range(100,125),label = 'sin cupos',alpha=0.6,density = True)
#plt.legend()
#plt.xlabel('Habilidad')
#plt.show()
print(f'average Habilidad con cupo {np.mean(average_Habilidad_cupos)}')
print(f'average Habilidad sin cupo {np.mean(average_Habilidad_sin_cupos)}')
