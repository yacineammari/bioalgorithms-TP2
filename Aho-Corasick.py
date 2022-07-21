import random
import string
import networkx as nx
import matplotlib.pyplot as plt

class noud:
    def __init__(self, id, val, cost, parent):
        self.id = id
        self.cost = cost
        self.output = []
        self.val = val
        self.go_to = None
        self.failur_go_to = []
        self.is_final = False
        self.parent = parent

def get_pref(lisf_des_motif):

    list_des_pref = []  # list of pref
    list_des_pref.append('')  # empty word

    # calculating prefix
    for motif in lisf_des_motif:
        motif = motif.upper()  # capitalize our text
        pref = ''
        for pointeur in motif:
            # return the sub-word from start to the of poiteur
            pref = pref + pointeur
            # check if pref is alrady in list
            if not pref_found(pref, list_des_pref):
                list_des_pref.append(pref)

    return list_des_pref


def pref_found(pref, list_of_pref):
    for elem in list_of_pref:
        if elem == pref:
            return True

    return False


def get_sufix_prop(pref):
    if pref != '':
        list_des_suff_prop = []  # list of clean sufix
        list_des_suff_prop.append('')  # empty word

        index = len(pref)-1  # true pos

        while(index > 0):
            # appending from my index to the last character
            list_des_suff_prop.append(pref[index::])
            index -= 1  # adding next character

        try:
            # removing the word if self if it's in the list and returning the list
            return list_des_suff_prop.remove(pref)

        except ValueError:
            return list_des_suff_prop


def fun_echec(list_des_pref):
    relation_echec = {}

    for pref in list_des_pref:
        if pref != '':
            # calculating clean sufix
            sufix_prop = get_sufix_prop(pref)
            # (list des sufix) innerjoin (list de prefix)
            not_found = True
            while not_found:
                # longest clean sufix
                longest_sufix = max(sufix_prop, key=len)

                # check if the longest clean sufix is in the list of prefix or if the list in empty
                if pref_found(longest_sufix, list_des_pref) or len(sufix_prop) == 0:
                    not_found = False
                    relation_echec[pref] = longest_sufix
                else:
                    sufix_prop.remove(longest_sufix)

    return relation_echec


def fun_set_failer_list(aho_atuom, list_des_pref):
    etats = fun_echec(list_des_pref)
    etats[''] = ''
    # looking for nodue id
    for aho_etat in aho_atuom.values():
        for pos_aho in aho_atuom.values():
            if aho_etat[2].id != 0:
                if ((etats[aho_etat[2].val] == pos_aho[2].val) and (pos_aho[2].id != aho_etat[2].id)):
                    aho_etat[2].failur_go_to.append(pos_aho[2].id)

    aho_atuom[0][2].failur_go_to.append(0)
    return aho_atuom


def set_sortie(list_des_motif, aho_atuom):
    for aho_etat in aho_atuom.values():

        if aho_etat[2].id != 0:
            # calculate the list of suffex
            list_des_suffix = get_sufix_prop(aho_etat[2].val)
            # appending the word it self
            list_des_suffix.append(aho_etat[2].val)

            # we test if every suffix of automate words existe in the list of motifs and if
            # it dose we sate the state to finale an append the the suffix in the output list
            for suffix in list_des_suffix:
                if (pref_found(suffix, list_des_motif)):
                    aho_etat[2].is_final = True
                    aho_etat[2].output.append(suffix)

    return aho_atuom


def go_next(ahom, text, current_state):
    # change the state to the next one
    if ahom[current_state][2].go_to != None:
        try:
            return ahom[current_state][2].go_to[text]
        except KeyError:
            return None

    else:
        return None


def fun_find_parent_id(elem, aho_autom):

    for aho_elem in aho_autom.values():
        if aho_elem[2].val == elem[:-1]:
            return aho_elem[2].id

    return 0


def init_aho_autom(list_des_motif):

    aho_dict = {}  # automate

    id_cpt = 0  # noude id

    list_pref = []  # the mini list of pref
    main_list_des_pref = []  # main list of pref

    # init root noud
    root = noud(id_cpt, '', '', None)
    aho_dict[id_cpt] = [id_cpt, root.val, root]
    id_cpt += 1

    # init tree
    for motif in list_des_motif:

        list_pref = (get_pref([motif]))  # init the mini list of pref

        node_existe_id = None  # holde the id of mode if it aleady existe
        node_existe = False  # useed to check if we are in state where the noude alrady existe

        for elem_pref in list_pref:
            if elem_pref != '':
                # check if our elem(pref) of the mini pref list exsite in the main list
                if pref_found(elem_pref, main_list_des_pref) == True:
                    # getting exsistiing node id
                    for dic_el in aho_dict.values():
                        if dic_el[1] == elem_pref and dic_el[2].val == elem_pref:
                            node_existe_id = dic_el[0]
                            node_existe = True

                else:
                    # if the elem is not in the main list it means we ethier create a new one
                    # or we have the last know state
                    if node_existe == True:
                        # laste know state for him
                        new_nod = noud(id_cpt, elem_pref,
                                       elem_pref[-1], node_existe_id)
                        aho_dict[id_cpt] = [id_cpt, new_nod.val, new_nod]

                        id_cpt += 1
                        node_existe_id = None
                        node_existe = False
                    else:
                        # creation and getting the parent id
                        new_nod = noud(
                            id_cpt, elem_pref, elem_pref[-1], fun_find_parent_id(elem_pref, aho_dict))
                        aho_dict[id_cpt] = [id_cpt, new_nod.val, new_nod]
                        id_cpt += 1

        # we add our last itration pref to the main list
        main_list_des_pref.extend(list_pref)
        main_list_des_pref = list(set(main_list_des_pref))  # remove duplicqute

    # initing go to
    for elm in aho_dict.keys():
        dict_of_go_to = None
        for elem in aho_dict.keys():
            # we look for nth parent id where it existe in our automate and save it
            # and the cost to get there in the go to list
            if elm == aho_dict[elem][2].parent:
                if dict_of_go_to == None:
                    dict_of_go_to = {}
                dict_of_go_to[aho_dict[elem][2].cost] = aho_dict[elem][2].id

        aho_dict[elm][2].go_to = dict_of_go_to

    # init faile link
    aho_dict = fun_set_failer_list(aho_dict, main_list_des_pref)

    # init stop noude
    aho_dict = set_sortie(list_des_motif, aho_dict)

    return aho_dict


def aho_parcour(text, list_des_motif):
    result = dict()  # returns a dict with keywords and list of its occurrences
    current_state = 0
    automate = init_aho_autom(list_des_motif)

    for i in range(len(text)):
        # as long as we can't move we take the fail route
        while (go_next(automate, text[i], current_state)) is None and current_state != 0:
            # take fail route
            current_state = automate[current_state][2].failur_go_to[0]

        # if we are here that means we have a pssible move is that case we move to that state
        current_state = go_next(automate, text[i], current_state)

        if current_state is None:
            # current_state = automate[current_state][2].failur_go_to[0]
            current_state = 0
        else:
            for key in automate[current_state][2].output:
                if not (key in result):
                    result[key] = []
                result[key].append(i - len(key) + 1)

    return result

def grphe(ahom):

    # graph type
    G = nx.DiGraph()
    # extening the plot surface
    plt.figure(figsize=(10, 5))

    # init color
    end = 'red'
    root = 'green'
    normale = 'blue'

    lables = {}

    List_of_noud = []
    color_map = []

    # noude+color
    # append every noud id and the appropriate color to a list that is going to be used to create the graphe
    for elem in ahom.keys():

        List_of_noud.append(elem)

        if elem == 0:
            color_map.append(root)
        elif ahom[elem][2].is_final == True:
            color_map.append(end)
        else:
            color_map.append(normale)

    # arc or edges for routes
    for elem in ahom.values():
        if elem[2].parent != None:
            G.add_edge(elem[2].parent, elem[2].id, color='r')
            # list_of_edge.append((elem[2].parent, elem[2].id))

    # arc or edges for failur
    for elem in ahom.values():
        if len(elem[2].failur_go_to) != 0:
            G.add_edge(elem[2].id, elem[2].failur_go_to[0], color='Blue')
            # list_of_edge.append((elem[2].parent, elem[2].id))

    # lables
    # this shape {(started noud id , target noud if): text to be displayed ak 3ark fik tatktb ani 3ayn}
    for elem in ahom.values():
        if elem[2].go_to != None:
            for go_to in elem[2].go_to.keys():
                lables[(elem[2].id, elem[2].go_to[go_to])] = go_to

    # adding noud
    G.add_nodes_from(List_of_noud)

    # getting the color for edges and puting them into  a list
    colors = nx.get_edge_attributes(G, 'color').values()

    # idk they used this layout and it worked best
    pos = nx.kamada_kawai_layout(G)

    # data    #do u want noud lables?    #color fou edges
    nx.draw_networkx(G, pos, with_labels=True, edge_color=colors,
                     connectionstyle="arc3,rad=0.1")
    # this for the curved arc

    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=lables, font_size=15)  # to add arc lables
    # to change noud color
    nx.draw_networkx_nodes(G, pos, node_color=color_map)
    # just to chnage noud lables color
    nx.draw_networkx_labels(G, pos, font_color='#FFFFFF')
    # plt.show()
    plt.savefig(f'{"".join(random.sample(string.ascii_lowercase, 8))}.png', bbox_inches='tight')

