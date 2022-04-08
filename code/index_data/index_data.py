
import os
import xml.etree.ElementTree as ET

import requests
import json
import re

#######################################
######## indexation de donnees ########
#######################################


PATH_WIKI_XML = 'final' #Emplacement du dossier contenant le fichier xml
FILE_NAME_WIKI = 'corpus_final.xml' #nom du fichier xml

FULL_PATH = os.path.abspath(os.path.join(PATH_WIKI_XML,FILE_NAME_WIKI )) #Retourne le chemin absolu vers notre fichier .xml (grâce à abspath)

def clean_data(text):
    # This removes words of up to 2 characters entirely
    # (Don't include the spaces ==> use \b)
    text = re.sub("\]|\'|\[", '', text)
    text = text.replace("'''","'")
    text = text.replace("''","'")
    text = text.replace("|"," | ")
    return text


data = {
    "id": -1,
    "title": "",
    "text":"",
    "resume":"",
    "link": ""
}

def postData(data):
    url = 'http://127.0.0.1:8000/api/page-create/'
    headers = {'Content-Type' : 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)

def indexPages():
    id = -1
    cpt = 0
    for event, elem in ET.iterparse(FULL_PATH, events=('start', 'end')):
        if event == 'end':
            if  elem.tag == 'id':
                data['id'] = int(elem.text)
                print("id : "+str(data['id']))
                cpt += 1

            if  elem.tag == 'title':
                data['title'] = elem.text
                data['link'] = "https://fr.wikipedia.org/wiki/"+'_'.join(elem.text.split())
                cpt += 1

            if  elem.tag == 'text':
                data['resume'] = clean_data(' '.join(elem.text.split()[:20]))+'...'
                data['text'] = elem.text
                cpt += 1
                
            if  cpt == 3:
                postData(data)
                cpt = 0
                data['id']= -1
                data['title']= ""
                data['link']= ""
                data['text']= ""
                

indexPages()