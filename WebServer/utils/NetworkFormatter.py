__author__ = 'carlos garcia-hernandez'

import networkx as nx
import numpy as np

# Tools to format the data and check for formatting errors in the networks before they are used to perform any calculations.

def check_network_format(network, network_task_or_type, preferred_format):
  """
  Checks the network for formatting errors.
  :param network_task_or_type: The type of network (e.g. 'undirected', 'directed', 'probabilistic', 'hyper', 'simplicial_complex').
  :param network: The network to be checked.
  :param preferred_format: The preferred format for the network (e.g. 'edgelist', 'adjmatrix', 'adjlist').  # ref: https://medium.com/basecs/from-theory-to-practice-representing-graphs-cfd782c5be38
  :return: True if the network is correctly formatted, False otherwise.
  """
  if network_task_or_type == 'undirected':
    return check_undirected_network_format(network, preferred_format)
  # elif network_task_or_type == 'directed':
  #     return check_directed_network_format(network)
  # elif network_task_or_type == 'probabilistic':
  #     return check_probabilistic_network_format(network)
  # elif network_task_or_type == 'hyper':
  #     return check_hyper_network_format(network)
  # elif network_task_or_type == 'simplicial_complex':
  #     return check_simplicial_complex_network_format(network)
  if network_task_or_type == 'visualization':
    return check_undirected_network_format(network, preferred_format) 
  # TODO: add the line below when the other network types are implemented
  # or check_directed_network_format(network) or check_probabilistic_network_format(network)
  else:
    return False
    
def check_undirected_network_format(network, preferred_format):
  """
  Checks the undirected network for formatting errors.
  :param network: The undirected network to be checked.
  :return: True if the network is correctly formatted, False otherwise.
  """
  parsed_network = None
  # Check if the network can be parsed as an edgelist
  try:
    G = nx.parse_edgelist(network.split("\n"))
    # if G is None or empty, return False
    if G is None or not G.nodes():
      # print("G is None or empty", G, "G.nodes()", G.nodes())
      raise Exception("G is None or empty")
    elif preferred_format == 'adjmatrix':
      adjmatrix = nx.to_numpy_array(G)
      # Write graph to a string with delimiter="\t"
      parsed_network = "\n".join(["\t".join(map(str, row)) for row in adjmatrix])
      print("parsed_network as adjmatrix", parsed_network)
    elif preferred_format == 'edgelist':
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
      # print("delimiter", delimiter)
      if delimiter:
        X = np.loadtxt(network.split("\n"), delimiter=delimiter, skiprows=0)
      else:
        X = np.loadtxt(network.split("\n"), skiprows=0)
      G = nx.from_numpy_matrix(X)
      # if G is None or empty, return False
      if G is None or not G.nodes():
        return False, None
      elif preferred_format == 'edgelist':
        parsed_network = unicode("\n".join([" ".join(map(str, edge)) for edge in nx.to_edgelist(G)]), "utf-8")
    except Exception as e:
      print("Exception", e, "e.message", e.message)
      return False, None
  # Otherwise, the network is correctly formatted
  return True, parsed_network