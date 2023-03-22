//
//  Create the Clique complex from a binary network
//
//  Noel Malod-Dognin, January 2018
//  Based on Bron-Kerbosch maximal clique enumeration algorithm as implemented by Atul Singh (2016).
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
	Graph()
	{
		
	}
	
	
	void addNode(int inNodeIndex)
	{
		if (mNodes.find(inNodeIndex) != mNodes.end())
			return;  //Throw Exception that Node already exists
		mNodes.insert(inNodeIndex);
		mAdjacencyList.insert(make_pair(inNodeIndex, set<int>()));
	}
	
	void addEdge(int inStartNode, int inEndNode)
	{
		if (mNodes.find(inStartNode) == mNodes.end())
		{
			//cout << "Nodes doesn't adding the Start Node" << endl;
			mNodes.insert(inStartNode);
			mAdjacencyList.insert(make_pair(inStartNode, set<int>()));
		}
		if (mNodes.find(inEndNode) == mNodes.end())
		{
			//cout << "Nodes doesn't adding the End Node" << endl;
			mNodes.insert(inEndNode);
			mAdjacencyList.insert(make_pair(inEndNode, set<int>()));
		}
		
		//Check if there is already in the Adjacency List
		if (mAdjacencyList.find(inStartNode) == mAdjacencyList.end())
		{
			mAdjacencyList.insert(make_pair(inStartNode, set<int>()));
		}
		else
		{
			mAdjacencyList.find(inStartNode)->second.insert(inEndNode);
		}
		
		if (mAdjacencyList.find(inEndNode) == mAdjacencyList.end())
		{
			mAdjacencyList.insert(std::make_pair(inEndNode, set<int>()));
		}
		else
		{
			mAdjacencyList.find(inEndNode)->second.insert(inStartNode);
		}
	}
	
	
	bool are_adjacent(int inNode1, int inNode2)
	{
		//Checks if Node1 and Node2 are adjacent
		return  mAdjacencyList[inNode1].find(inNode2) != mAdjacencyList[inNode1].end() ? true : false;
	}
	
	set<int> get_node_neighbours(int inNode)
	{
		return mAdjacencyList[inNode];
	}
	
	
	vector< set<int> > find_all_cliques(int min_vertex_in_clique=2)
	{
		//Implements Bron-Kerbosch algorithm , Version 2
		vector< set<int> > cliques;
		typedef tuple< set<int>, set<int>, set<int>, int, int   >  stackNode;
		stack< stackNode > stack_;
		int nd = -1;
		int disc_num = mNodes.size();
		stackNode search_node = make_tuple(set<int>(), set<int>(mNodes), set<int>(), nd, disc_num);
		stack_.push(search_node);
		while (stack_.size() > 0)
		{
			//if(stack_.size() % 100 == 1){
			//	cout << "-- Remaining nodes " <<  stack_.size() << std::endl;
			//}
			stackNode tupel = stack_.top();
			stack_.pop();
			
			set<int> c_compsub = get<0>(tupel);
			set<int> c_candidates = get<1>(tupel);
			set<int> c_not = get<2>(tupel);
			int c_nd = get<3>(tupel);
			int c_disc_cum = get<4>(tupel);
			
			if (c_candidates.size() == 0 && c_not.size() == 0)
			{
				//Here we are pushing the Cliques
				if (c_compsub.size() >= min_vertex_in_clique)
				{
					//Before Pushing Back check if it already exists or not
					bool alreadyPresent = false;
					for (unsigned int i(0); i < cliques.size(); ++i)
					{
						if (cliques[i].size() == c_compsub.size())
						{
							bool setMatched = true;
							set<int>::iterator it1, it2;
							for (it1 = cliques[i].begin(), it2 = c_compsub.begin();
								 it1 != cliques[i].end() && it2 != c_compsub.end();
								 ++it1, ++it2 )
							{
								if ( (*it1) != (*it2))
								{
									setMatched = false;
									break;
								}
							}
							
							if (setMatched)
							{
								alreadyPresent = true;
								break;
							}
						}
					}
					
					if (false ==  alreadyPresent)
						cliques.push_back( std::set<int>(c_compsub));
					continue;
				}
			}
			
			set<int>::iterator it = c_candidates.begin();
			while ( it != c_candidates.end() )
			{
				int u = *it;
				it++;
				
				if ((c_nd == -1) || !(are_adjacent(u, c_nd)))
				{
					c_candidates.erase(u);
					set<int> Nu = get_node_neighbours(u);
					set<int> new_compsub = set<int>(c_compsub);
					new_compsub.insert(u);
					set<int> new_candidates;
					set_intersection(c_candidates.begin(), c_candidates.end(), Nu.begin(), Nu.end(), inserter(new_candidates, new_candidates.begin()));
					
					set<int> new_not;
					set_intersection(c_not.begin(), c_not.end(), Nu.begin(), Nu.end(), inserter(new_not, new_not.begin()));
					
					if (c_nd != -1)
					{
						if (new_not.find(c_nd) != new_not.end())
						{
							int new_disc_num = c_disc_cum - 1;
							if (new_disc_num > 0)
							{
								stackNode new_search_node = std::make_tuple(new_compsub, new_candidates, new_not, c_nd, new_disc_num);
								stack_.push(new_search_node);
							}
						}
						else
						{
							int new_disc_num = mNodes.size();
							int new_nd = c_nd;
							for (int cand_nd : new_not)
							{
								set<int> tempSet;
								set<int> tempNeightBours = get_node_neighbours(c_nd);
								set_intersection(new_candidates.begin(), new_candidates.end(),
												 tempNeightBours.begin(), tempNeightBours.end(),
												 inserter(tempSet, tempSet.begin()));
								
								int cand_disc_num = new_candidates.size() - tempSet.size();
								
								if (cand_disc_num < new_disc_num)
								{
									new_disc_num = cand_disc_num;
									new_nd = cand_nd;
								}
							}
							
							stackNode new_search_node = std::make_tuple(new_compsub, new_candidates, new_not, new_nd, new_disc_num);
							stack_.push(new_search_node);
						}
					}
					else
					{
						stackNode new_search_node = make_tuple(new_compsub, new_candidates, new_not, c_nd, c_disc_cum);
						stack_.push(new_search_node);
					}
					
					c_not.insert(u);
					int new_disc_num = 0;
					for (int x : c_candidates)
					{
						if (false == are_adjacent(x, u))
						{
							new_disc_num += 1;
						}
					}
					
					if (new_disc_num < c_disc_cum && new_disc_num > 0)
					{
						stackNode new1_search_node = make_tuple(c_compsub, c_candidates, c_not, u, new_disc_num);
						stack_.push(new1_search_node);
					}
					else
					{
						stackNode new1_search_node = make_tuple(c_compsub, c_candidates, c_not, c_nd, c_disc_cum);
						stack_.push(new1_search_node);
						
					}
				}
				
			}
		}
		
		
		return cliques;
		
	}
	
private:
	set<int> mNodes;
	map< int, set<int> > mAdjacencyList;
	
	
};


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
			G.addEdge(ind1, ind2);
		}
		myfile.close();
		cout << "Network has " << ind_to_node.size() << " nodes\n";
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
	vector< set<int >  > cliques = g.find_all_cliques();
	
	//replace by a function that export a list of maximal cliques
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