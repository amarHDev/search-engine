import time

from chemins import PATH_TO_XML_CORPUS, path_to_lst_pages_au_contenu_brut, \
    path_to_lst_of_tuples_containing_lst_of_links, path_to_cli_vectors

from analyse import get_lst_pages_au_contenu_brut, get_lst_of_links_from_lst_of_pages, cree_cli

from utils import serialize, hour_min_sec_format, deserialize


def analyse_et_serialisation():
    """
    Analyse du corpus obtenu afin de :
        (principalement)
        * Créer la matrice du graphe de ce corpus sous format CLI
        * Créer le pagerank.

    :return: void (génère les fichier 'cli_vectors.ser')
    """
    start_time = time.time()

    print(" \t-> Début de l'analyse syntaxique du corpus (parsing)")
    lst_pages_au_contenu_brut = get_lst_pages_au_contenu_brut(PATH_TO_XML_CORPUS)

    # print(" \t-> Commencer la sérialisation de la liste des pages au contenu brut")
    # serialize(lst_pages_au_contenu_brut, path_to_lst_pages_au_contenu_brut)

    # print(" \t-> Commencer à deserialiser lst_pages_au_contenu_brut")
    # lst_pages_au_contenu_brut = deserialize(path_to_lst_pages_au_contenu_brut)

    print(" \t-> Commencer à créer la liste des tuples contenant chacun une liste de liens")
    lst_of_tuples_containing_lst_of_links = get_lst_of_links_from_lst_of_pages(lst_pages_au_contenu_brut)

    # print(" commencer à serialiser la liste des tuples contenant chacun une liste de liens")
    # serialize(lst_of_tuples_containing_lst_of_links, path_to_lst_of_tuples_containing_lst_of_links)

    # print(" \t-> Commencer à deserialiser la liste des tuple contenant chacun une liste de liens")
    # lst_of_tuples_containing_lst_of_links = deserialize(path_to_lst_of_tuples_containing_lst_of_links)

    print("\t-> Commencer la création de la matrice sous le format CLI")
    (C, L, I) = cree_cli(lst_of_tuples_containing_lst_of_links)

    print("\t-> Commencer la sérialisation de la matrice qui est sous le format CLI")
    serialize((C, L, I), path_to_cli_vectors)

    print("\t-> Commencer à désérialisation de la matrice qui est sous le format CLI")
    C, L, I = deserialize(path_to_cli_vectors)

    print("taille C : ", len(C))
    print("taille L : ", len(L))
    print("taille I : ", len(I))

    print("\n\n\n\t\t### Fin ###")
    elapsed_time = time.time() - start_time
    print(" \t\t==>Temps total écoulé (pour l'analyse du corpus et les serialisations) : {}".format(
        hour_min_sec_format(elapsed_time)))


# Debut du programme principal pour CLI
analyse_et_serialisation()
