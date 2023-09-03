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