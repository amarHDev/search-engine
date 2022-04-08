import xml.etree.ElementTree as ET
from utils import print_percentage, hour_min_sec_format, get_internal_links
import time


def get_lst_pages_au_contenu_brut(file_name, max_num_of_pages=200000):
    """
    :param file_name: notre corpus (fichier XML)
    :param max_num_of_pages: nombre maximal de pages à récupérer (à ajouter dans la liste)

    :return: Liste de tuples sous forme (id, title, content) pour chaque page
    """
    start_time = time.time()

    # liste des pages au contenu à l'état brut (car il y a encore les [[]] pour constuire le graphe et mat CLI par la
    # suite)
    lst_pages_au_contenu_brut = []
    compteur_de_pages = 0

    id_page = None
    titre_page = None
    contenu_page = None

    for event, elem in ET.iterparse(file_name, events=('start', 'end')):
        tag = elem.tag

        if event == 'start':

            if tag == 'page':
                # initialization des champs de la nouvelle page :
                titre_page = ''
                id_page = -1
                contenu_page = ''
        else:
            if tag == 'title':
                titre_page = elem.text

            elif tag == 'id':
                id_page = int(elem.text)

            elif tag == 'text':
                contenu_page = elem.text

            elif tag == 'page':
                compteur_de_pages += 1
                lst_pages_au_contenu_brut.append((id_page, titre_page, contenu_page))
                print_percentage(compteur_de_pages, max_num_of_pages)

            # Afin de libérer de la mémoire:
            elem.clear()

    temps_ecoule = time.time() - start_time
    print("\n==>Fin de l'analyse (parsing) du corpus")
    print("==>Temps écoulé pour l'analyse (parsing) du corpus : {}".format(hour_min_sec_format(temps_ecoule)))

    return lst_pages_au_contenu_brut


def get_lst_of_links_from_lst_of_pages(lst_pages_au_contenu_brut):
    """
    :param lst_pages_au_contenu_brut: liste des pages au contenu brut sous forme d'un 3-uplet (id_of_current_page,
    title_of_current_page, content_of_current_page)

    :return: liste de tuples (id_of_current_page, title_of_current_page, lst_links[]) où lst_links[] est la liste
             des liens internes correspondant à la page identifiée par (id_of_current_page, title_of_current_page)
    """
    start_time = time.time()
    lst_of_tuples_containing_lst_of_links = []

    for counter, (id_of_current_page, title_of_current_page, content_of_current_page) in enumerate(
            lst_pages_au_contenu_brut):
        # links c'est la liste des titres cibles (en partant de la page courante)
        links = get_internal_links(content_of_current_page)
        lst_of_tuples_containing_lst_of_links.append((id_of_current_page, title_of_current_page, links))
        print_percentage(counter, len(lst_pages_au_contenu_brut))

    elapsed_time = time.time() - start_time
    print("\n==>Fin de la récupération des liens lst_of_links_from_lst_of_pages")
    print("==>Temps écoulé pour la récupération des liens lst_of_links_from_lst_of_pages: {}".format(
        hour_min_sec_format(elapsed_time)))
    return lst_of_tuples_containing_lst_of_links


def cree_cli(lst_of_tuples_containing_lst_of_links):
    """
    la matrice est construite à partir du graphe de notre corpus,
    chaque noeud de ce graphe représente une page du corpus, et les arcs représentent les liens entres ces pages.

    :param lst_of_tuples_containing_lst_of_links: la liste de tous les liens sous forme de tuples
                                  contenant (id_de_la_page, titre_de_la_page, liste_de_liens_de_cette_page)
                                   où liste_de_liens_de_cette_page est la liste des titres cibles
                                   (en partant de la page courante (id_de_la_page, titre_de_la_page))

    :return: Matrice d'adjacence du graphe de notre corpus sous le format CLI
    """
    start_time = time.time()
    nbr_total_de_pages = len(lst_of_tuples_containing_lst_of_links)
    nodes_dico = {}
    edges_dico = {}

    # remplir le dictionnaire 'nodes_dico' des noeuds (sous forme :
    # "titre de la page" : indice du tuple (contenant ce titre en question) dans la liste des tuples)
    for index_of_tuple_in_the_lst, (_, title, _) in enumerate(lst_of_tuples_containing_lst_of_links):
        nodes_dico[title] = index_of_tuple_in_the_lst

    # remplir le dictionnaire 'edges_dico' des arcs (sous forme :
    # un indice dans la liste des tuples : la liste des liens (pages cibles) partant de la page du tuple à cet indice)
    for _, index_of_tuple_in_the_lst in nodes_dico.items():
        # Pour chaque page (car il y a exactement une page à chaque indice de la liste),
        # on crée la liste des liens internes à notre corpus
        edges_dico[index_of_tuple_in_the_lst] = [lien for lien in
                                                 lst_of_tuples_containing_lst_of_links[index_of_tuple_in_the_lst][2] if
                                                 lien in nodes_dico.keys()]  # c'est ici qu'on vérifie s'il est interne

    C = []  # len = m (avac m = nbr d'entrees non nulles)
    L = [0]  # len = n+1 (avec n = nbr total de noeuds)
    I = []  # len = m

    for index_of_src_tuple, _ in enumerate(lst_of_tuples_containing_lst_of_links):
        lst_des_liens = edges_dico[index_of_src_tuple]
        degre_sortant = len(lst_des_liens)

        for lien in lst_des_liens:
            # s'il ne s'agit pas d'un lien interne à notre corpus, on ne le traite pas
            if lien not in nodes_dico.keys():
                continue

            # à cet endroit on est sûr d'avoir au moins un arc (==> coef !=0, donc on l'ajoute à C)
            coef = 1 / degre_sortant if degre_sortant > 0 else 0
            C.append(coef)
            index_of_target_tuple = nodes_dico[lien]
            I.append(index_of_target_tuple)

        L.append(L[-1] + degre_sortant)
        print_percentage(index_of_src_tuple, nbr_total_de_pages)

    elapsed_time = time.time() - start_time
    print("\n==>Fin de la création de la matrice sous le format CLI")
    print(" ==>Temps écoulé pour créer la matrice sous le format CLI : {}".format(hour_min_sec_format(elapsed_time)))
    return C, L, I
