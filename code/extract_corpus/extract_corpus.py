import xml.etree.ElementTree as etree
import re
import os.path
import time

PATH_WIKI_XML = '../Data' # Emplacement du dossier contenant le fichier xml
FILE_NAME_WIKI = 'frwiki.xml' # Nom du fichier xml

FULL_PATH = os.path.join(PATH_WIKI_XML,FILE_NAME_WIKI ) # Retourne le chemin relatif vers notre fichier .xml (grâce à abspath)



############################################################################################
#  Objectif : Parcourire tout le fichier et extraire les balises id / page / title / text  #
# 	          Minimiser au plus les aupérations                                            #
############################################################################################




#-----------theme----------------
notre_theme=['software', 'informatique', 'algorithme', 'code', 'logiciel', 'application', 'programme', 'systeme', 'hardware', 'ordinateur', 'machine', 'processeur', 'CPU', 'processus', 'registre', 'memoire', 'RAM', 'complexite', 'architecture', 'reseau', 'protocole', 'TCP', 'UDP', 'connecter', 'sécurité', 'Authentification', 'internet', 'exploitation', 'UNIX', 'macOS', 'Windows', 'Linux', 'FreeBSD', 'Android', 'iOS', 'Java', 'python', 'C++', 'Ruby', 'PHP', 'C/C++', 'C', 'JavaScript', 'HTML', 'CSS', 'SQL', 'Scala', 'Swift', 'C#', 'Go', 'Shell', 'OCaml', 'framework', 'laravel', 'angular', 'angularJS', 'Symfony', 'Bootstrap', 'script', 'fichier', 'repertoire']

#------------ extraire les données par regex ---------------
lien_externe_line= re.compile(r"\{\{(.*?)\}\}",re.MULTILINE )# On supprimer les {{}} sur une ligne 
lien_externe_multi= re.compile(r"\{\{(.+?)\}\}",re.DOTALL )# On supprime les {{}} sur plusieurs lignes (probleme si on fait au mm temps line et multiline)


# Les pathes sont former de {}tag donc on veut laisser que le tag
def strip_tag_name(t):
    t = t
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

# --------------- Calculer le nombre d'occuprence dans chaque page pour la choisir ou pas ------------- 
def nbr_Occurence(corps,title,notre_theme): 
    i = 0
    for x in notre_theme:
        i = i + corps.count(x)
        i = i + title.count(x)
    return i

#----------------- Supprimer les [] et garder les liens interne [[]] -----------------
def delete_accolade(text): 
	allpar = re.compile(r'\[.*?\]',re.DOTALL )
	m = allpar.finditer(text)
	if ( m != None):
		for x in m:
			if x.group(0)[0:2]!="[[":
				text = text.replace(x.group(0),'')
	return text
	
#------------ Suppression des liens externes entre {{}} ------------------------------
def supprimer_lien_externe(text): 
	lien = lien_externe_line.finditer(text)
	if ( lien != None):
		for x in lien:
			text = text.replace(x.group(0),'')
	lienn = lien_externe_multi.finditer(text)
	if ( lienn != None):
		for x in lienn:
			text = text.replace(x.group(0),'')

	return text

def nettoyage(text):
	text = supprimer_lien_externe(text)		
	text = delete_accolade(text)

	text = re.sub(r'\{(.+?)\}','',text,flags=re.DOTALL)					# Supprimer les '{ }' 
	text = re.sub(r'<','',text,flags=re.DOTALL) 						# Supprimer les '<' 
	text = re.sub(r'\*','',text,flags=re.DOTALL) 						# Supprimer les '*' 
	text = re.sub(r'>','',text,flags=re.DOTALL) 						# Supprimer les '>' 
	text = re.sub(r'&','',text,flags=re.DOTALL) 						# Supprimer les '&' 
	text = re.sub(r'\}\}','',text,flags=re.DOTALL)						# Supprimer les '}}' 
	text = re.sub(r'<.*?>','',text, flags=re.MULTILINE)					# Supprimer les balise inutile
	
	text = re.sub(r'(\=\=\=?).+?(\=\=\=?)','',text,flags=re.MULTILINE)  # Supprimer les lines qui contient ===  ===
	text = re.sub(r'\{\|.*?\s\|\}','',text,flags=re.DOTALL) 	    	# Supprimer les {\\ \\} contient du code css 
	
	text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)          
	text = re.sub(r'\[\[(Image:|:Catégorie:|Fichier:|Catégorie:).*?]]','',text, flags=re.MULTILINE)     
	text = re.sub(r"(\w|\.|\-|\/|\?|\=|\&|\%)*.(jpg|gif|png|bmp|JPEG|JPG|svg)",'',text,flags=re.DOTALL)

	text = text=re.sub(r"(\w|\.|\-|\/|\?|\=|\&|\%)*.(com|net|dz|fr|org|gov|edu|int|arpa|blog|au|aspx|eu|de|asp|be|ca|COM|de)/?\b",'',text,flags=re.DOTALL)
	text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))','',text,flags=re.DOTALL)

	return text


# Recuperer le corpus des mots choisis
def getCorpus():# Recupperer le corpus des mots choisis

	openfile= False

	title= '' # Pour récupérer le titre des différentes pages
	nbr_page= 0 # nombre de page
	corps= None # Contient la partie "text" des pages qui détient les informations principales
	
	fixed_nombre_occ = 10 # Nombre d'occurence des mots > 10 (après 10 apparition de 10 mots dans le context de l'informatique dans la page, on juge que 
	                      # se domaine appartient bien au domaine de l'informatique)
	nombre_occ_found= 0 # Nombre d'occurence de mots liée à l'informatique trouvée dans la page
	nbr_page_total = 0	  # Nombre de page total du fichier wikipédia
	
	dictPage= []
	
	file1='output-corpus1.xml'
	file2='output-corpus2.xml'

	df= 0
	i= 1
	while(i < 3):
		df=open('output-corpus'+str(i)+'.xml','w')
		df.write('\n<?xml version ="1.0" encoding ="UTF-8" ?>\n')
		df.write('<root>\n')
		df.close()
		i+=1
	i=0
	
	for event, elem in etree.iterparse(FULL_PATH, events=('start', 'end')):
		tname = strip_tag_name(elem.tag)

		if event == 'start':
			# Pour chaque nouvelle page initialiser les variablle
			if tname == 'page':
				title = ''
				inrevision = False # Pour eviter le probleme de recuperer id + dautre info
			elif tname == 'revision':
				inrevision = True
			elif tname == 'title': # Recuperer le titre de la page 
				title = elem.text			
			elif tname=='text': # Recuperer le text de la page 
				corps=elem.text
		else:

			if tname == 'page': # Pour compter nombre de page du fichier 
				nbr_page_total += 1
			if tname=='text': # A la fin de la balise <text> quon peut recuperer le text sinon none
				              #recuperer le corps de la page
				if(corps == None):
					corps= elem.text
					try:
						text5= corps
					except TypeError:
						corps=''
						title= ''
						continue
				
				if (title!=None and corps!=None):
					if ('Wikipédia' in title or 'Projet:' in title or 'Modèle:' in title or 'Portail:' in title):
						corps=''
						title = ''
						continue
					nombre_occ_found= nbr_Occurence(corps,title,notre_theme)

					if(nombre_occ_found>=fixed_nombre_occ):
						text2=nettoyage(corps)
						#print(corps[:20])
						
						title= re.sub(r'&','',title,flags=re.DOTALL) # Supprimer les {||} contient du code css 
						if (str(nbr_page)!=None and str(nbr_page)!='None' and title!=None and title!='None' and title!='' and title not in dictPage  and nbr_page<200000 ):
							print(str(nbr_page),title)
							dictPage.append(title)
							if (int(nbr_page/100000)==i and openfile==False ):#chaque fichier contient 50k page
								x='output-corpus'+str(i+1)+'.xml'

								df=open(x,'a')
								openfile=True
							

							df.write('	<page>\n')
							df.write('		<id>'+str(nbr_page)+'</id>\n')
							df.write('		<title>'+title+'</title>\n')
							df.write('		<text>' +text2 +'</text>\n')
							df.write('	</page>\n')
							nbr_page+= 1
							print('nombre de page :'+ str(nbr_page))
							if (nbr_page==100000 or nbr_page ==200000):
								df.write('</root>\n')
								df.close()
								i+=1
								openfile=False
								if nbr_page == 200000:
									break
						nombre_occ_found= 0
						
		elem.clear()

	print('nombre de page trouvées :', nbr_page)
	print('nombre de page du fichier total parcouru :', nbr_page_total)
	return nbr_page


#********************** Debut du programme principale ************************
print('calcule du corpus ...\n')

start_time_corpus = time.time()
getCorpus()
time.sleep(1) #Juste pour voir que ça marche (Sur le mini fichier c'est trop rapide)
done_time_corpus = time.time()
elapsed_time_corpus = done_time_corpus - start_time_corpus

def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

print("Le Corpus a été généré en ", convert(elapsed_time_corpus))

