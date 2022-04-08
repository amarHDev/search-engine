from nltk.probability import FreqDist

idf = FreqDist()

titles_file = open('./final/titres_final.txt','r')
textes_file = open('./final/textes_final.txt','r')
dict = open('./final/dictionnary.txt','r').readline().split()
unique_words = []

for i in range(200000):
    title = titles_file.readline().split()
    content = textes_file.readline().split()
    content += title
    
    print(i)
    unique_words = []
    for word in content:
        if word not in unique_words and word in dict:
            unique_words.append(word)

    for word in unique_words:
        idf[dict.index(word)] += 1


import math
idf_result = list(idf.most_common())
idf_result.sort(key=lambda y: y[0])

result_final = ['' for i in range(200000)]
for x in idf_result:
    result_final[x[0]] = str(float("{:.6f}".format(math.log10(200000/x[1]))))

print(result_final[:10])

with open('./final/idf.txt','w') as f:
    f.write('/'.join(result_final))

