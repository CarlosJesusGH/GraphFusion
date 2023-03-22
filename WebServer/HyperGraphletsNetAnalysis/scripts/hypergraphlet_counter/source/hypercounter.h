#ifndef HYPERCOUNTER_H
#define HYPERCOUNTER_H

#include "hypergraph.h"

typedef vector<set<int> > V2Vs_set;
typedef map<int,set<int> > V2Hs_map;
typedef map<int, V2Hs_map > VV2Hs_tensor;
typedef vector<vector<long long int> > Count;

class hypercounter
{
    public:
        // Constructors & Destructor
        hypercounter();
        hypercounter(const hypergraph&);
        virtual ~hypercounter();

        // Setters & Getters
        void initialise_counter(const hypergraph&); // Initialise counter with hypergraph
        void read_config_orbit_map(const string&); // Read in configuration/orbit map

        V2Vs_set get_node_neighbours();
        V2Vs_set get_nodes_hedges();
        Count get_hypercount();

        // Counter
        void global_counter(const int, const int); // Outputs matrix of the counts of all nodes
        void counter(const int); // Outputs HDV for specified node
        void process_pairs(const int, const int);
        void process_triplets(const int, const int, const int); // From triplets of vertices computes overlap of hyperedges and call classification
        void process_quadruplets(const int, const int, const int, const int); // From quadruplets of vertices computes overlap of hyperedges and call classification

        // Write
        void output_hdvs_to_file(const string &path); // Write count to a file given by "path"

    private:
        // Class Attributes
        //VV2Hs_tensor nodes_common_hedges; // (sparse) tensor giving the list of hyperedges containing each pair of vertices
        V2Vs_set nodes_hedges;
        V2Vs_set node_neighbours; // (sparse) matrix giving the neighbour set for each vertex
        hypergraph h;
        Count hdvs;
        V2Vs_vector config_orbit_map;

};

#endif // HYPERCOUNTER_H

