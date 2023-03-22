//
//  Create the Clique complex from a binary network
//
//  Noel Malod-Dognin, January 2018
//  Based on Bron-Kerbosch maximal clique enumeration algorithm V2, using Tomita, Tanaka and Takahash pivot selection.
//

#include <iostream>
#include <set>
#include <vector>
#include <map>
#include <stack>
#include <tuple>
#include <algorithm>
#include <iterator>
#include <string>
#include <fstream>
#include <sstream>


using namespace std;


class Graph
{
public:
	
	int nb_nodes;
	int nb_edges;
	
	set<int> node_set;
	
	map< int, set<int> > adj_matrix;
	
	Graph()
	{
		nb_nodes = 0;
		nb_edges = 0;
		adj_matrix.clear();
		node_set.clear();
	};
	
	void add_edge(int u, int v){
		if(u != v){
			if(adj_matrix.find(u) == adj_matrix.end()){
				set<int> emptyset; 
				adj_matrix[u] = emptyset;
				node_set.insert(u);
			}
			if(adj_matrix.find(v) == adj_matrix.end()){
				set<int> emptyset; 
				adj_matrix[v] = emptyset;
				node_set.insert(v);
			}
			adj_matrix[u].insert(v);
			adj_matrix[v].insert(u);
			nb_nodes = node_set.size();
		}
	};
	
	set<int> & get_neighboors(int u){
		return adj_matrix[u];
	};
};


void BronKerbosch2(set<int> R, set<int> P, set<int> X, Graph & G, vector<set<int> > & cliques){
	if(P.size()==0 && X.size()==0){
		//maximal clique
		set<int> clique(R);
		cliques.push_back(clique);
	}
	else{
		//find pivot u in PX = (P union X) such that cardinality of PNU = (P inter Neigh(u)) is maximal.
		
		// computing P union X
		vector<int> PX;
		std::set_union(P.begin(), P.end(), X.begin(), X.end(), std::back_inserter(PX));
		
		unsigned int best_u=PX[0];
		unsigned int best_pnu=0;
	
		for(vector<int>::iterator vit(PX.begin()); vit!=PX.end(); ++vit){
			// computing P \ Neigh(u)
			int cur_u = *vit;
			vector<int> PNU;
			set<int> & neigh_u(G.get_neighboors(cur_u));
			std::set_difference(P.begin(), P.end(), neigh_u.begin(), neigh_u.end(), std::back_inserter(PNU));
			if(PNU.size() >= best_pnu){
				best_u = cur_u;
				best_pnu = PNU.size();
			}
		}
		
		vector<int> PNU;
		set<int> & neigh_u(G.get_neighboors(best_u));
		std::set_difference(P.begin(), P.end(), neigh_u.begin(), neigh_u.end(), std::back_inserter(PNU));
		
		
		for(vector<int>::iterator vit(PNU.begin()); vit!=PNU.end(); ++vit){
			int v = *vit;
			set<int> & neigh_v(G.get_neighboors(v));
			
			P.erase(v);
			
			// RUV = (R union {v} ), PIN = (P inter neigh(v)), XIN = (X inter neigh(v))
			
			set<int> RUV(R);
			RUV.insert(v);
			
			vector<int> PIN_v;
			std::set_intersection(P.begin(), P.end(), neigh_v.begin(), neigh_v.end(), std::back_inserter(PIN_v));
			set<int> PIN(PIN_v.begin(), PIN_v.end());
			
			vector<int> XIN_v;
			std::set_intersection(X.begin(), X.end(), neigh_v.begin(), neigh_v.end(), std::back_inserter(XIN_v));
			set<int> XIN(XIN_v.begin(), XIN_v.end());
			
			//Main recursive call
			BronKerbosch2(RUV, PIN, XIN, G, cliques);
			
			//updates

			X.insert(v);
		}
	}
};

//BronKerbosch2(R,P,X):
//       if P and X are both empty:
//           report R as a maximal clique
//       choose a pivot vertex u in P ⋃ X
//       for each vertex v in P \ N(u):
//           BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
//           P := P \ {v}
//           X := X ⋃ {v}



void Read_EdgeList(string ifname, Graph & G, vector<string> & ind_to_node, map<string, int> & node_to_ind){
	
	string line;
	ifstream myfile (ifname.c_str());
	if (myfile.is_open()){
		while ( getline (myfile,line) ){
			istringstream iss(line);
			string node1, node2;
			
			iss >> node1 >> node2;
			if(node_to_ind.find(node1) == node_to_ind.end()){
				//insert node1
				node_to_ind[node1] = ind_to_node.size();
				ind_to_node.push_back(node1);
			}
			if(node_to_ind.find(node2) == node_to_ind.end()){
				//insert node1
				node_to_ind[node2] = ind_to_node.size();
				ind_to_node.push_back(node2);
			}
			
			int ind1, ind2;
			ind1 = node_to_ind[node1];
			ind2 = node_to_ind[node2];
			G.add_edge(ind1, ind2);
		}
		myfile.close();
		cout << "Network has " << G.nb_nodes << " nodes\n";
	}
	else cout << "Unable to open network file\n";
	return;
};

int main(int argc, char** argv)
{
	//Parse the command line
	if(argc != 3){
		cout << "Usage: Make_Clique_Complex <input network filename> <output filename>\n";
		exit(0);
	}
	
	string networkfname(argv[1]);
	string outputfname(argv[2]);
	
	//Load binary network from edgelist file
	Graph g = Graph();
	vector<string> ind_to_node;
	map<string, int> node_to_ind;
	
	Read_EdgeList(networkfname, g, ind_to_node, node_to_ind);
	
	
	//std::cout << g.are_adjacent(1, 3) << std::endl;
	//std::cout << g.are_adjacent(1, 4) << std::endl;
	
	cout << "Starting Maximal clique ennumeration:\n";
	
	set<int> R,P,X;
	R.clear();
	P.clear();
	X.clear();
	
	for(int i(0); i<ind_to_node.size(); ++i){
		P.insert(i);
	}
	
	vector< set<int >  > cliques;
	cliques.clear();
	
	BronKerbosch2(R, P, X, g, cliques);
	
	cout << cliques.size() << " cliques\n";
	
	cout << "Enumeration done\n";
	ofstream outfile (outputfname.c_str());
	if (outfile.is_open()){
		for(unsigned int i(0); i<cliques.size(); ++i){
			for(set<int>::iterator it=cliques[i].begin(); it!=cliques[i].end(); ++it){
				outfile << ind_to_node[*it] << " ";
			}
			outfile << endl;
		}
		outfile.close();
	}
	else cout << "Unable to open outputfile\n";
}


