import sys
import operator
import networkx as nx
import collections
import logging
import re
import sys

exp_go_terms = ["EXP", "IDA", "IPI", "IMP", "IGI", "IEP"]


# logger = logging.getLogger("read_go_terms")
logger = logging.getLogger('go_term_util')


def build_altid2id_mapping(obo_filepath=None, go_termdict=None):
    """ Constructs a mapping from GO term alternate IDs to canonical/unique IDs

    Exactly one of 'obo_filepath' and 'go_termdict' should be specified. The
    former is used to read the GO term information directly from a file; the
    latter reuses information that was already read from a file (to avoid
    duplicating the file processing when calling more than one function that
    uses this information).
    """
    if (obo_filepath is not None) == (go_termdict is not None):
        raise ValueError("exactly one of obo_filepath or go_termdict should be given")
    if obo_filepath is not None:
        logger.info("reading GO ID and alt-ID info from {0}".format(obo_filepath))
        term_info = read_go_terms.read_go_terms(obo_filepath)
    else:
        term_info = go_termdict
      
    alt_id_to_main_id = dict()
    for term in term_info:
        cur_id = term.get('id', [])
        if len(cur_id) == 0:
            errmsg = "no main ID for term: {0}".format(term)
            #logger.fatal(errmsg)
            sys.stderr.write(errmsg + "\n")
            sys.exit(1)
        elif len(cur_id) > 1:
            errmsg = "multiple main IDs for term: {0}".format(term)
            #logger.fatal(errmsg)
            sys.stderr.write(errmsg + "\n")
            sys.exit(1)
        cur_id = cur_id[0]
        alt_ids = term.get('alt_id', [])
        for alt_id in alt_ids:
            if alt_id in alt_id_to_main_id:
                errmsg = "alt_id {0} listed more than once in {1}".format(
                    alt_id, obo_filepath)
                #logger.fatal(errmsg)
                sys.stderr.write(errmsg + "\n")
                sys.exit(1)
            alt_id_to_main_id[alt_id] = cur_id
            
    return alt_id_to_main_id

def build_term2name_mapping(obo_filepath=None, go_termdict=None):
    """ Constructs a mapping from GO term IDs to names (descriptions)

    Exactly one of 'obo_filepath' and 'go_termdict' should be specified. The
    former is used to read the GO term information directly from a file; the
    latter reuses information that was already read from a file (to avoid
    duplicating the file processing when calling more than one function that
    uses this information).
    """

    if (obo_filepath is not None) == (go_termdict is not None):
        raise ValueError("exactly one of obo_filepath or go_termdict should be given")
    if obo_filepath is not None:
        terms = read_go_terms.read_go_terms(obo_filepath)
    else:
        terms = go_termdict
    
    id2name = dict()
    for term in terms:
        term_id = term['id']
        term_name = term['name']
        if (len(term_id) != 1) or (len(term_name) != 1):
            print "ERROR: term_id and term_name should be length-1 lists"
            print "bad GO-term dict was: {0}".format(repr(term))
            sys.exit()
        else:
            term_id = term_id[0]
            term_name = term_name[0]
        term_id = re.split('[\.:]', term_id)[-1] # "GO:#######" -> "#######"
        if term_id in id2name.keys():
            print "ERROR: GO ID {0} already mapped to {1} in {2}".format(
                term_id, id2name[term_id], obo_filepath)
            sys.exit()
        id2name[term_id] = term_name
    print "found {0} terms".format(len(terms))
    
    return id2name

def go_str_to_int(gostr):
    """ extracts the integer part of a GO-term string """
    go_int = [mtch for mtch in re.split('\D+', gostr) if mtch]
    if len(go_int) != 1:
        raise ValueError("unique digit sequence not found in GO-id: {0}\n".format(
            gostr))
    return long(go_int[0])
    
def change_term_keys_to_int(dct):
    """ changes the keys of a GO-string->item mapping from strings to integers
    """
    return dict([(go_str_to_int(key), val) for (key, val) in dct.iteritems()])

# NOTE: not reflexive (unless term_to_parents is)
def all_ancestors(query, term_to_parents):
    """ finds all ancestors of a term, given a term-to-parents mapping """
    visited = set()
    to_check = [go_str_to_int(parent) 
        for parent in term_to_parents[query]]
    while to_check:
        cur_anc = to_check.pop()
        visited.add(cur_anc)
        to_check.extend([go_str_to_int(anc) 
            for anc in term_to_parents[cur_anc] if anc not in visited])
    return visited

TermScore = collections.namedtuple('TermScore', ['term', 'score'])
def read_term_scores(in_filepath, match_num):
    """ reads GO-term scores from a CCA output file """
    match_header = 'match  {0}'.format(match_num)
    in_file = open(in_filepath, 'rt')
    cur_line = in_file.readline()
    while match_header not in cur_line and cur_line != '':
        cur_line = in_file.readline()
        
    if cur_line == '':
        sys.stderr.write("match {0} not found in {1}\n".format(
            match_num, in_filepath))
        sys.exit(1)

    cur_line = in_file.readline()
    while 'GO' not in cur_line and cur_line != '':
        cur_line = in_file.readline()
    
    if cur_line == '':
        sys.stderr.write(
            "could not find GO-term scores list for match {0} in {1}\n".format(
            match_num, in_filepath))
        sys.exit(1)
    
    term_scores = []
    while 'GO' in cur_line:
        elts = cur_line.split()
        if len(elts) != 2:
            sys.stderr.write('"{0}" not formatted as "GO_term xcor_val"')
        term = go_str_to_int(elts[0])
        score = float(elts[1])
        term_scores.append(TermScore(term, score))
        cur_line = in_file.readline()
        
    in_file.close()
        
    return term_scores

def read_parent_info(obo_filepath=None, go_termdict=None, relation_types=None):
    """ constructs a dict mapping GO terms to their parents

    Exactly one of 'obo_filepath' and 'go_termdict' should be specified. The
    former is used to read the GO term information directly from a file; the
    latter reuses information that was already read from a file (to avoid
    duplicating the file processing when calling more than one function that
    uses this information).
    By default, GO term parents are determined by "is_a" relationships.
    To allow other relationships to also imply parenthood, specify the
    relationship names as list items in relation_types
    (e.g., relation_types=["part_of"]).
    """
    if (obo_filepath is not None) == (go_termdict is not None):
        raise ValueError("exactly one of obo_filepath or go_termdict should be given")
    if obo_filepath is not None:
        terms = read_go_terms(obo_filepath)
    else:
        terms = go_termdict
        
#    idvals = [term.get('id', []) for term in terms] + [term.get('alt_id', []) for term in terms]
#    idvals = [item for sublist in idvals for item in sublist]
#    print "tmp_idvals:"
#    print [idval for idval in idvals if type(idval) != type('str')]
        
    term_to_parents = dict()
    for term in terms:
        cur_id = term.get('id', [])
        if len(cur_id) != 1:
            errmsg = (
                "GO-term did not have exactly one ID: {0}\n".format(
                cur_id))
            sys.stderr.write('ERROR: {0}\n'.format(errmsg))
            #logger.error(errmsg)
            term_info = "full term information: {0}".format(term)
            sys.stderr.write(term_info + '\n')
            #logger.info(term_info)
            sys.exit()
        cur_id = cur_id[0]
        alt_ids = [alt_id for alt_id in term.get('alt_id', [])]
        for term_id in [cur_id] + alt_ids:
            if term_id in term_to_parents:
                errmsg = (
                    "GO-term with ID {0} listed more than once\n".format(
                    str(term_id)))
                sys.stderr.write('ERROR: {0}\n'.format(errmsg))
                #logger.error(errmsg)
                sys.exit()
            cur_parents = term.get('is_a', [])
            if relation_types:
                relations = term.get('relationship', [])
                for relation in relations:
                    relation = relation.partition('!')[0] # remove comments
                    relation_toks = relation.split()
                    rel_type = relation_toks[0]
                    if rel_type in relation_types:
                        new_pts = [pt for pt in relation_toks[1:] 
                            if pt.startswith('GO')]
                        cur_parents.extend(new_pts)
            term_to_parents[term_id] = cur_parents
#    return change_term_keys_to_int(term_to_parents)
    return term_to_parents

def get_ancestor_mapping_from_parents(term_to_parents, is_reflexive):
    """ produces a term-to-ancestors mapping from a term-to-parents mapping

    is_reflexive indicates whether a term should be considered an ancestor of
    itself.
    """
    term_to_ancestors = dict()
    for term in term_to_parents.iterkeys():
        ancestors = all_ancestors(term, term_to_parents)
        if is_reflexive:
            ancestors.add(term)
        term_to_ancestors[term] = frozenset(ancestors)
    return term_to_ancestors
    
def get_descendant_mapping_from_ancestors(term_to_ancestors):
    """ produces a term->descendants mapping from a term->ancestors mapping """
    term_to_descendants = dict()
    for term, ancs in term_to_ancestors.iteritems():
        for anc in ancs:
            cur_desc = term_to_descendants.get(anc, set())
            cur_desc.add(term)
            term_to_descendants[anc] = cur_desc
    return term_to_descendants
    
def get_descendant_mapping_from_file(
        is_reflexive, obo_filepath=None, go_termdict=None):
    term_to_parents = read_parent_info(obo_filepath, go_termdict)
    term_to_ancestors = get_ancestor_mapping_from_parents(term_to_parents, 
        is_reflexive)
    term_to_descendants = get_descendant_mapping_from_ancestors(term_to_ancestors)
    return term_to_descendants


class FileFormatError(Exception):
    pass

def _read_next_go_term(go_file, cur_line):
    while not '[Term]' in cur_line:
        if cur_line == '':
            return ({}, '')
        cur_line = go_file.readline()
    term_dict = {}
    cur_line = go_file.readline()
    (tag, sep, value) = cur_line.partition(':')
    tag = tag.strip()
    while True:
        if ':' in sep:
            value = value.partition('!')[0].strip()
            cur_val = term_dict.get(tag.strip(), [])
            term_dict[tag] = cur_val + [value]
        elif '[Term]' in cur_line:
            return (term_dict, cur_line)
        elif re.search(r'\[.+\]', cur_line) is not None:
            return (term_dict, cur_line)
        elif cur_line == '': # end of file
            return ({}, '')
        elif cur_line.strip() == '':
            pass
        else:
            raise FileFormatError('non-tag/value, non-blank line encountered in [term] stanza')
        cur_line = go_file.readline()
        (tag, sep, value) = cur_line.partition(':')        
        tag = tag.strip()

def read_go_terms(filename):
    #logger.info("reading GO-terms from {0}".format(filename))
    go_file = open(filename, 'rt')
    go_terms = []
    more_terms = True
    cur_line = go_file.readline()
    while more_terms:
        (term_dict, cur_line) = _read_next_go_term(go_file, cur_line)
        if term_dict:
            go_terms.append(term_dict)
        else:
            more_terms = False
    return go_terms


# load entrez-ids from a PPI (in leda format)
def readPPI(fileName):
	network = nx.read_leda(fileName)
	vertices = network.nodes()
	vertex_set = set(vertices)
	return vertex_set



def GO_from_entrezid(entrez_ids, gene2gofile, gotype):
	ifile = open(gene2gofile, "r")
	dic = {}	
	ifile.readline()
	total_terms = 0
	for line in ifile.readlines():
		linesplit=line.strip().split('\t')
		if len(linesplit)>=2:
			taxon = linesplit[0]
			gene =  linesplit[1]
			go_id = linesplit[2]
			go_xp = linesplit[3]
			goterm = linesplit[5]
			typeg = linesplit[7]
			if gotype==typeg:
				if go_xp in exp_go_terms:
					if gene in entrez_ids:
						if gene not in dic:
							dic[gene]=[]
						dic[gene].append(go_id)
						total_terms +=1
	
	ifile.close()
	#ofile = open(fileName, "w")
	#for eid in entrez_ids:
	#	if eid in dic:
	#		for glist in dic[eid]:
	#			ofile.write("%s\t%s\t%s\n"%(eid, glist[0], glist[1]))
	#ofile.close()
	print len(dic), " annotated genes, with ", total_terms, "annotations"
	return dic

def getAllParents(parent_dic, goTerm):
	allParents = [goTerm]
	organisedParents = [[goTerm]]
	currentLevel = 0
	while True:
		organisedParents.append([])
		for element in organisedParents[currentLevel]:
			parent = parent_dic[element]
			for pr in parent:
				if pr not in allParents:
					organisedParents[-1].append(pr)
					allParents.append(pr)		
		currentLevel += 1
		if organisedParents[-1] == []:
			break
	return allParents

def extend_all(dic, parent_dic):
	extended_dic = {}
	total_ext = 0
	for key in dico:
		extended_dic[key] = set()
		for goterm in dic[key]:
			extended_dic[key].add(goterm)
			parents = getAllParents(parent_dic, goterm)
			for elem in parents:
				extended_dic[key].add(elem)
				total_ext += 1
	print "Total terms after extension: ", total_ext
	return extended_dic

"""
	Main code starts here
"""


# Read the publications and experiments types in the database for human-human interactions
PPI_File = sys.argv[1]
GENE2GO_File = sys.argv[2]
OBO_File = sys.argv[3]
annotationtype = sys.argv[4] # BP, MF or CC
OutputGO_File = sys.argv[5]

print "## Loading entrez-ids from PPI file\n"

entrez_list = readPPI(PPI_File)


# Remove the ubiquitin protein as it distorts the topology


print "## Retrieving GO terms\n"
my_go_type = "Process" # =BP
if annotationtype == "MF":
	my_go_type = "Function"
elif annotationtype == "CC":
	my_go_type = "Component"

dico = GO_from_entrezid(entrez_list, GENE2GO_File, my_go_type)

print "## Reading Gene Ontology OBO\n"

goParentDict = read_parent_info(obo_filepath=OBO_File)

print "## Extending Annotations\n"

ext_dic = extend_all(dico, goParentDict)

ofile = open(OutputGO_File, "w")
for eid in entrez_list:
	if eid in ext_dic:
		for glist in ext_dic[eid]:
			ofile.write("%s\t%s\n"%(eid, glist))
ofile.close()


