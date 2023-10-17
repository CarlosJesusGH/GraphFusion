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
  if input_task_or_type == 'undirected' or input_task_or_type == 'directed' or input_task_or_type == 'visualization':
    return check_undirected_network_format(input_data, preferred_format, verbose)
  elif input_task_or_type == 'factor':
    return check_factor_format(input_data, verbose)
  elif input_task_or_type == 'entitylist' or input_task_or_type == 'entityanno':
    return check_entityfile_format(input_data, input_task_or_type, verbose)
  # elif network_task_or_type == 'probabilistic':
  #     return check_probabilistic_network_format(network)
  # elif network_task_or_type == 'hyper':
  #     return check_hyper_network_format(network)
  # elif network_task_or_type == 'simplicial_complex':
  #     return check_simplicial_complex_network_format(network)
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

def check_factor_format(factor, verbose=False):
  """
  Checks a factor network for formatting errors. A factor matrix is similar to a weighted adjacency matrix, but it does not have to be symmetric.
  :param factor: The factor network to be checked.
  :param verbose: Whether to print debugging information.
  :return: True if the network is correctly formatted, False otherwise.
  """
  # First try to parse the network as a undirected network
  # try:
  #   response = check_undirected_network_format(input, preferred_format='adjmatrix', verbose=verbose)
  #   if not response[0]:
  #     raise Exception("Factor could not be loaded as adjacency matrix")
  #   return response
  # except Exception as e:
  #   if verbose: print("Exception", e, "e.args", e.args)
  if True:
    # If that fails, try to parse the network as a numpy matrix
    parsed_network = None
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
        parsed_network = unicode("\n".join(["\t".join(map(str, row)) for row in X]), "utf-8")
        if verbose: print("parsed_network as factor", parsed_network)
    except Exception as e:
      if verbose: print("Exception", e, "e.args", e.args)
      return False, None
    # Otherwise, the network is correctly formatted
    return True, parsed_network

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
      file_content = list(set(file_content))
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
      file_content = list(set(file_content))
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