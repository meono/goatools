__author__ = 'emre'

"""
Just putting some utility function available on scripts here
"""

def load_geneset(pop=None, pop_fn=None, study=None, study_fn=None, compare=False):
    '''
    A utility function to read file(s) to generate sets for population and/or study. It can also be used to prepare 2 sets of genes for comparison.
    :param pop: the set of IDs detected in the experiment (e.g. 'pop.txt'). Alternatively, set of IDs to be used for comparison.
    :param pop_fn: File name/path for the set of IDs detected in the experiment (e.g. 'pop.txt'). Alternatively, set of IDs to be used for comparison.
    :param study: A set of genes/identifiers to be used for enrichment study
    :param study_fn: File name/path for the set of IDs to be studied (e.g. 'study.txt')
    :param compare: True or False depending on whether pop_fn is for population set or a comparison set.
    :return: two sets containing IDs for study and population
    '''
    if (study == None) and (study_fn) == None and (compare == True):
        raise ValueError('Either a set or a file name containing genes to be studied is required for comparison of two studies.')

    if (pop == None) and (pop_fn == None):
        raise ValueError('Either a set or a file name containing population of genes (or study to be compared) is required.')

    if pop_fn:
        pop = set(_.strip() for _ in open(pop_fn) if _.strip())

    if study_fn:
        study = frozenset(_.strip() for _ in open(study_fn) if _.strip())


    # some times the pop is a second group to compare, rather than the
    # population in that case, we need to make sure the overlapping terms
    # are removed first
    if compare:
        common = pop & study
        pop |= study
        pop -= common
        study -= common
        print("removed %d overlapping items" % (len(common)))
        # print("Set 1: {0}, Set 2: {1}".\
        #     format(len(study), len(pop)))
        return study, pop
    else:
        return pop

def read_associations(assoc_fn):
    """
    :param assoc_fn: File name/path for the gene/uniprot ID to GO association (e.g. 'ecogeneGOassociation.txt')
    :return: a dictionary with the association info.
    """
    assoc = {}
    for row in open(assoc_fn):
        atoms = row.split()
        if len(atoms) == 2:
            a, b = atoms
        elif len(atoms) > 2 and row.count('\t') == 1:
            a, b = row.split("\t")
        else:
            continue
        b = set(b.split(";"))
        assoc[a] = b

    return assoc