/*
 * H-Clustering.h
 *
 *  Created on: 14 Apr 2014
 *      Author: nmaloddo
 */

#include<set>
#include<map>

#define my_INFINITY 1000000.

using namespace std;

template <class Matrix_T> class H_Clustering{
private:
	Matrix_T & Similarity_Matrix;
	int nb_node;

	set<set<int> > clusters;
	/** Cluster are sorted by decreasing sum of similarity */
	multimap<double, set<int>, std::greater<double> > sorted_clusters;

	/** the hierarchical classification*/
	vector< pair<int,int> > hierarchical_clustering;

	/** compute the sum of similarity between all pairs of node from a cluster */
	double cluster_similarity(const set<int> & s1){
		double sim(0);
		int ind1, ind2;
		//vector<int> linear_set;
		//std::copy(s1.begin(), s1.end(), std::back_inserter(linear_set));

			for(set<int>::iterator s1it(s1.begin()); s1it != s1.end(); ++s1it){
			ind1 = *s1it;
			set<int>::iterator s2it(s1it);
			++s2it;
			for(; s2it != s1.end(); ++s2it){
				ind2 = *s2it;
				sim += Similarity_Matrix.get(ind1,ind2);
			}
		}
		/*
		for(int ind1(0); ind1 < linear_set.size(); ++ind1){
			for(int ind2(ind1+1); ind2 < linear_set.size(); ++ind2){
				sim += Similarity_Matrix.get(ind1,ind2);
			}
		}
		*/
		return(sim);
	};

	void Sort_Clusters(set<set<int> > & clusters){
		sorted_clusters.clear();
		typedef set<set<int> >::iterator ssit;
		for(ssit it(clusters.begin());it!=clusters.end();++it){
			sorted_clusters.insert( pair<double, set<int> >( cluster_similarity(*it),*it )   );
		}
	};


	/** compute the average similarity between all pairs of node from the two input sets */
	double avg_similarity(const set<int> & s1, const set<int> & s2){
		double sim(0);
		int ind1, ind2, net1, net2;
		for(set<int>::iterator s1it(s1.begin()); s1it != s1.end(); ++s1it){
			ind1 = *s1it;
			for(set<int>::iterator s2it(s2.begin()); s2it != s2.end(); ++s2it){
				ind2 = *s2it;
				//we do not allow merging set containing nodes from the same networks
				sim += Similarity_Matrix.get(ind1,ind2);
			}
		}
		return(sim/((float)(s1.size() * s2.size())));
	};

	/** compute the minimum similarity between all pairs of node from the two input sets */
	double min_similarity(set<int> & s1, set<int> & s2){
		double smin(INFINITY), sim;
		int ind1, ind2, net1, net2;
		for(set<int>::iterator s1it(s1.begin()); s1it != s1.end(); ++s1it){
			ind1 = *s1it;
			for(set<int>::iterator s2it(s2.begin()); s2it != s2.end(); ++s2it){
				ind2 = *s2it;
				sim = Similarity_Matrix.get(ind1,ind2);
				if(sim<smin){	smin = sim;}
		}}
		return(smin);
	};

	/** compute the maximum similarity between all pairs of node from the two input sets */
	double max_similarity(set<int> & s1, set<int> & s2){
		double smax(-INFINITY), sim;
		int ind1, ind2, net1, net2;
		for(set<int>::iterator s1it(s1.begin()); s1it != s1.end(); ++s1it){
			ind1 = *s1it;
			for(set<int>::iterator s2it(s2.begin()); s2it != s2.end(); ++s2it){
				ind2 = *s2it;
				sim = Similarity_Matrix.get(ind1,ind2);
				if(sim>smax){	smax = sim;}
		}}
		return(smax);
	};

public:
	/** Constructor */
	H_Clustering(Matrix_T & p_Similarity_Matrix, int k):
		Similarity_Matrix(p_Similarity_Matrix),
		nb_node(k)
	{
		;
	};

	/** Hierarchical clustering, using UPGMA strategy  */
	void UPGMA_Clustering()
	{
		//initialise clusters
		clusters.clear();
		for(int node(0); node< nb_node; ++node){
			set<int> local;
			local.insert(node);
			clusters.insert(local);
		}

		hierarchical_clustering.clear();

		//cluster are selected based on average similarity
		while(clusters.size()>1){
			set< set<int> >::iterator best_i, best_j;
			double max_avg_dist(-my_INFINITY), local_avg;

			// find best sets i and j
			for(set<set<int> >::iterator si(clusters.begin()); si!= clusters.end(); ++si){
				set<set<int> >::iterator sj = si;
				++sj;
				for(; sj!= clusters.end(); ++sj){
					local_avg = avg_similarity((*si), (*sj));
					if(local_avg > max_avg_dist){
						max_avg_dist = local_avg;
						best_i = si;
						best_j = sj;
			}}}

			// merge sets i and j
			int set1_ind( *(best_i->begin()) );
			int set2_ind( *(best_j->begin()) );
			set<int> new_cluster;
			new_cluster.insert(best_i->begin(), best_i->end());
			new_cluster.insert(best_j->begin(), best_j->end());
			clusters.erase(best_i);
			clusters.erase(best_j);
			clusters.insert(new_cluster);

			//add merge sequence

			if (set1_ind > set2_ind){
				int tmp = set2_ind;
				set2_ind = set1_ind;
				set1_ind = tmp;
			}
			hierarchical_clustering.push_back( pair<int,int>(set1_ind, set2_ind) );

		}
		//cout << "-  Sorting clusters\n";
		//Sort cluster by weights
		//Sort_Clusters(clusters);
		//cout << "-  End of Clustering\n";
	};

	/**   */
	//void Single_Linkage_Clustering( set<set<int> > & clusters)
	//{
		//initialise clusters

		//cluster are selected based on maximum similarity
	//};

	/**  */
	//void Complete_Linkage_Clustering( set<set<int> > & clusters)
	//{
		//initialise clusters

		//cluster are selected based on minimum similarity
	//};

	vector< pair<int,int> > & get_h_clustering(){ return(hierarchical_clustering); };

	multimap<double, set<int>, std::greater<double> > & get_clustering(){
		return(sorted_clusters);
	};
};
