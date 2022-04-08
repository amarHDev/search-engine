import math

dict = open('./data/structures/dictionnary.txt','r').readline().split()
tf_file = open('.data/structures/tf/tf.txt','w')

titles_file = open('./data/titres.txt','r')
textes_file = open('./data/textes.txt','r')

titles = titles_file.readlines()
contents = textes_file.readlines()

tf = []
page = []

def words_indexes(unique_list):
    index = []
    for word in unique_list:
        if word in dict:
            index.append(int(dict.index(word)))

    index.sort()
    return index


data_tf =''
for i in range(0, 200000):
    print(i)
    unique_words = []
    index = []
    ligne = ''
    title = titles[i].split()
    content = contents[i].split()
    page_content = title + content
    for word in page_content:
        if word not in unique_words:
            unique_words.append(word)

    index = words_indexes(unique_words)

    for word_index in index:
        count = page_content.count(dict[word_index])
        log_num = 1 + math.log10(float(count))
        log_num = float("{:.6f}".format(log_num))
        ligne += str(word_index)+','+str(float(log_num))+'/'
           
    ligne = ligne[:len(ligne)-1]
    tf_file.write(ligne+'\n')

tf_file.close()

