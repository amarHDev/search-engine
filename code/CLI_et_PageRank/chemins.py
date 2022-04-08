import os

PATH_TO_OUTPUT_FOLDER = '../data/out/'
PATH_TO_DATA_FOLDER = '../data/'

XML_CORPUS_FILENAME = 'corpus.xml'
PATH_TO_XML_CORPUS = os.path.join(PATH_TO_DATA_FOLDER, XML_CORPUS_FILENAME)

LST_PAGES_AU_CONTENU_BRUT_FILENAME = 'lst_pages_au_contenu_brut.ser'  # .ser for "serialized"
path_to_lst_pages_au_contenu_brut = os.path.join(PATH_TO_OUTPUT_FOLDER, LST_PAGES_AU_CONTENU_BRUT_FILENAME)

LST_OF_TUPLES_CONTAINING_LST_OF_LINKS_FILENAME = 'lst_of_tuples_containing_lst_of_links.ser'
path_to_lst_of_tuples_containing_lst_of_links = os.path.join(PATH_TO_OUTPUT_FOLDER,
                                                             LST_OF_TUPLES_CONTAINING_LST_OF_LINKS_FILENAME)

LST_PAGES_AU_CONTENU_CLAIR_FILENAME = 'lst_pages_au_contenu_clair.ser'
path_to_lst_pages_au_contenu_clair = os.path.join(PATH_TO_OUTPUT_FOLDER, LST_PAGES_AU_CONTENU_CLAIR_FILENAME)

LST_PAGES_AU_CONTENU_CLAIR_COUPE_FILENAME = 'lst_pages_au_contenu_clair_coupe.ser'
path_to_lst_pages_au_contenu_clair_coupe = os.path.join(PATH_TO_OUTPUT_FOLDER,
                                                        LST_PAGES_AU_CONTENU_CLAIR_COUPE_FILENAME)

CLI_VECTORS_FILENAME = 'cli_vectors.ser'
path_to_cli_vectors = os.path.join(PATH_TO_OUTPUT_FOLDER, CLI_VECTORS_FILENAME)

DICO_ID_TITRE_FILENAME = 'dico_id_titre.ser'
path_to_dico_id_titre = os.path.join(PATH_TO_OUTPUT_FOLDER, DICO_ID_TITRE_FILENAME)

DICO_TITRE_ID_FILENAME = 'dico_titre_id.ser'
path_to_dico_titre_id = os.path.join(PATH_TO_OUTPUT_FOLDER, DICO_TITRE_ID_FILENAME)
