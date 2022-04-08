# Pickle in Python is primarily used in serializing and deserializing a Python object structure.
# (In other words, it's the process of converting a Python object into a byte stream to store it in a file/database)
import pickle

import sys


def print_percentage(current_i, max_size):
    if current_i % 1000 == 0:
        print("\t\t %.3f" % (current_i / max_size * 100), " %")


# Affichage du temps
def hour_min_sec_format(temps_ecoule_en_secondes):
    h = int(temps_ecoule_en_secondes / (60 * 60))
    m = int((temps_ecoule_en_secondes % (60 * 60)) / 60)
    s = temps_ecoule_en_secondes % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def serialize(obj, path_to_output_file):
    """

    :param obj: l'objet à serialiser
    :param path_to_output_file: le fichier où le résultat de la serialisation sera ecrit.
    :return: void
    """
    # wb mode : write and binary mode
    print("taille de l'objet à serialiser : " + str(sys.getsizeof(obj)),
          ' octets (', str(sys.getsizeof(obj) / 1024), 'kilobytes)')
    # input()
    with open(path_to_output_file, "wb") as file:
        file.write(pickle.dumps(obj))
    print("sérialisation réussie, résultat dans : ", path_to_output_file.split('/')[-1])


def deserialize(path):
    with open(path, "rb") as file:
        return pickle.load(file)


def get_internal_links(text_of_current_page):
    """
    :param text_of_current_page: le texte (content) de la page
    :return: La liste des liens internes (de frwiki à frwiki) de la page
    """
    import re
    internal_links_regex = re.compile(r'\[\[.*?\]\]')
    lst_internal_links_of_current_page = internal_links_regex.findall(text_of_current_page)

    # [[nom de la page wikipedia à laquelle on fait référence | texte affiché dans la page courante]]
    # example : [[lycée Théodore-de-Banville|lycée]]
    # nous, on ne prends que la 1ere partie (jusqu'à la barre verticale '|' si elle y a eu lieu,
    # sinon jusqu'au dernier caractère avant les deux crochets fermants ']]')
    return [link[2:-2].split("|")[0] for link in lst_internal_links_of_current_page]
