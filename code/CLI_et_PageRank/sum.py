vecteur = open('./pagerank.txt','r').readline().split('/')
sum = 0
for element in vecteur:
    sum += float(element)

print(sum)