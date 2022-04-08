import math
import numpy as np

tf_lines = open('./final/tf_final/tf.txt','r').readlines()

## ici on stock la relation mot-page
tf_normalized = open('./final/tf_final/mot_page_normalized.txt','w')

relation_mots_pages = ['' for i in range(10000)]

## normaliser le vecteur tf recupere et stocker ces elements dans la relation mot-page
def vecteur_normalize(line, page_number):
    mot_indexes = []
    tf_values = []
    for element in line.split('/'):
        element = element.split(',')
        mot_indexes.append(int(element[0]))
        tf_values.append(float(element[1]))

    tf_values= np.array(tf_values)
    normalized_v = list(tf_values / np.sqrt(np.sum(tf_values**2)))
    normalized_v = [float("{:.6f}".format(x)) for x in normalized_v]

    for i in range(len(mot_indexes)):
        relation_mots_pages[mot_indexes[i]] +=  str(page_number)+','+str(normalized_v[i]) + '/'
        

## pour chaque line du fichier tf, qui represente le tf d'une page
for i in range(len(tf_lines)) : 
    print(i)
    if len(tf_lines[i])>4:
        ## on normalise le tf de la page
        vecteur_normalize(tf_lines[i],i)


## enregistrer la structure mot-page dans un fichier texte
for item in relation_mots_pages:
    tf_normalized.write(item[:len(item)-1]+'\n')