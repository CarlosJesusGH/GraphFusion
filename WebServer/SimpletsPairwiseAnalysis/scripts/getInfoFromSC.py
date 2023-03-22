"""
Description:
------------
script to compute the number of nodes, number of edges and 1d-density of a simplicial complex

Run as:
-------
from scripts.GetInfoFromSC import get_values_from_sc
get_values_from_sc(path2sc=None, list_of_lines=None)

Parameters
----------
path2sc: string
  path to simplicial complex file
list_of_lines: list ([line1, line2, ..., lineN])
  list containing lines from simplicial complex file

Returns
-------
n_nodes: int
  number of nodes
n_edges: int
  number of edges
density: float
  1d-density
"""

import itertools

# Load the facets of a simplicial complex (pointed by path)
def read_sc_from_path(path):
  data = []
  ifile = open(path, 'r')
  for line in ifile.readlines():
    lspt = line.strip().split()
    if len(lspt)>= 2:
      edge = set(lspt)
      data.append(edge)
  ifile.close()
  return data

# Load the facets of a simplicial complex (pointed by list of lines)
def read_sc_from_list(list_of_lines):
  data = []
  for line in list_of_lines:
    lspt = line.strip().split()
    if len(lspt)>= 2:
      edge = set(lspt)
      data.append(edge)
  return data

def get_values_from_sc(path2sc=None, list_of_lines=None):
  print("computing n_nodes, n_edges, density")
  # read all lines from sc, either from file or from string
  if path2sc:
    sc = read_sc_from_path(path2sc)
  elif list_of_lines:
    sc = read_sc_from_list(list_of_lines)
  # count nodes and edges
  nodes = set()
  for s in sc:
    nodes.update(s)
  edges = set()
  for s in sc:
    for pair in itertools.combinations(s, 2):
      pair = tuple(sorted(pair))
      edges.update([pair])
    nodes.update(s)
  # compute density
  n_nodes = len(nodes)
  n_edges = len(edges)
  # max_edges = (n_nodes * (n_nodes - 1)) / 2
  # density = n_edges / max_edges
  density = (2.0 * n_edges) / (n_nodes * (n_nodes - 1))  # from: https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.density.html
  print("n_nodes, n_edges, density", n_nodes, n_edges, density)
  return n_nodes, n_edges, density