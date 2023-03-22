#include "hypercounter.h"
#include "time.h"
#include "string.h"
#include <boost/algorithm/string.hpp>
#include <omp.h>
#include <math.h>
#include <algorithm>

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Constructor & Destructor ///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

hypercounter::hypercounter()
{
    // ctor
    config_orbit_map.resize(4);// Initialise the configuration/orbit map for 1/2/3/4 hypergraphlets
    for (int i = 0; i!=4;++i)
    {
        int n = pow(2,pow(2,i+1)-1);
        config_orbit_map[i].resize(n);
    }
    read_config_orbit_map("./hypergraphlets_1_4_map");

}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

hypercounter::~hypercounter()
{
    // dtor
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

hypercounter::hypercounter(const hypergraph & H)
{
    config_orbit_map.resize(4);// Initialise the configuration/orbit map for 1/2/3/4 hypergraphlets
    for (int i = 0; i!=4;++i)
    {
        int n = pow(2,pow(2,i+1)-1);
        config_orbit_map[i].resize(n);
    }
    read_config_orbit_map("./hypergraphlets_1_4_map");

    h = H;
    V2Vs_vector hedge_list = h.get_hedges_list();
    node_neighbours.resize(h.get_nb_nodes());
    nodes_hedges.resize(h.get_nb_nodes());
    hdvs.resize(h.get_nb_nodes());

    for (size_t it = 0; it != hedge_list.size(); ++it)
    {
        int l = hedge_list[it].size();
        nodes_hedges[hedge_list[it][l-1]].insert(it);
        for (int i = 0; i != l-1; ++i)
        {
            int ii = hedge_list[it][i];
            nodes_hedges[ii].insert(it);
            for (int j = i+1; j != l; ++j)
            {
                int jj = hedge_list[it][j];
                node_neighbours[ii].insert(jj);
                node_neighbours[jj].insert(ii);
            }
        }
    }
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Setters & Getters //////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

V2Vs_set hypercounter::get_node_neighbours()
{
    return node_neighbours;
}

V2Vs_set hypercounter::get_nodes_hedges()
{
    return nodes_hedges;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void hypercounter::initialise_counter(const hypergraph & H)
{
    h = H;
    hdvs.clear(); node_neighbours.clear(); nodes_hedges.clear();
    V2Vs_vector hedge_list = h.get_hedges_list();
    node_neighbours.resize(h.get_nb_nodes());
    nodes_hedges.resize(h.get_nb_nodes());
    hdvs.resize(h.get_nb_nodes());

    for (size_t it = 0; it != hedge_list.size(); ++it)
    {
        int l = hedge_list[it].size();
        nodes_hedges[hedge_list[it][l-1]].insert(it);
        for (int i = 0; i != l-1; ++i)
        {
            int ii = hedge_list[it][i];
            nodes_hedges[ii].insert(it);
            for (int j = i+1; j != l; ++j)
            {
                int jj = hedge_list[it][j];
                node_neighbours[ii].insert(jj);
                node_neighbours[jj].insert(ii);
            }
        }
    }
}

void hypercounter::read_config_orbit_map(const string& path)
{
    std::ifstream file_in(path, ios::in);
    if (file_in.fail())
    {
        cerr << "ERROR: Configuration orbit map file hypergraphlets_1_4_map is not in the root directory and could not be opened.\n";
        exit(1);
    }

    string line;
    vector<string> tokens;
    while( std::getline(file_in, line) ) // Second reading to get hyperedges list
    {
        boost::split(tokens,line,[](char c){return c == '\t';});
        int nb_nodes = to_i(tokens[0]) - 1 ;
        int config = to_i(tokens[1]);
        int orbit = to_i(tokens[2]);

        config_orbit_map[nb_nodes][config] = orbit;
    }
    file_in.close();
}


Count hypercounter::get_hypercount()
{
    return hdvs;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Output functions ///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void hypercounter::output_hdvs_to_file(const string &path)
{
    ofstream output_file( path, ios::out );
    size_t M = hdvs.size();
    for (size_t i = 0; i != M; ++i)
    {
        size_t N = hdvs[i].size();
        output_file << i;
        for (size_t j = 0; j != N; ++j)
        {
            if (hdvs[i][j] != 0) { output_file << " " << j << ":" << hdvs[i][j]; }
        }
        output_file << " #" << i << "\n";
    }
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Counter functions //////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void hypercounter::global_counter(const int nb_thread, const int nb_batches)
{
    cerr << "Starting counter..." << "\n";
    size_t N = h.get_nb_nodes();

    std::vector<int> range(N);
    for (int i=0;i<N;++i) range[i] = i;
    std::random_shuffle(range.begin(),range.end());

    omp_set_dynamic(0);
    omp_set_num_threads(nb_thread);
    size_t block_size = ceil(N/float(nb_batches));
    double t = omp_get_wtime();

    #pragma omp parallel for
    for (size_t i = 0; i < nb_batches; ++i)
    {
       for (size_t j = i*block_size; j< min((i+1)*block_size,N);++j)
       {
           int jj = range[j];
           counter(jj);
       }
       cerr << "Block " <<i<<"/"<<nb_batches<<" ("<< block_size<<" nodes) processed in " << (double)omp_get_wtime() - t << " seconds...\n";
    }
    cout << "Count completed in " << ((double)omp_get_wtime()- t)<< " seconds.\n";
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void hypercounter::counter(const int n)
{
    hdvs[n].resize(6369);

    std::vector<bool> nodes_visited(h.get_nb_nodes(), false);
    nodes_visited[n] = true;

    int l_n = nodes_hedges[n].size();
    hdvs[n][0] += l_n; // Count of orbit 0

    for (set<int>::iterator iter = node_neighbours[n].begin(); iter != node_neighbours[n].end(); ++iter)
    {
        int i = *iter;
        nodes_visited[i] = true;

        // Process pair n,i ////////////////////////////////////////////////////////////////////////////
        int m = max(nodes_hedges[n].size(),nodes_hedges[i].size());
        std::vector<int> ni;
        std::set_intersection(nodes_hedges[n].begin(),nodes_hedges[n].end(),nodes_hedges[i].begin(),nodes_hedges[i].end(),std::back_inserter(ni));
        int l_ni = ni.size();

        l_n = nodes_hedges[n].size()-l_ni;
        int l_i = nodes_hedges[i].size() - l_ni;

        std::vector<int> configuration = {l_ni,l_n,l_i};
        int count = 1, config = 0, l=configuration.size();
        for (int ind = 0; ind != l; ++ind)
        {
            if (configuration[ind] != 0) {count *= configuration[ind]; config += 1 << l-1-ind;}
        }

        int orbit = config_orbit_map[1][config];
        if (orbit != 0) hdvs[n][orbit] += 1;
        // End process pair n,i ////////////////////////////////////////////////////////////////////////

        std::vector<bool> nodes_visited_ext(nodes_visited);

        std::vector<int> ni_neighbourhood;
        std::set_union(iter,node_neighbours[n].end(),node_neighbours[i].begin(),node_neighbours[i].end(),std::back_inserter(ni_neighbourhood));

        // Iterate through third nodes
        for ( vector<int>::iterator jt = ni_neighbourhood.begin(); jt != ni_neighbourhood.end(); ++jt)
        {
            int j = *jt;

            if (nodes_visited_ext[j]) continue;
            else nodes_visited_ext[j] = true;

            // Start process triplets n, i, and j ///////////////////////////////////////////////////////////

            // n,j pair
            m = max(nodes_hedges[n].size(),nodes_hedges[j].size()); vector<int> nj;
            std::set_intersection(nodes_hedges[n].begin(),nodes_hedges[n].end(),nodes_hedges[j].begin(),nodes_hedges[j].end(),std::back_inserter(nj));

            // i,j pair
            m = max(nodes_hedges[i].size(),nodes_hedges[j].size()); vector<int> ij;
            std::set_intersection(nodes_hedges[i].begin(),nodes_hedges[i].end(),nodes_hedges[j].begin(),nodes_hedges[j].end(),std::back_inserter(ij));

            // n,i,j triplet
            m = max(ni.size(),nj.size()); vector<int> nij;
            std::set_intersection(ni.begin(),ni.end(),nj.begin(),nj.end(),std::back_inserter(nij));
            int l_nij = nij.size();

            l_ni = ni.size() - l_nij;
            int l_nj = nj.size() - l_nij;
            int l_ij = ij.size() - l_nij;

            l_n = nodes_hedges[n].size() - l_ni - l_nj - l_nij;
            l_i = nodes_hedges[i].size() - l_ni - l_ij - l_nij;
            int l_j = nodes_hedges[j].size() - l_nj - l_ij - l_nij ;

            configuration = {l_nij,l_ni,l_nj,l_ij,l_n,l_i,l_j};
            count = 1; config = 0; l=configuration.size();
            for (int ind = 0; ind != l; ++ind)
            {
                if (configuration[ind] != 0) {count *= configuration[ind]; config += 1  << l-1-ind;}
            }
            orbit = config_orbit_map[2][config];
            if (orbit != 0) hdvs[n][orbit] += 1;
            // End process triplets n, i, and j /////////////////////////////////////////////////////////////////

            std::vector<int> nij_neighbourhood; // Union of n, i, and j neighbourhoods
            std::set_union(jt,ni_neighbourhood.end(),node_neighbours[j].begin(),node_neighbours[j].end(),std::back_inserter(nij_neighbourhood));

            for ( vector<int>::iterator kt = nij_neighbourhood.begin(); kt != nij_neighbourhood.end(); ++kt)
            {

                int k = *kt;

                if (nodes_visited_ext[k]) continue;
                // Start process quadruplet n, i, j, and k /////////////////////////////////////////////////////////////

                // n,k pair
                m = max(nodes_hedges[n].size(),nodes_hedges[k].size()); vector<int> nk;
                std::set_intersection(nodes_hedges[n].begin(),nodes_hedges[n].end(),nodes_hedges[k].begin(),nodes_hedges[k].end(),std::back_inserter(nk));

                // i,k pair
                m = max(nodes_hedges[i].size(),nodes_hedges[k].size()); vector<int> ik;
                std::set_intersection(nodes_hedges[i].begin(),nodes_hedges[i].end(),nodes_hedges[k].begin(),nodes_hedges[k].end(),std::back_inserter(ik));

                // j,k pair
                m = max(nodes_hedges[j].size(),nodes_hedges[k].size()); vector<int> jk;
                std::set_intersection(nodes_hedges[j].begin(),nodes_hedges[j].end(),nodes_hedges[k].begin(),nodes_hedges[k].end(),std::back_inserter(jk));

                // n,i,k triplets
                m = max(ni.size(),ik.size()); vector<int> nik;
                std::set_intersection(ni.begin(),ni.end(),ik.begin(),ik.end(),std::back_inserter(nik));

                // n,j,k triplets
                m = max(nj.size(),jk.size()); vector<int> njk;
                std::set_intersection(nj.begin(),nj.end(),jk.begin(),jk.end(),std::back_inserter(njk));

                // i,j,k triplets
                m = max(ik.size(),jk.size()); vector<int> ijk;
                std::set_intersection(ik.begin(),ik.end(),jk.begin(),jk.end(),std::back_inserter(ijk));

                // n,i,j,k quadruplets
                m = max(nij.size(),nik.size()); vector<int> nijk;
                std::set_intersection(nij.begin(),nij.end(),nik.begin(),nik.end(),std::back_inserter(nijk));
                int l_nijk = nijk.size();

                l_nij = nij.size() - l_nijk;
                int l_nik = nik.size() - l_nijk;
                int l_njk = njk.size() - l_nijk;
                int l_ijk = ijk.size() - l_nijk;

                l_ni = ni.size() - l_nij - l_nik - l_nijk;
                l_nj = nj.size() - l_nij - l_njk - l_nijk;
                int l_nk = nk.size() - l_nik - l_njk - l_nijk;
                l_ij = ij.size() - l_nij - l_ijk - l_nijk;
                int l_ik = ik.size() - l_nik - l_ijk - l_nijk;
                int l_jk = jk.size() - l_njk - l_ijk - l_nijk;

                l_n = nodes_hedges[n].size() - l_ni - l_nj - l_nk - l_nij - l_nik - l_njk - l_nijk;
                l_i = nodes_hedges[i].size() - l_ni - l_ij - l_ik - l_nij - l_nik - l_ijk - l_nijk;
                l_j = nodes_hedges[j].size() - l_nj - l_ij - l_jk - l_nij - l_njk - l_ijk - l_nijk;
                int l_k = nodes_hedges[k].size() - l_nk - l_ik - l_jk - l_nik - l_njk - l_ijk - l_nijk;

                configuration = {l_nijk,l_nij,l_nik,l_njk,l_ijk,l_ni,l_nj,l_nk,l_ij,l_ik,l_jk,l_n,l_i,l_j,l_k};
                count = 1; config =0; l=configuration.size();
                for (int ind = 0; ind != l; ++ind)
                {
                    if (configuration[ind] != 0) {count *= configuration[ind]; config += 1 << l-1-ind;}
                }

                orbit = config_orbit_map[3][config];
                if (orbit != 0) {hdvs[n][orbit] += 1;}

                // End process quadruplet n, i, j, and k
            }
        }
    }
}

