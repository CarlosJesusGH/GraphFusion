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
    if verbose: print("G", G, "G.nodes()[:10]", G.nodes()[:10])
    # if G is None or empty, return False
    if G is None or not G.nodes():
      if verbose: print("G is None or empty", G, "G.nodes()", G.nodes())
      raise Exception("G is None or empty")
    elif preferred_format == 'adjmatrix':
      if verbose: print("preferred_format", preferred_format)
      # Get the adjacency matrix from the network. Use Python 2.7
      adjmatrix = nx.to_numpy_matrix(G).tolist()
      if verbose: print("adjmatrix[:10]", adjmatrix[:10])
      # Write adjmatrix to a string with delimiter="\t"
      parsed_network = unicode("\n".join(["\t".join(map(str, row)) for row in adjmatrix]), "utf-8")
      if verbose: print("parsed_network as adjmatrix[:10]", parsed_network[:10])
    elif preferred_format == 'edgelist':
      if verbose: print("preferred_format", preferred_format)
      # Print the edgelist without the dictionary
      if verbose: print("G.edges(data=False)[:10]", G.edges(data=False)[:10])
      # parsed_network = unicode("\n".join([" ".join(map(str, edge)) for edge in nx.to_edgelist(G)]), "utf-8")
      parsed_network = unicode("\n".join([" ".join(map(str, edge)) for edge in G.edges(data=False)]), "utf-8")
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
  if verbose: print("parsed_network[:10] as lines:", parsed_network.split("\n")[:10])
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

def check_column_list_format(input_data, num_of_columns, col_id_numerical=[], parsed_delimiter="\t", add_headers=False, verbose=False):
  """
  Checks the input for formatting errors. The input file will usually be tab-delimited or space-delimited or comma-delimited. The input file will commonly have one or more columns. Some columns might be textual (e.g. gene names), while others might be numerical (e.g. gene expression values).
  :param input_data: The input data to be checked.
  :param num_of_columns: The number of columns in the input data.
  :param col_id_numerical: The list of column ids that must be numerical.
  :param verbose: Whether to print debugging information.
  :return: True if the input data is correctly formatted, False otherwise.
  """
  # Check if the file is tab-delimited or space-delimited or comma-delimited
  if "\t" in input_data:
    delimiter = "\t"
  elif " " in input_data:
    delimiter = " "
  elif "," in input_data:
    delimiter = ","
  else:
    delimiter = None
  if verbose: print("delimiter", delimiter)
  if delimiter:
    lines = [line.split(delimiter) for line in input_data.split("\n")]
  else:
    lines = [line.split() for line in input_data.split("\n")]
  if verbose: print("len(lines)", len(lines))
  if verbose: print("lines[:10]", lines[:10])
  # if lines is None or empty, return False
  if lines is None or not lines:
    return False, "The input file is empty."
  # elif lines has empty sets, return False
  elif any(not line for line in lines):
    return False, "There are empty sets in the input file."
  # elif lines has a different number of columns than num_of_columns columns, return False. Ignore the last line in case it is empty.
  elif any(len(line) != num_of_columns for line in lines[:-1]):
    # Print the index of the lines with a different number of columns than num_of_columns
    if verbose: print("The index of the lines with a different number of columns than " + str(num_of_columns) + " is:", [i for i, line in enumerate(lines[:-1]) if len(line) != num_of_columns])
    return False, "There are lines with a different number of columns than " + str(num_of_columns) + "."
  # elif lines has a column with index in col_id_numerical that is not numerical, return False. Ignore the last line in case it is empty.
  elif any(not all(line[col_id].replace(".", "", 1).replace("-","",1).isdigit() for col_id in col_id_numerical) for line in lines[:-1]):
    # Print the index of the lines with a column with index in col_id_numerical that is not numerical
    if verbose: print("The index of the lines with a column with index in col_id_numerical that is not numerical is:", [i for i, line in enumerate(lines[:-1]) if not all(line[col_id].replace(".", "", 1).replace("-","",1).isdigit() for col_id in col_id_numerical)])
    return False, "There are lines with a column with index '" + str(col_id_numerical) + "' that is not numerical."
  # Otherwise, the input data is correctly formatted
  # Write lines to a string with delimiter="\n" and parsed_delimiter as separator between columns
  if not parsed_delimiter:
    parsed_delimiter = "\t"
  if add_headers:
    lines.insert(0, add_headers)
  parsed_input = unicode("\n".join([parsed_delimiter.join(map(str, line)) for line in lines]), "utf-8")
  if verbose: print("parsed_input[:10] as lines", parsed_input.split("\n")[:10])
  return True, parsed_input


def check_factor_format(factor, verbose=False):
  """
  Checks a factor for formatting errors. A factor matrix is similar to a weighted adjacency matrix, but it does not have to be symmetric.
  :param factor: The factor network to be checked.
  :param verbose: Whether to print debugging information.
  :return: True if the factor is correctly formatted, False otherwise.
  """
  # First, check if the input is a two-column edgelist file using the 'check_column_list_format' method, in that case, parse it as network and obtain the adjacency matrix as factor
  check_response, parsed_input = check_column_list_format(factor, num_of_columns=2, col_id_numerical=[], parsed_delimiter="\t", verbose=False)
  if check_response:
    # Parse the network as an adjacency matrix
    check_response, parsed_input = check_undirected_network_format(parsed_input, preferred_format='adjmatrix', verbose=False)
    if check_response:
      factor = parsed_input
      print("Input is a two-column edgelist file, parsed as network and obtained the adjacency matrix as factor")
  else:
    # Second, check if the input is a three-column weighted edgelist file using the 'check_column_list_format' method, in that case, parse it as probabilistic network and obtain the adjacency matrix as factor using the 'check_probabilistic_network_format' method
    check_response, parsed_input = check_column_list_format(factor, num_of_columns=3, col_id_numerical=[2], parsed_delimiter="\t", verbose=False)
    if check_response:
      # Parse the network as an adjacency matrix
      check_response, parsed_input = check_probabilistic_network_format(parsed_input, preferred_format='adjmatrix', verbose=False)
      if check_response:
        factor = parsed_input
        print("Input is a three-column weighted edgelist file, parsed as probabilistic network and obtained the adjacency matrix as factor")
  # Then, work with the factor matrix
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
      if verbose: print("parsed_input[:100]", parsed_input[:100])
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