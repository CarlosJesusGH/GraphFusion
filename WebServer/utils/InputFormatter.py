__author__ = 'carlos garcia-hernandez'

import networkx as nx
import numpy as np
import unicodedata

# Tools to format the data and check for formatting errors in the networks before they are used to perform any calculations.

def check_input_format(input_data, input_task_or_type, preferred_format='', verbose=False):
  """
  Checks the input for formatting errors.
  :param network_task_or_type: The type of network (e.g. 'undirected', 'directed', 'probabilistic', 'hyper', 'simplicial_complex').
  :param network: The network to be checked.
  :param preferred_format: The preferred format for the network (e.g. 'edgelist', 'adjmatrix', 'adjlist').  # ref: https://medium.com/basecs/from-theory-to-practice-representing-graphs-cfd782c5be38
  :return: True if the network is correctly formatted, False otherwise.
  """
  if verbose: print("check_input_format - input_task_or_type:", input_task_or_type, ", preferred_format:", preferred_format)
  if input_task_or_type == 'undirected' or input_task_or_type == 'directed' or input_task_or_type == 'visualization':
    return check_undirected_network_format(input_data, preferred_format, verbose)
  elif input_task_or_type == 'factor':
    return check_factor_format(input_data, verbose)
  elif input_task_or_type == 'entitylist' or input_task_or_type == 'entityanno':
    return check_entityfile_format(input_data, input_task_or_type, verbose)
  elif input_task_or_type == 'probabilistic':
      return check_probabilistic_network_format(input_data, preferred_format, verbose)
  elif input_task_or_type == 'simplicial_complex':
      return check_simplicial_complex_format(input_data, preferred_format, verbose)
  elif input_task_or_type == 'hyper':
      return check_hyper_network_format(input_data, preferred_format, verbose)
  else:
    return False, None
    
def check_undirected_network_format(network, preferred_format, verbose=False):
  """
  Checks the undirected network for formatting errors.
  :param network: The undirected network to be checked.
  :param preferred_format: The preferred format for the network (e.g. 'edgelist', 'adjmatrix', 'adjlist').
  :param verbose: Whether to print debugging information.
  :return: True if the network is correctly formatted, False otherwise.
  """
  parsed_network = None
  # Check if the network can be parsed as an edgelist
  try:
    G = nx.parse_edgelist(network.split("\n"))
    if verbose: print("G", G, "G.nodes()", G.nodes())
    # if G is None or empty, return False
    if G is None or not G.nodes():
      if verbose: print("G is None or empty", G, "G.nodes()", G.nodes())
      raise Exception("G is None or empty")
    elif preferred_format == 'adjmatrix':
      if verbose: print("preferred_format", preferred_format)
      # Get the adjacency matrix from the network. Use Python 2.7
      adjmatrix = nx.to_numpy_matrix(G).tolist()
      if verbose: print("adjmatrix", adjmatrix)
      # Write adjmatrix to a string with delimiter="\t"
      parsed_network = unicode("\n".join(["\t".join(map(str, row)) for row in adjmatrix]), "utf-8")
      if verbose: print("parsed_network as adjmatrix", parsed_network)
    elif preferred_format == 'edgelist':
      if verbose: print("preferred_format", preferred_format)
      parsed_network = unicode("\n".join([" ".join(map(str, edge)) for edge in nx.to_edgelist(G)]), "utf-8")
  except:  
    #  Check if the network can be parsed as an adjacency matrix
    try:
      # G = nx.parse_adjlist(network.split("\n"))
      # Numpy load from text
      # Check if the file is tab-delimited or space-delimited or comma-delimited
      if "\t" in network:
        delimiter = "\t"
      elif " " in network:
        delimiter = " "
      elif "," in network:
        delimiter = ","
      else:
        delimiter = None
      if verbose: print("delimiter", delimiter)
      if delimiter:
        X = np.loadtxt(network.split("\n"), delimiter=delimiter, skiprows=0)
      else:
        X = np.loadtxt(network.split("\n"), skiprows=0)
      G = nx.from_numpy_matrix(X)
      # if G is None or empty, return False
      if G is None or not G.nodes():
        return False, None
      elif preferred_format == 'edgelist':
        if verbose: print("preferred_format", preferred_format)
        parsed_network = unicode("\n".join([" ".join(map(str, edge)) for edge in nx.to_edgelist(G)]), "utf-8")
      elif preferred_format == 'adjmatrix':
        if verbose: print("preferred_format", preferred_format)
        # Get the adjacency matrix from the network. Use Python 2.7
        adjmatrix = nx.to_numpy_matrix(G).tolist()
        if verbose: print("adjmatrix", adjmatrix)
        # Write adjmatrix to a string with delimiter="\t"
        parsed_network = unicode("\n".join(["\t".join(map(str, row)) for row in adjmatrix]), "utf-8")
        if verbose: print("parsed_network as adjmatrix", parsed_network)
    except Exception as e:
      if verbose: print("Exception", e, "e.message", e.message)
      return False, None
  # Otherwise, the network is correctly formatted
  return True, parsed_network

def check_probabilistic_network_format(network, preferred_format, verbose=False):
  """
  Checks the probabilistic network for formatting errors.
  :param network: The probabilistic network to be checked.
  :param preferred_format: The preferred format for the network (e.g. 'edgelist', 'adjmatrix', 'adjlist').
  :param verbose: Whether to print debugging information.
  :return: True if the network is correctly formatted, False otherwise.
  """
  parsed_network = None
  # Check if the network can be parsed as a weighted edgelist
  try:
    G = nx.parse_edgelist(network.split("\n"), nodetype=str, data=(('weight',float),))
    if verbose: print("G", G, "G.nodes()", G.nodes())
    if verbose: print("G.edges(data=True)", G.edges(data=True))
    # if G is None or empty, return False
    if G is None or not G.nodes():
      if verbose: print("G is None or empty", G, "G.nodes()", G.nodes())
      raise Exception("G is None or empty")
    elif preferred_format == 'adjmatrix':
      if verbose: print("preferred_format", preferred_format)
      # Get the adjacency matrix from the network. Use Python 2.7
      adjmatrix = nx.to_numpy_matrix(G).tolist()
      if verbose: print("adjmatrix", adjmatrix)
      # Write adjmatrix to a string with delimiter="\t
      parsed_network = unicode("\n".join(["\t".join(map(str, row)) for row in adjmatrix]), "utf-8")
      if verbose: print("parsed_network as adjmatrix", parsed_network)
    elif preferred_format == 'edgelist':
      if verbose: print("preferred_format", preferred_format)
      # Write edgelist to a string with delimiter=" ", the third element is the weight value only, not the dictionary
      # parsed_network = unicode("\n".join([" ".join(map(str, edge)) for edge in nx.to_edgelist(G)]), "utf-8")
      parsed_network = unicode("\n".join([" ".join(map(str, [edge[0], edge[1], edge[2]['weight'] if 'weight' in edge[2] else 1.0])) for edge in nx.to_edgelist(G)]), "utf-8")
    else:
      if verbose: print("preferred_format not valid: ", preferred_format)
      raise Exception("preferred_format value is not valid")
      
  except Exception as e:
    if verbose: print("Exception", e, "e.message", e.message)
    #  Check if the network can be parsed as a weighted adjacency matrix
    try:
      # G = nx.parse_adjlist(network.split("\n"))
      # Numpy load from text
      # Check if the file is tab-delimited or space-delimited or comma-delimited
      if "\t" in network:
        delimiter = "\t"
      elif " " in network:
        delimiter = " "
      elif "," in network:
        delimiter = ","
      else:
        delimiter = None
      if verbose: print("delimiter", delimiter)
      if delimiter:
        X = np.loadtxt(network.split("\n"), delimiter=delimiter, skiprows=0)
      else:
        X = np.loadtxt(network.split("\n"), skiprows=0)
      if verbose: print("X", X)
      G = nx.from_numpy_matrix(X)
      if verbose: print("G", G, "G.nodes()", G.nodes())
      if verbose: print("G.edges(data=True)", G.edges(data=True))
      # if G is None or empty, return False
      if G is None or not G.nodes():
        return False, None
      elif preferred_format == 'edgelist':
        if verbose: print("preferred_format", preferred_format)
        parsed_network = unicode("\n".join([" ".join(map(str, [edge[0], edge[1], edge[2]['weight'] if 'weight' in edge[2] else 1.0])) for edge in nx.to_edgelist(G)]), "utf-8")
      elif preferred_format == 'adjmatrix':
        if verbose: print("preferred_format", preferred_format)
        # Get the adjacency matrix from the network. Use Python 2.7
        adjmatrix = nx.to_numpy_matrix(G).tolist()
        if verbose: print("adjmatrix", adjmatrix)
        # Write adjmatrix to a string with delimiter="\t"
        parsed_network = unicode("\n".join(["\t".join(map(str, row)) for row in adjmatrix]), "utf-8")
        if verbose: print("parsed_network as adjmatrix", parsed_network)
      else:
        if verbose: print("preferred_format not valid: ", preferred_format)
        raise Exception("preferred_format value is not valid")
    except Exception as e:
      if verbose: print("Exception", e, "e.message", e.message)
      return False, None
  # Otherwise, the network is correctly formatted
  if verbose: print("the network is correctly formatted - parsed_network", parsed_network)
  return True, parsed_network

def check_simplicial_complex_format(network, preferred_format, verbose=False):
  """
  Checks the simplicial complex for formatting errors. A simplicial complex is a network where each node is a set of nodes representing a facet. This facet is represented as a string of nodes separated by a space, tab or comma.
  :param network: The simplicial complex network to be checked.
  :param verbose: Whether to print debugging information.
  :return: True if the network is correctly formatted, False otherwise.
  """
  # Check if the file can be read as a list of facets
  try:
    # Check if the file is tab-delimited or space-delimited or comma-delimited
    if "\t" in network:
      delimiter = "\t"
    elif " " in network:
      delimiter = " "
    elif "," in network:
      delimiter = ","
    else:
      delimiter = None
    if verbose: print("delimiter", delimiter)
    if delimiter:
      facets = [facet.split(delimiter) for facet in network.split("\n")]
    else:
      facets = [facet.split() for facet in network.split("\n")]
    if verbose: print("len(facets)", len(facets))
    if verbose: print("facets[:10]", facets[:10])
    # if facets is None or empty, return False
    if facets is None or not facets:
      return False, "The input file is empty."
    # elif facets has empty sets, return False
    elif any(not facet for facet in facets):
      return False, "There are empty sets in the input file."
    else:
      # Write facets to a string with delimiter="\n" and preffered_format as separator between nodes
      if not preferred_format:
        preferred_format = " "
      parsed_network = unicode("\n".join([preferred_format.join(map(str, facet)) for facet in facets]), "utf-8")
      if verbose: print("parsed_network[:10] as facets", parsed_network.split("\n")[:10])
  except Exception as e:
    if verbose: print("Exception", e, "e.args", e.args)
    return False, None
  # Otherwise, the network is correctly formatted
  return True, parsed_network

def check_hyper_network_format(network, preferred_format, verbose=False):
  """
  Checks the hyper network for formatting errors. A hyper network is a network where edges can connect more than two nodes. This hyper edge is represented as a string of nodes separated by a space, tab or comma.
  :param network: The hyper network to be checked.
  :param verbose: Whether to print debugging information.
  :return: True if the network is correctly formatted, False otherwise.
  """
  # Since the hyper network input file format is the same as for the simplicial complex, we can use the same function
  check_response, parsed_network = check_simplicial_complex_format(network, preferred_format, verbose)
  if check_response:
    # Verify that the first element of each edge is not repeated
    edges = [edge.split(preferred_format) for edge in parsed_network.split("\n")]
    if len(edges) != len(set([edge[0] for edge in edges])):
      return False, "The first column of the input file contains duplicates."
    # Verify that each edge has at least two nodes, excluding the first column. Consider that the last line of the file may be empty
    if any(len(edge) < 3 for edge in edges[:-1]):
      print("The index of the edges with less than two nodes is:", [i for i, edge in enumerate(edges) if len(edge) < 3])
      return False, "There are edges with less than two nodes."
  return check_response, parsed_network
  
# ----------------------------------------
# Other file types different from networks
# ----------------------------------------

def check_factor_format(factor, verbose=False):
  """
  Checks a factor for formatting errors. A factor matrix is similar to a weighted adjacency matrix, but it does not have to be symmetric.
  :param factor: The factor network to be checked.
  :param verbose: Whether to print debugging information.
  :return: True if the factor is correctly formatted, False otherwise.
  """
  parsed_input = None
  try:
    # Check if the file is tab-delimited or space-delimited or comma-delimited
    if "\t" in factor:
      delimiter = "\t"
    elif " " in factor:
      delimiter = " "
    elif "," in factor:
      delimiter = ","
    else:
      delimiter = None
    if verbose: print("delimiter", delimiter)
    if delimiter:
      X = np.loadtxt(factor.split("\n"), delimiter=delimiter, skiprows=0)
    else:
      X = np.loadtxt(factor.split("\n"), skiprows=0)
    # if X is None or empty, return False
    if X is None or not X.any():
      return False, None
    else:
      # Write X to a string with delimiter="\t"
      parsed_input = unicode("\n".join(["\t".join(map(str, row)) for row in X]), "utf-8")
      if verbose: print("parsed_input as factor", parsed_input)
  except Exception as e:
    if verbose: print("Exception", e, "e.args", e.args)
    return False, None
  # Otherwise, the network is correctly formatted
  return True, parsed_input

def check_entityfile_format(entity_file, input_task_or_type, verbose=False):
  file_content = unicodedata.normalize('NFKD', unicode(entity_file.read(), "utf-8")).encode('ascii', 'ignore')
  if verbose: print("input_task_or_type", input_task_or_type); print("file_content - start:\n", file_content)
  if input_task_or_type == 'entitylist':
    # Check if the file is a one-column file
    print("len(file_content.split('\n')[0].split('\t')) == 1:", len(file_content.split('\n')[0].split('\t')) == 1)
    if len(file_content.split('\n')[0].split('\t')) == 1:
      # Parse the file as a list of entities as a list of strings
      file_content = file_content.split("\n")
      # Get only unique values in the list
      # file_content = list(set(file_content))
      # Check if exists duplicates
      if len(file_content) != len(set(file_content)):
        if verbose: print("The file contains duplicates")
        return False, "The file contains duplicates"
      # Remove empty strings
      file_content = filter(None, file_content)
      # Parse back to a one-column file
      file_content = "\n".join(file_content)
      if verbose: print("file_content - end:\n", file_content)
      return True, file_content
    else:
      if verbose: print("The file is not a one-column file")
      return False, "The file is not a one-column file"
  elif input_task_or_type == 'entityanno':
    # Check if the file is a two-column file
    if len(file_content.split('\n')[0].split('\t')) == 2:
      # Parse the file as a list of entities as a list of strings
      file_content = file_content.split("\n")
      # Get only unique values in the list
      # file_content = list(set(file_content))
      # Check if exists duplicates
      if len(file_content) != len(set(file_content)):
        if verbose: print("The file contains duplicates")
        return False, "The file contains duplicates"
      # Remove empty strings
      file_content = filter(None, file_content)
      # Parse back to a two-column file
      file_content = "\n".join(file_content)
      if verbose: print("file_content - end:\n", file_content)
      return True, file_content
    else:
      if verbose: print("The file is not a two-column file")
      return False, "The file is not a two-column file"
  return True, file_content