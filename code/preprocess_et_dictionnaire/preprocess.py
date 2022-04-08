# Text preprocessing function
from distutils.command.clean import clean
from itertools import count
from turtle import title
from unittest import result
import nltk 

#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import FrenchStemmer
from spellchecker import SpellChecker

import re

# data cleaning
def clean_data(text):
    text = str(text).lower()
    text = text.replace("è","e")
    text = text.replace("é","e")
    text = text.replace("ê","e") 
    text = text.replace("à","a")
    text = text.replace("ù","u")
    text = text.replace("ç","c")
    text = text.replace("â","a")
    #text = text.replace("à","a")

    # This removes words of up to 2 characters entirely
    # (Don't include the spaces ==> use \b)
    text = re.sub(r'\b\w{1,1}\b', '', text)

    text = re.sub(r"[^a-zA-Z]", " ", text)
    return text


def preprocess(text):
    # clean data
    text = clean_data(text)

    # word tokenization
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = stopwords.words("french")
    words = [word for word in tokens if word not in stop_words]

    # correct words 
    #spell = SpellChecker(language='fr')
    #correct_words = [spell.correction(word) for word in words]

    # stemming
    stemmer = FrenchStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]

    # significant words
    result = [word for word in stemmed_words if len(word) > 2]

    ##return " ".join(stemmed_words)
    return result


import os
import xml.etree.ElementTree as ET

# count words in a dictionnary
from nltk.probability import FreqDist

PATH_WIKI_XML = 'final' #Emplacement du dossier contenant le fichier xml
FILE_NAME_WIKI = 'corpus_final.xml' #nom du fichier xml de notre corpus

FULL_PATH = os.path.abspath(os.path.join(PATH_WIKI_XML,FILE_NAME_WIKI )) #Retourne le chemin absolu vers notre fichier .xml (grâce à abspath)
fdist = FreqDist()
idf = FreqDist()

def getPages():
    ## dans les 2 fichiers suivants, on met le texte pre-traite de chaque page
    titles_file = open('./final/titres_final.txt','w')
    textes_file = open('./final/textes_final.txt','w')
    id = -1
    cpt = 0
    for event, elem in ET.iterparse(FULL_PATH, events=('start', 'end')):
        if event == 'end':
            if  elem.tag == 'id':
                id = int(elem.text)
                print("id : "+str(id))

            if  elem.tag == 'title':
                title_words = preprocess(elem.text)
                titles_file.write(" ".join(title_words)+'\n')
                for word in title_words:
                    fdist[word] += 1000

            if  elem.tag == 'text':
                cpt += 1
                print(cpt)
                text_words = preprocess(elem.text)
                textes_file.write(" ".join(text_words)+'\n')
                for word in text_words:
                    fdist[word] += 1


## lancer la fonction principale
getPages()

## recuperer les 10000 mots les plus frequents
first_tuple_elements = [a_tuple[0] for a_tuple in fdist.most_common(10000)]

## trier par ordre alphabetique
first_tuple_elements = sorted(first_tuple_elements)
dictionary = " ".join(first_tuple_elements)

## ecrire le dictionnaire dans un fichier text
with open('./final/dictionnary.txt', 'w') as fout:
    fout.write(dictionary)

print("finish")
