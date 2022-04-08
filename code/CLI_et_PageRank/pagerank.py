from chemins import path_to_cli_vectors
from utils import deserialize, print_percentage

import numpy as np


def normalize_vector(v):
    v = np.array(v)
    normalized_v = list(v / np.sqrt(np.sum(v ** 2)))
    normalized_v = [float("{:.6f}".format(x)) for x in normalized_v]
    return normalized_v


C, L, I = deserialize(path_to_cli_vectors)
n = len(L) - 1

new_matrix = []

# calcul
a = 0
Pi = [0 for i in range(n)]
# V = [1/4,1/4,1/4,1/4]
V = [(1 / n) for _ in range(n)]
epsilon = 1 / 7


def produit_matriciel():
    T = [0 for i in range(n)]
    for i in range(n):
        print_percentage(i, n)
        for j in range(L[i], L[i + 1]):
            T[I[j]] += C[j] * V[i]

        if L[i] == L[i + 1]:
            for j in range(n):
                T[j] += (1 / n) * V[i]

    sum_v = sum(V)
    for i in range(len(T)):
        print_percentage(i, len(T))
        Pi[i] = (1 - epsilon) * T[i] + (epsilon / n) * sum_v
        V[i] = Pi[i]

# pagerank
mysum = []
for i in range(50):
    print("itér : \n", i)
    produit_matriciel()
    mysum.append(sum(Pi))

file = open('./pagerank.txt', 'w')
file.write('/'.join([str(x) for x in Pi]))
file = open('./sum.txt', 'w')
file.write('|'.join([str(x) for x in mysum]))

print(mysum)