set N :=  {1..100};
set J := {1..10};

# enunciado
param d[J]:= read "clase4.txt" as "<1n> 2n" skip 1;
param k[J]:= read "clase4.txt" as "<1n> 3n" skip 1;
param b[J]:= read "clase4.txt" as "<1n> 4n" skip 1;
param g[J]:= read "clase4.txt" as "<1n> 5n" skip 1;

var e[N*J] binary; # e[n, j] = 1 <=> empleado n asignado a tarea j
var r[J] binary; # r[j] = 1 <=> se realiza la tarea j

# función a trozos
set S:= {1..3};
set K:= {1..6};
param A[K] := <1> 1, <2> 4, <3> 5, <4> 6, <5> 7, <6> 9;
param B[K] := <1> 1, <2> 4, <3> 3, <4> 2, <5> 4, <6> 8;
var delta[S] binary;
var lambda[K] real;
var b4 real;

maximize f: b4 * r[4] + sum <j> in J: r[j] *(b[j] + g[j] * sum <n> in N: e[n, j]);

subto r1: forall <j> in J: sum <n> in N: e[n, j] <= k[j];   # menos de kj empleados por tarea
subto r2: forall <n> in N: sum <j> in J: e[n, j] <= 2;  # a lo sumo 2 tareas por empleado

# tarea 4
subto t1: sum <s> in S: delta[s] == 1;
subto t2: forall <s> in S: lambda[2*s-1] + lambda[2*s] == delta[s];
subto t3: sum <n> in N: e[n, 4] == sum <i> in K: A[i] * lambda[i];
subto t4: b4 == sum <i> in K: B[i] * lambda[i];
subto t5: forall <i> in K: lambda[i] >= 0;
subto t6: lambda[card(K)] <= 1 - 0.00001;

# relacion entre las variables
subto v1: forall <j> in J: sum <n> in N: e[n, j] <= card(N)*r[j];
subto v2: forall <j> in J: - sum <n> in N: e[n, j] <= -1 + card(N)*(1-r[j]);

# depto. RRHH
subto rrhh1: forall <j> in J: e[3, j] == e[5, j];
subto rrhh2: forall <j> in J: e[1, j] <= 10*(1-e[11, j]); # e1j >= 1 ==> e11j = 0
subto rrhh3: e[6, 10] == 1;
subto rrhh4: e[8, 5] + e[8, 2] == 1;