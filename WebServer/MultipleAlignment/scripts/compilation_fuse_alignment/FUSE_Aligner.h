//============================================================================
// Name        : L-GRAAL.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#define NDEBUG

#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <map>

#include <boost/program_options.hpp>

#include <lemon/smart_graph.h>
#include <lemon/bp_matching.h>

#include "H-Clustering_2.h"

/* for including a wait loop, needed for memory measurement */
extern "C"{
    #include <unistd.h>
}

//#include "H_Clustering_2.h"

namespace po = boost::program_options;

using namespace std;


/**
 * The multiple network aligner class
 * - Given a k-partite network encoding the node-to-node mapping between the k networks,
 *   it applies a greedy seed+extend strategy to form clusters of similar nodes accross networks.
 */
template <template <class k, class v> class Sparse_Matrix_T> class MNA_SBM_T {

public:
	typedef lemon::SmartBpGraph BPGraph;
	typedef BPGraph::Edge Edge;
	typedef BPGraph::Node Node;
	typedef BPGraph::NodeMap<int> NO_Map;
	typedef BPGraph::EdgeMap<long int> Aweight_Map;

	typedef lemon::MaxWeightedBipartiteMatching< BPGraph, Aweight_Map> MWBM;

private:

	/*
	 * Parameters
	 */

	string network_fname, seq_dist_fname, tri_dist_fname, output_fname;
	float alpha;


	/*
	 * Data
	 */
	vector<string> network_names;
	vector<string> ids_to_nodes;
	map<string, int> nodes_to_ids;

	vector<vector<int> > network_nodeids;
	Sparse_Matrix_T<int, float> pairwise_score;
	Sparse_Matrix_T<int, float> sequence_score;
	size_t nb_networks;
	bool k_only;
	string order_method;

	vector<pair<int, int> > ordering;

	vector< vector<vector<int> > > multiple_mapping;

	/*
	 * Parse the command line
	 */
	void parse_command_line(int argc, char** argv){
		po::options_description desc("Allowed options");
		po::options_description genopt("General options");
		genopt.add_options()
			("help,h", "Produce this help message")
			("input_networks,n",		po::value<std::string>(&network_fname)->required(),		"Input networks filename")
			("input_seq_distances,s",	po::value<std::string>(&seq_dist_fname)->required(),	"Input sequence distance filename")
			("input_nmtf_distances,t",	po::value<std::string>(&tri_dist_fname)->required(),	"Input NMTF distance filename")
			("output,o",				po::value<std::string>(&output_fname)->required(),		"Output file name")
			("alpha,a",					po::value<float>(&alpha)->default_value(0.6),			"From sequence only (1) to NMTF only (0)")
			("ordering,r",				po::value<std::string>(&order_method)->default_value("Min_Size"),	"Ordering: Min_Size, or Hierarchical")
			("k_only,k",				po::value<bool>(&k_only)->default_value(false),			"Boolean:\n - true -> clusters cover exactly k networks,\n - false -> clusters cover 1 to k networks");
		desc.add(genopt);
		//transfer command line to variable vm
		try{
			po::variables_map vm;
			po::store(po::parse_command_line(argc, argv, desc), vm);
			po::notify(vm);
			if (vm.count("help"))	{std::cerr << desc << std::endl; exit(EXIT_FAILURE);}
		}
		catch(std::exception& e)
		{
			std::cerr << "\nError: " << e.what() << "\n\n";
			std::cerr << desc << std::endl; exit(EXIT_FAILURE);
		}
	};

	void Load_Data(){
		/*
		 * Load network list
		 */
		ifstream ifile(network_fname.c_str(), ifstream::in);
		if(!ifile.is_open()){
			cout << "Unable to open " << network_fname << endl;
			exit(1);
		}

		string line, name1, name2;
		while(getline(ifile, line)){
			stringstream ss(line);
			ss >> name1;
			network_names.push_back(name1);
		}
		ifile.close();
		nb_networks = network_names.size();
		cout << "\n\033[1;31m Loading Data\033[0m\n";
		network_nodeids.resize(nb_networks);

		/*
		 * Load each network (only its node set)
		 */
		int counter = 0;
		for(size_t i(0); i<nb_networks; ++i){
			ifstream ifile2(network_names[i].c_str(), ifstream::in);
			if(!ifile2.is_open()){
				cout << "-- Unable to open " << network_names[i] << endl;
				exit(1);
			}
			//get ride of the 4 first header lines
			for(size_t j(0); j<4; ++j){
				getline(ifile2, line);
			}
			//retrieving number of nodes in the current network
			size_t nb_nodes;
			getline(ifile2, line);
			stringstream ss2(line);
			ss2 >> nb_nodes;

			for(size_t j(0); j<nb_nodes; ++j){
				getline(ifile2, line);
				char name[1024];
				sscanf(line.c_str(), "|{%[^}^|]s", name);
				network_nodeids[i].push_back( counter );
				ids_to_nodes.push_back( string(name) );
				nodes_to_ids[string(name)] = counter;
				counter++;
			}
			ifile2.close();
			cout << "\033[1;31m -- [" << i << "]\033[0m <- " << network_names[i] << "; " << nb_nodes << " nodes\n";
		}

		/*
		 * Load node sequence scores
		 */
		ifstream ifile3(seq_dist_fname.c_str(), ifstream::in);
		if(!ifile3.is_open()){
			cout << "-- Unable to open " << seq_dist_fname << endl;
			exit(1);
		}

		//get ride of the first header line
		getline(ifile3, line);
		string p1, p2;
		int id1, id2;
		float score, ascore;
		while(getline(ifile3, line)){
			stringstream ss2(line);
			ss2 >> p1 >> p2 >> score;
			ascore = alpha*score;
			id1 = nodes_to_ids[p1];
			id2 = nodes_to_ids[p2];
			pairwise_score.set(id1,id2,ascore);
			sequence_score.set(id1,id2,score);
		}
		cout << "\033[1;31m -- Sequence scores loaded\n";
		/*
		 * Load node pairwize scores from second file
		 */
		ifstream ifile4(tri_dist_fname.c_str(), ifstream::in);
		if(!ifile4.is_open()){
			cout << "Unable to open " << tri_dist_fname << endl;
			exit(1);
		}

		//get ride of the first header line
		getline(ifile4, line);
		while(getline(ifile4, line)){
			stringstream ss2(line);
			ss2 >> p1 >> p2 >> score;
			score = (1.-alpha)*score;
			id1 = nodes_to_ids[p1];
			id2 = nodes_to_ids[p2];
			score += pairwise_score.get(id1,id2);
			pairwise_score.set(id1,id2,score);
		}
		cout << "\033[1;31m -- NMTF scores loaded\n";

		//for (int node1(0); node1<ids_to_nodes.size(); ++node1){
		//	for(int node2(node1+1); node2 < ids_to_nodes.size(); ++node2){
		//		score = pairwise_score.get(node1,node2);
		//		if( score > 0. ){
		//			pairwise_score.set(node1,node2,score);
		//		}
		//	}
		//}
		//sanity check
		//int non_napped( ids_to_nodes.size()-pairwise_score.get_NZ_row_size());
		//float mapped_perc( 100.*float(pairwise_score.get_NZ_row_size())/float(ids_to_nodes.size()) );
		//cout << "## " << mapped_perc << " % of the nodes have at least one counterpart\n";

		//init multiple mapping with the nodes in network 1
		multiple_mapping.clear();
		multiple_mapping.resize(nb_networks);
		for(size_t k(0); k< nb_networks; ++k){
			multiple_mapping[k].reserve(network_nodeids[k].size());
			for(size_t i(0); i<network_nodeids[k].size() ; ++i){
				multiple_mapping[k].push_back( vector<int>(1, network_nodeids[k][i])  );
			}
		}
	};

	/*
	 * Create an alignment order, so that networks are aligned from the smallest one to the largest one.
	 */
	void Set_Order_MIN(){

		cout << "\n\033[1;32m Computing Min_Size ordering:\033[0m\n";

		multimap<int,int> sorter;

		for(size_t i(0); i<nb_networks; ++i){
			sorter.insert(pair<int,int>(network_nodeids[i].size(),i));
		}
		vector<int> loc_order;
		for(multimap<int,int>::iterator it(sorter.begin()); it != sorter.end(); ++it){
			loc_order.push_back(it->second);
		}

		for(size_t i(1); i<nb_networks; ++i){
			ordering.push_back(pair<int,int>(loc_order[0], loc_order[i]));
		}

		for(size_t i(0);i<ordering.size(); ++i){
			cout << "\033[1;32m -- " << i+1 << " [" << ordering[i].first << "," << ordering[i].second << "] -> " << ordering[i].first << "\033[0m:\n";
		}
	};

	/*
	 * Create an alignment order, so that networks are aligned from the smallest one to the largest one.
	 */
	void Set_Order_MIN_MAX(){

		cout << "\n\033[1;32m Computing Min_MAX ordering:\033[0m\n";
		cout << "\033[1;32m -- Step 1: Finding smaller network\033[0m\n";

		size_t smaller_size(network_nodeids[0].size());
		size_t smaller_net(0);

		for(size_t i(1); i<nb_networks; ++i){
			if(network_nodeids[i].size()<smaller_size){
				smaller_size=network_nodeids[i].size();
				smaller_net=i;
			}
		}
		vector<size_t> order, left;
		order.push_back(smaller_net);
		for(size_t i(0); i<nb_networks; ++i){
			if(i!=smaller_net){
				left.push_back(i);
			}
		}
		cout << "\033[1;32m -- [" << smaller_net << "]\033[0m, with " << smaller_size << " nodes\n";


		cout << "\033[1;32m -- Step 2: computing all pairwise similarities\033[0m\n";
		Sparse_Matrix_T<int,float> Similarity_Scores;
		for(size_t k(0); k<nb_networks; ++k){
			for(size_t l(k+1); l<nb_networks; ++l){
				float score = 0.;

				// align networks i and j
				BPGraph Global_flow;
				NO_Map Smap(Global_flow), Tmap(Global_flow);
				Aweight_Map Arc_Cost(Global_flow);
				std::vector< Node > S,T;

				//adding nodes
				Global_flow.reserveNode(multiple_mapping[k].size() + multiple_mapping[l].size());
				//Global_flow.reserveEdge();
				for(size_t i(0); i< multiple_mapping[k].size(); ++i){
					Node n=Global_flow.addRedNode();
					Smap[n] = i;
					S.push_back(n);
				}
				for(size_t i(0); i< multiple_mapping[l].size(); ++i){
					Node n=Global_flow.addBlueNode();
					Tmap[n] = i;
					T.push_back(n);
				}

				//adding edges
				Node u1, u2;
				Edge e1;
				int pos_edge(0);

				//loop over multiple mapping clusters
				for(size_t i(0); i< multiple_mapping[k].size(); ++i){
					vector<int> & cluster_i(multiple_mapping[k][i]);
					u1 = S[i];

					//loop over nodes in network k
					for(size_t j(0); j< multiple_mapping[l].size(); ++j){
						vector<int> & cluster_j(multiple_mapping[l][j]);
						u2 = T[j];
						float edge_w(0.);

						//loop over nodes in clusters
						for(size_t kk(0); kk < cluster_i.size(); ++kk){
							for(size_t ll(0); ll < cluster_j.size(); ++ll){
								edge_w += pairwise_score.get(cluster_i[kk],cluster_j[ll]);
							}
						}
						if(edge_w > 0.){
							pos_edge++;
							e1 = Global_flow.addEdge(u1, u2);
							Arc_Cost[e1] = int(edge_w*10000.);
				}}}
				if(pos_edge==0){
					cout << "-- No positive edge in Bi-partite matching ?\n";
				}
				MWBM global_solver(Global_flow, Arc_Cost);
				global_solver.run();
				score = global_solver.matchingWeight()/10000.;
				score/= (float)(multiple_mapping[k].size()+multiple_mapping[l].size());
				cout << "\033[1;32m -- pair [" << k << "," << l << "]\033[0m evaluated: sim = " << score << "\n";

				Similarity_Scores.set(k,l,score);
			}
		}
		// while some network have not been added
		while(left.size()>0){
			int best_net(-1);
			float best_score(-1.);
			// find best network
			for(int i(0); i< left.size(); ++i){
				float score_i(0.);
				size_t net_i(left[i]);
				for(int j(0); j< order.size(); ++j){
					size_t net_j(order[j]);
					score_i += Similarity_Scores.get(net_i,net_j);
				}
				if(score_i>best_score){
					best_score=score_i;
					best_net=net_i;
				}
			}
			//add it to order, and remove it from left
			order.push_back(best_net);
			vector<size_t> new_left;
			for(int i(0); i< left.size(); ++i){
				if(left[i] != best_net){
					new_left.push_back(left[i]);
				}
			}
			left= new_left;
		}


		cout << "\033[1;32m -- Step 3: Building ordering\033[0m\n";

		for(size_t i(1); i<nb_networks; ++i){
			ordering.push_back(pair<int,int>(order[0], order[i]));
		}


		for(size_t i(0);i<ordering.size(); ++i){
			cout << "\033[1;32m -- " << i+1 << " [" << ordering[i].first << "," << ordering[i].second << "] -> " << ordering[i].first << "\033[0m:\n";
		}
	};


	/*
	 * Create an alignment order, so that networks are aligned from the most similar to the most dissimilar ones, as determined by hierarchical clustering
	 */
	void Set_Order_Hierachical(){
		cout << "\n\033[1;32m Computing Hierarchical ordering:\033[0m\n";
		Sparse_Matrix_T<int,float> Similarity_Scores;
		for(size_t k(0); k<nb_networks; ++k){
			for(size_t l(k+1); l<nb_networks; ++l){
				float score = 0.;

				// align networks i and j
				BPGraph Global_flow;
				NO_Map Smap(Global_flow), Tmap(Global_flow);
				Aweight_Map Arc_Cost(Global_flow);
				std::vector< Node > S,T;

				//adding nodes
				Global_flow.reserveNode(multiple_mapping[k].size() + multiple_mapping[l].size());
				//Global_flow.reserveEdge();
				for(size_t i(0); i< multiple_mapping[k].size(); ++i){
					Node n=Global_flow.addRedNode();
					Smap[n] = i;
					S.push_back(n);
				}
				for(size_t i(0); i< multiple_mapping[l].size(); ++i){
					Node n=Global_flow.addBlueNode();
					Tmap[n] = i;
					T.push_back(n);
				}

				//adding edges
				Node u1, u2;
				Edge e1;
				int pos_edge(0);

				//loop over multiple mapping clusters
				for(size_t i(0); i< multiple_mapping[k].size(); ++i){
					vector<int> & cluster_i(multiple_mapping[k][i]);
					u1 = S[i];

					//loop over nodes in network k
					for(size_t j(0); j< multiple_mapping[l].size(); ++j){
						vector<int> & cluster_j(multiple_mapping[l][j]);
						u2 = T[j];
						float edge_w(0.);

						//loop over nodes in clusters
						for(size_t kk(0); kk < cluster_i.size(); ++kk){
							for(size_t ll(0); ll < cluster_j.size(); ++ll){
								edge_w += pairwise_score.get(cluster_i[kk],cluster_j[ll]);
							}
						}
						if(edge_w > 0.){
							pos_edge++;
							e1 = Global_flow.addEdge(u1, u2);
							Arc_Cost[e1] = int(edge_w*10000.);
				}}}
				if(pos_edge==0){
					cout << "-- No positive edge in Bi-partite matching ?\n";
				}
				MWBM global_solver(Global_flow, Arc_Cost);
				global_solver.run();
				score = global_solver.matchingWeight()/10000.;
				score/= (float)(multiple_mapping[k].size()+multiple_mapping[l].size());
				cout << "\033[1;32m -- pair [" << k << "," << l << "]\033[0m evaluated: sim = " << score << "\n";

				Similarity_Scores.set(k,l,score);
			}
		}

		H_Clustering<Sparse_Matrix_T<int,float> > upgma_clustering(Similarity_Scores, nb_networks);
		upgma_clustering.UPGMA_Clustering();
		ordering = upgma_clustering.get_h_clustering();

		cout << "\033[1;32m -- Proposed ordering:\033[0m\n";
		for(size_t i(0);i<ordering.size(); ++i){
			cout << "\033[1;32m -- " << i+1 << " [" << ordering[i].first << "," << ordering[i].second << "] -> " << ordering[i].first << "\033[0m:\n";
		}
	};

	/*
	 * Multiple network alignment using successive bi-partite matching
	 * a.k.a. progressive alignment
	 *
	 */
	void K_Align(){

		cout << "\n\033[1;34m Aligning Networks:\033[0m\n";

		for(size_t m(0); m<ordering.size(); ++m){
			int k = ordering[m].first;
			int l = ordering[m].second;

			int size_k = multiple_mapping[k].size();
			int size_l = multiple_mapping[l].size();
			/*
			 * aligning multiple mapping to network k
			 *
			 */
			//cout << "\033[1;31m[" << k << "," << l << "]\033[0m:\n";

			//step 1: creating dedicated bi-partite graph: S = multiple mapping, T = network k
			BPGraph Global_flow;
			NO_Map Smap(Global_flow), Tmap(Global_flow);
			Aweight_Map Arc_Cost(Global_flow);
			std::vector< Node > S,T;

			//adding nodes
			Global_flow.reserveNode(multiple_mapping[k].size() + multiple_mapping[l].size());
			//Global_flow.reserveEdge();
			for(size_t i(0); i< multiple_mapping[k].size(); ++i){
				Node n=Global_flow.addRedNode();
				Smap[n] = i;
				S.push_back(n);
			}
			for(size_t i(0); i< multiple_mapping[l].size(); ++i){
				Node n=Global_flow.addBlueNode();
				Tmap[n] = i;
				T.push_back(n);
			}

			//adding edges
			Node u1, u2;
			Edge e1;
			int pos_edge(0);

			//loop over multiple mapping clusters
			for(size_t i(0); i< multiple_mapping[k].size(); ++i){
				vector<int> & cluster_i(multiple_mapping[k][i]);
				u1 = S[i];

				//loop over nodes in network k
				for(size_t j(0); j< multiple_mapping[l].size(); ++j){
					vector<int> & cluster_j(multiple_mapping[l][j]);
					u2 = T[j];
					float edge_w(0.);

					//loop over nodes in clusters
					for(size_t kk(0); kk < cluster_i.size(); ++kk){
						for(size_t ll(0); ll < cluster_j.size(); ++ll){
							edge_w += pairwise_score.get(cluster_i[kk],cluster_j[ll]);
						}
					}
					if(edge_w > 0.){
						pos_edge++;
						e1 = Global_flow.addEdge(u1, u2);
						Arc_Cost[e1] = int(edge_w*10000.);
			}}}
			//cout << "-- Bi-partite network created: " << multiple_mapping[k].size() + multiple_mapping[l].size() << " nodes and " << pos_edge << " edges \n";

			//Step 2: solving maximum weight bipartite matching
			if(pos_edge==0){
				cout << "-- No positive edge in Bi-partite matching ?\n";
			}
			MWBM global_solver(Global_flow, Arc_Cost);
			global_solver.run();
			//B_value = global_solver.matchingWeight();
			//LR_value= LR_value/10000.;

			// Step 3: Retrieving selected vertices and edges
			vector<pair<int, int> > solution;
			size_t nk;
			vector<bool> mapped_cluster_k(multiple_mapping[k].size(), false);
			vector<bool> mapped_cluster_l(multiple_mapping[l].size(), false);
			for(size_t c(0); c<multiple_mapping[k].size(); ++c){
				u1 = S[c];
				u2 = global_solver.mate(u1);
				if(Global_flow.valid(u2)){
					nk = Tmap[u2];
					solution.push_back( pair<int, int>(c,nk) );
					mapped_cluster_k[c] = true;
					mapped_cluster_l[nk] = true;
			}}
			//modified up to here   <------- leftover ????

			//updating multiple mapping: non aligned elements are discarded (V1)
			vector< vector<int> > multiple_mapping2;
			if(k_only){
				multiple_mapping2.reserve(solution.size());
				for(size_t i(0); i<solution.size() ; ++i){
					vector<int> & cluster_k( multiple_mapping[k][solution[i].first] );
					vector<int> & cluster_l( multiple_mapping[l][solution[i].second] );
					vector<int> new_cluster( cluster_k.size() + cluster_l.size(), 0 );
					for(size_t j(0); j< cluster_k.size(); ++j){
						new_cluster[j] = cluster_k[j];
					}
					for(size_t j(0); j< cluster_l.size(); ++j){
						new_cluster[j+cluster_k.size()] = cluster_l[j];
					}
					multiple_mapping2.push_back( new_cluster );
			}}
			else{
				//first adding mapped clusters + their mapped nodes
				multiple_mapping2.reserve(multiple_mapping[k].size()+multiple_mapping[l].size() -(2*solution.size()));
				for(size_t i(0); i<solution.size() ; ++i){
					vector<int> & cluster_k( multiple_mapping[k][solution[i].first] );
					vector<int> & cluster_l( multiple_mapping[l][solution[i].second] );
					vector<int> new_cluster( cluster_k.size() + cluster_l.size(), 0 );
					for(size_t j(0); j< cluster_k.size(); ++j){
						new_cluster[j] = cluster_k[j];
					}
					for(size_t j(0); j< cluster_l.size(); ++j){
						new_cluster[j+cluster_k.size()] = cluster_l[j];
					}
					multiple_mapping2.push_back( new_cluster );
				}
				//second, adding non-mapped clusters from k
				for(size_t i(0); i<mapped_cluster_k.size(); ++i){
					if(!mapped_cluster_k[i]){
						multiple_mapping2.push_back( multiple_mapping[k][i]);
				}}
				//third, adding non-mapped clusters from l
				for(size_t i(0); i<mapped_cluster_l.size(); ++i){
					if(!mapped_cluster_l[i]){
						multiple_mapping2.push_back( multiple_mapping[l][i] );
			}}}
			multiple_mapping[k] = multiple_mapping2;
			multiple_mapping[l].clear();
			cout << "\033[1;34m -- [" << k << "," << l << "] -> " << k << "\033[0m: " << multiple_mapping[k].size() << " clusters from " << size_k << ", " << size_l << "\n";
		}
	};

	/*
	 * Score and rank the clusters
	 */
	void Score_and_Rank(){

		vector<vector<int> > & clustering(multiple_mapping[0]);

		vector<float> combined_score(clustering.size(), 0.);
		vector<float> blast_score(clustering.size(), 0.);
		vector<float> best_edge_score(clustering.size(), 0.);
		vector<float> best_edge_score2(clustering.size(), 0.);

		size_t p1,p2;

		multimap<float, int> sorter;
		float cscore(0.), sscore(0.), bscore(0.), bscore2(0.),tmp, tmp2;
		size_t ind;
		/* for(size_t c(0); c<clustering.size(); ++c){
					vector<int> & cluster( clustering[c] );
					cscore = 0.;
					sscore = 0.;
					bscore = 0.;
					bscore2 = 0.;
					for(size_t i(0); i<cluster.size(); ++i){
						p1 = cluster[i];
						for(size_t j(i+1); j<cluster.size(); ++j){
							p2 = cluster[j];
							tmp = pairwise_score.get(p1,p2);
							tmp2 = sequence_score.get(p1,p2);
							cscore += tmp;
							sscore += tmp2;
							if (tmp > bscore) {	bscore = tmp;	}
							if (tmp2 > bscore2) {	bscore2 = tmp2;	}
						}
					}
					combined_score[c] = cscore;
					blast_score[c] = sscore;
					best_edge_score[c] = bscore;
					best_edge_score2[c] = bscore2;
					if(bscore2 > 0.){
						sorter.insert(pair<float,int>( best_edge_score2[c], c ));
					}
				} */
		for(size_t c(0); c<clustering.size(); ++c){
			vector<int> & cluster( clustering[c] );
			cscore = 0.;
			sscore = 0.;
			for(size_t i(0); i<cluster.size(); ++i){
				p1 = cluster[i];
				for(size_t j(i+1); j<cluster.size(); ++j){
					p2 = cluster[j];
					tmp = pairwise_score.get(p1,p2);
					cscore += (tmp*tmp);
					sscore += sequence_score.get(p1,p2);
				}
			}
			float ss(cluster.size()*(cluster.size()-1));
			combined_score[c] = sqrt( 2.*cscore/ss );
			blast_score[c] = sscore;
			if(cscore > 0.){
				sorter.insert(pair<float,int>( combined_score[c], c ));
			}
		}

		ofstream ofile(output_fname.c_str(), ofstream::out);
		if(!ofile.is_open()){
			cout << "Error: Unable to open " << output_fname << endl;
			exit(1);
		}

		for(multimap<float,int>::reverse_iterator it(sorter.rbegin()); it != sorter.rend(); ++it){
			cscore = it->first;
			ind = it->second;
			bscore = blast_score[ind];

			vector<int> & cluster( clustering[ind] );
			ofile << cscore << "\t" << bscore << "\t";
			for(size_t i(0); i<cluster.size(); ++i){
				ofile << ids_to_nodes[ cluster[i] ] << "\t";
			}
			ofile << endl;
		}
		ofile.close();


	};





	/*
	 * Write node clusters into output file
	 */
	void Output_Clusters(){
		ofstream ofile(output_fname.c_str(), ofstream::out);
		if(!ofile.is_open()){
			cout << "Error: Unable to open " << output_fname << endl;
			exit(1);
		}
		//unless the process was wrong, the final alignment is in multiple_mapping[0]
		for(size_t c(0); c<multiple_mapping[0].size(); ++c){
			vector<int> & cluster( multiple_mapping[0][c] );
			for(size_t i(0); i<cluster.size(); ++i){
				ofile << ids_to_nodes[ cluster[i] ] << "\t";
			}
			ofile << endl;
		}
		ofile.close();
	};

public:

	/**
	 * Main function, which load the k-partite networks, generates the clusters, and output them in a file
	 */
	int work(int argc, char** argv) {
		//Parse command line options
		parse_command_line(argc, argv);

		//Load input networks and node pairwise scores
		Load_Data();

		//Ordering strategy
		if(order_method=="Min_Size"){
			Set_Order_MIN();
		}
		else if(order_method=="Min_MAX"){
			Set_Order_MIN_MAX();
		}
		else{
			Set_Order_Hierachical();
		}

		//Compute the multiple network alignment
		K_Align();

		//Score and rank clusters
		Score_and_Rank();

		//Write obtained clusters into output file
		//Output_Clusters();

		return(0);
	};
};
