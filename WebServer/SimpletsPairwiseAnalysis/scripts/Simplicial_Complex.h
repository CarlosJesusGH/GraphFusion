//============================================================================
// Name        : Simplicial_Complex.h
// Author      : NMD
// Version     :
// Copyright   : Your copyright notice
// Description : A simple simplicial complex class
//============================================================================

#include<string>
#include<set>
#include<vector>
#include<map>

#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<algorithm>

int fact(long long int N){
	//if(N==0) return 1;
	if(N>0) return N*fact(N-1);
	else return 1;
};

int NcR(long long int N, long long int R){
	if(N<R) return 0;
	return(fact(N)/(fact(R)*fact(N-R)));
}


bool check_SDV(std::vector<long long int> sdv){
	bool eq1( NcR(sdv[0], 2) == (sdv[1]+sdv[3]+sdv[4]) );
	//std::cout << (NcR(sdv[1], 1)*NcR(sdv[0]-2,1)) << ", " << (3*sdv[8]+2*sdv[10]+2*sdv[13]+sdv[17]+sdv[19]+sdv[22]);
	bool eq2( (NcR(sdv[1], 1)*NcR(sdv[0]-2,1)) == (3*sdv[8]+2*sdv[10]+2*sdv[13]+sdv[17]+sdv[19]+sdv[22]) );
	bool eq3( (NcR(sdv[2], 1)*NcR(sdv[0]-1,1)) == (sdv[6]+2*sdv[15]+sdv[11]+sdv[14]+2*sdv[16]+2*sdv[18]+2*sdv[20]+2*sdv[21]) );
	bool eq4( (NcR(sdv[3], 1)*NcR(sdv[0]-2,1)) == (sdv[10]+2*sdv[17]+1*sdv[19]+3*sdv[23]+2*sdv[24]+3*sdv[25]+1*sdv[26]+2*sdv[27]+1*sdv[28]) );
	bool eq5( (NcR(sdv[4], 1)*NcR(sdv[0]-2,1)) == (sdv[13]+1*sdv[19]+2*sdv[22]+1*sdv[24]+2*sdv[26]+1*sdv[27]+2*sdv[28]+3*sdv[29]+3*sdv[30] + 3*sdv[31]) );
	//std::cout << " -- "<< (NcR(sdv[4], 1)*NcR(sdv[0]-2,1)) << ", " << (sdv[13]+1*sdv[19]+2*sdv[22]+1*sdv[24]+2*sdv[26]+1*sdv[27]+2*sdv[28]+3*sdv[29]+3*sdv[30] + 3*sdv[31]) << " -- ";
	bool eq6( NcR(sdv[0], 3) == (sdv[8]+sdv[10]+sdv[13]+sdv[17]+sdv[19]+sdv[22]+sdv[23]+sdv[24]+sdv[25]+sdv[26]+sdv[27]+sdv[28]+sdv[29]+sdv[30]+sdv[31]) );
	return(eq1 && eq2 && eq3 && eq4 && eq6);
}

class face_1D {
public:
	int first;
	int second;

	face_1D(int a, int b){
		std::vector<int>sorter;
		sorter.push_back(a);
		sorter.push_back(b);
		std::sort(sorter.begin(), sorter.end());
		first = sorter[0];
		second = sorter[1];
	};

	const bool operator < ( const face_1D &T ) const{
		if(first < T.first){
			return true;
		}
		else if ((first == T.first) && (second < T.second)){
			return true;
		}
		else{ return false;}
	};
};

class face_2D {
public:
	int first;
	int second;
	int third;

	face_2D(int a, int b, int c){
		std::vector<int>sorter;
		sorter.push_back(a);
		sorter.push_back(b);
		sorter.push_back(c);
		std::sort(sorter.begin(), sorter.end());
		first = sorter[0];
		second = sorter[1];
		third = sorter[2];
	};

	const bool operator < ( const face_2D &T ) const{
		if(first < T.first){
			return true;
		}
		else if ((first == T.first) && (second < T.second)){
			return true;
		}
		else if ((first == T.first) && (second == T.second) && (third < T.third)){
			return true;
		}
		else{ return false;}
	};
};

class face_3D {
public:
	int first;
	int second;
	int third;
	int fourth;

	face_3D(int a, int b, int c, int d){
		std::vector<int>sorter;
		sorter.push_back(a);
		sorter.push_back(b);
		sorter.push_back(c);
		sorter.push_back(d);
		std::sort(sorter.begin(), sorter.end());
		first = sorter[0];
		second = sorter[1];
		third = sorter[2];
		fourth = sorter[3];
	};

	const bool operator < ( const face_3D &T ) const{
		if(first < T.first){
			return true;
		}
		else if ((first == T.first) && (second < T.second)){
			return true;
		}
		else if ((first == T.first) && (second == T.second) && (third < T.third)){
			return true;
		}
		else if ((first == T.first) && (second == T.second) && (third == T.third) && (fourth < T.fourth)){
			return true;
		}
		else{ return false;}
	};
};

std::ostream& operator << (std::ostream& os, const face_1D& f){
	os << "(" << f.first << "," << f.second <<")";
	return os;
};

std::ostream& operator << (std::ostream& os, const face_2D& f){
	os << "(" << f.first << "," << f.second << "," << f.third <<")";
	return os;
};

std::ostream& operator << (std::ostream& os, const face_3D& f){
	os << "(" << f.first << "," << f.second << "," << f.third << "," << f.fourth <<")";
	return os;
};




class Simplicial_Complex {

	typedef std::set<int> face;
	typedef std::vector<std::vector<bool> > binary_matrix;

private:
	/** Vertex set */
	std::vector<std::string> V;
	std::map<std::string, int> V_to_Ind;

	/** Set of faces */
	std::vector<face> Sigma;
	std::set<face_1D> S_1D;
	std::set<face_2D> S_2D;
	std::set<face_3D> S_3D;


	/** Adjacency matrix */
	binary_matrix adjacency_matrix;

	/** Neighbours */
	std::vector<std::vector<int> > neighbours;

public:
	int nb_vertices;
	int nb_faces;
	int dimension;

	/** Constructor; read a face list file. */
	Simplicial_Complex(std::string filename)
	{
		//empty simplicial complex
		nb_vertices = 0;
		nb_faces = 0;
		dimension = 0;

		//opening file
		std::ifstream face_file;
		face_file.open(filename.c_str());

		//parsing file
		std::string line;
		std::string vertex;
		while(std::getline(face_file, line)){
			face new_face;
			std::istringstream iss(line);
			while(iss >> vertex){
				int vind = 0;
				std::map<std::string, int>::iterator my_it(V_to_Ind.find(vertex));
				if(my_it != V_to_Ind.end()){
					vind = my_it->second;
				}
				else{
					vind = nb_vertices;
					nb_vertices++;
					V_to_Ind.insert(std::pair<std::string, int>(vertex,vind));
					V.push_back(vertex);
				}
				new_face.insert(vind);
			}
			Sigma.push_back(new_face);
			if(new_face.size() > dimension){
				dimension = new_face.size();
			}
			nb_faces++;
		}
		face_file.close();
		std::cout << "input list: " << nb_vertices << " vertices, " << nb_faces << " faces, dimension = "<< dimension <<"\n";

		/**
		 * generating 3D skeleton required for 2- to 4-nodes simplets
		 */

		std::cout << "Generating 3D skeleton:\n";
		for(int i(0);i<nb_faces; ++i){
			face f(Sigma[i]);
			std::vector<int> ff(f.begin(),f.end());

			// generating all 1-3-D faces from f
			for(int i(0); i<ff.size(); ++i){
				int a(ff[i]);
				for(int j(i+1); j<ff.size(); ++j){
					int b(ff[j]);
					S_1D.insert(face_1D(a, b));
					for(int k(j+1); k<ff.size(); ++k){
						int c(ff[k]);
						S_2D.insert(face_2D(a, b, c));
						for(int l(k+1); l<ff.size(); ++l){
							int d(ff[l]);
							S_3D.insert(face_3D(a, b, c, d));
						}
					}
				}
			}
		}
		std::cout << "-- 1D-faces: " << S_1D.size() << std::endl;
		//for(std::set<face_1D>::iterator myid(S_1D.begin()); myid != S_1D.end(); ++myid)
		//{
		//	std::cout << "---- " << *myid << std::endl;
		//}
		std::cout << "-- 2D-faces: " << S_2D.size() << std::endl;
		//for(std::set<face_2D>::iterator myid(S_2D.begin()); myid != S_2D.end(); ++myid)
		//{
		//	std::cout << "---- " << *myid << std::endl;
		//}
		std::cout << "-- 3D-faces: " << S_3D.size() << std::endl;
		//for(std::set<face_3D>::iterator myid(S_3D.begin()); myid != S_3D.end(); ++myid)
		//{
		//	std::cout << "---- " << *myid << std::endl;
		//}

		/**
		 * Setting up adjacency and neighbourhood
		 */
		adjacency_matrix.clear();
		adjacency_matrix.resize(nb_vertices);
		for(int i(0); i<nb_vertices; ++i){
			adjacency_matrix[i].clear();
			adjacency_matrix[i].resize(nb_vertices, false);
		}

		neighbours.clear();
		neighbours.resize(nb_vertices);
		for(int i(0); i<nb_vertices; ++i){
			neighbours[i].clear();
		}
		for(std::set<face_1D>::iterator myid(S_1D.begin()); myid != S_1D.end(); ++myid)
		{
			int a(myid->first);
			int b(myid->second);
			adjacency_matrix[a][b]=true;
			adjacency_matrix[b][a]=true;
			neighbours[a].push_back(b);
			neighbours[b].push_back(a);
		}
	};


	void count(std::string outputfname){
		std::vector<std::vector<long long int> > SDV;
		SDV.resize(nb_vertices);
		for(int i(0); i<nb_vertices; ++i){
			SDV[i].clear();
			SDV[i].resize(32, 0);
		}

		for(int a(0); a<nb_vertices; ++a){
			if(a%100 == 1){
				std::cout << "Processing node " << a << " / " << nb_vertices << std::endl;
			}
			//S1, orbit 1 (0)
			int a_01(neighbours[a].size());
			SDV[a][0] = a_01;

			//S2, S3, S4, orbit 2 to 5 (1-4)
			for(int ind_b(0); ind_b < a_01; ++ind_b){
				int b(neighbours[a][ind_b]);
				for(int ind_c(ind_b+1); ind_c < a_01; ++ind_c){
					int c(neighbours[a][ind_c]);
					face_2D abc(a,b,c);
					if(S_2D.find(abc) != S_2D.end()){
						//orbit 5 (4)
						SDV[a][4] += 1;
						SDV[b][4] += 1;
						SDV[c][4] += 1;
					}
					else if(adjacency_matrix[b][c]){
						//orbit 4 (3)
						SDV[a][3] += 1;
						SDV[b][3] += 1;
						SDV[c][3] += 1;
					}
					else{
						//orbit 2 (1) and 3 (2)
						SDV[a][1] += 1;
						SDV[b][2] += 1;
						SDV[c][2] += 1;
					}
				}
			}
			//S5, orbit 6 and 7 (5-6)
			for(int ind_b(0); ind_b < a_01; ++ind_b){
				int b(neighbours[a][ind_b]);
				int b_01(neighbours[b].size());
				for(int ind_c(0); ind_c < b_01; ++ind_c){
					int c(neighbours[b][ind_c]);
					if((!adjacency_matrix[a][c]) && (a!=c)){
						int c_01(neighbours[c].size());
						for(int ind_d(0); ind_d < c_01; ++ind_d){
							int d(neighbours[c][ind_d]);
							if((!adjacency_matrix[a][d]) && (!adjacency_matrix[b][d]) && (a!=d) && (b!=d)){
								//orbit 6 (5) and 7 (6)
								SDV[a][5] += 1;
								SDV[b][6] += 1;
								SDV[c][6] += 1;
								SDV[d][5] += 1;
							}
						}
					}
				}
			}
			//S6, S7 and S8, orbits 8-15 (7-14)
			for(int ind_b(0); ind_b < a_01; ++ind_b){
				int b(neighbours[a][ind_b]);
				int b_01(neighbours[b].size());
				for(int ind_c(0); ind_c < b_01; ++ind_c){
					int c(neighbours[b][ind_c]);
					if((!adjacency_matrix[a][c]) && (a!=c)){
						for(int ind_d(ind_c+1); ind_d < b_01; ++ind_d){
							int d(neighbours[b][ind_d]);
							if((!adjacency_matrix[a][d]) && (a!=d)){
								face_2D bcd(b,c,d);
								if(S_2D.find(bcd) != S_2D.end()){
									//orbit 13-15 (12-14)
									SDV[a][12] += 1;
									SDV[b][13] += 1;
									SDV[c][14] += 1;
									SDV[d][14] += 1;
								}
								else if(adjacency_matrix[c][d]){
									//orbit 10-12 (9-11)
									SDV[a][9] += 1;
									SDV[b][10] += 1;
									SDV[c][11] += 1;
									SDV[d][11] += 1;
								}
								else{
									//orbit 8-9 (7-8)
									SDV[a][7] += 1;
									SDV[b][8] += 1;
									SDV[c][7] += 1;
									SDV[d][7] += 1;
								}
							}
						}
					}
				}
			}
			//S9, S10, S11 and S12, orbit 16-23 (15-22)
			for(int ind_b(0); ind_b < a_01; ++ind_b){
				int b(neighbours[a][ind_b]);
				int b_01(neighbours[b].size());
				for(int ind_c(ind_b+1); ind_c < a_01; ++ind_c){
					int c(neighbours[a][ind_c]);
					for(int ind_d(0); ind_d < b_01; ++ind_d){
						int d(neighbours[b][ind_d]);
						if((adjacency_matrix[c][d]) && (!adjacency_matrix[a][d]) && (a!=d) && (c!=d)){
							if(!adjacency_matrix[b][c]){
								//S9, orbits 16 (15)
								SDV[a][15] += 1;
								SDV[b][15] += 1;
								SDV[c][15] += 1;
								SDV[d][15] += 1;
							}
							else{
								face_2D abc(a,b,c);
								face_2D bcd(b,c,d);
								bool is_abc(S_2D.find(abc) != S_2D.end());
								bool is_bcd(S_2D.find(bcd) != S_2D.end());
								if((!is_abc) && (!is_bcd)){
									//S10, orbit 17-18 (16-17)
									SDV[a][16] += 1;
									SDV[b][17] += 1;
									SDV[c][17] += 1;
									SDV[d][16] += 1;
								}
								else if(is_abc && (!is_bcd)){
									//S11, orbit 19-21 (18-20)
									SDV[a][18] += 1;
									SDV[b][19] += 1;
									SDV[c][19] += 1;
									SDV[d][20] += 1;
								}
								else if(is_abc && is_bcd){
									//S12, orbit 22-23 (21-22)
									SDV[a][21] += 1;
									SDV[b][22] += 1;
									SDV[c][22] += 1;
									SDV[d][21] += 1;
								}
							}
						}
					}
				}
			}
			//S13 to S17, orbits 24-31 (23-30)
			for(int ind_b(0); ind_b < a_01; ++ind_b){
				int b(neighbours[a][ind_b]);
				int b_01(neighbours[b].size());
				for(int ind_c(0); ind_c < b_01; ++ind_c){
					int c(neighbours[b][ind_c]);
					if( (adjacency_matrix[a][c]) && (c!=a)){
						int c_01(neighbours[c].size());
						for(int ind_d(0); ind_d < c_01; ++ind_d){
							int d(neighbours[c][ind_d]);
							if((adjacency_matrix[a][d]) && (adjacency_matrix[b][d]) && (a!=d) && (b!=d)){
								face_2D abc(a,b,c);
								face_2D abd(a,b,d);
								face_2D acd(a,c,d);
								face_2D bcd(b,c,d);
								bool is_abc(S_2D.find(abc) != S_2D.end());
								bool is_abd(S_2D.find(abd) != S_2D.end());
								bool is_acd(S_2D.find(acd) != S_2D.end());
								bool is_bcd(S_2D.find(bcd) != S_2D.end());
								if( !is_abc && !is_abd && !is_acd && !is_bcd){
									//S13, orbit 24 (23)
									SDV[a][23] += 1;
									SDV[b][23] += 1;
									SDV[c][23] += 1;
									SDV[d][23] += 1;
								}
								else if(is_abc && !is_abd && !is_acd && !is_bcd){
									//S14, orbit 25-26 (24-25)
									SDV[a][24] += 1;
									SDV[b][24] += 1;
									SDV[c][24] += 1;
									SDV[d][25] += 1;
								}
								else if(is_abc && is_abd && !is_acd && !is_bcd){
									//S15, orbit 27-28 (26-27)
									SDV[a][26] += 1;
									SDV[b][26] += 1;
									SDV[c][27] += 1;
									SDV[d][27] += 1;
								}
								else if(is_abc && is_abd && is_acd && !is_bcd){
									//S16, orbit 29-30 (28-29)
									SDV[a][29] += 1;
									SDV[b][28] += 1;
									SDV[c][28] += 1;
									SDV[d][28] += 1;
								}
								else if(is_abc && is_abd && is_acd && is_bcd){
									face_3D abcd(a,b,c,d);
									if(S_3D.find(abcd) != S_3D.end()){
										//S18, orbit 32 (31)
										SDV[a][31] += 1;
										SDV[b][31] += 1;
										SDV[c][31] += 1;
										SDV[d][31] += 1;
									}
									else{
										//S17, orbit 31 (30)
										SDV[a][30] += 1;
										SDV[b][30] += 1;
										SDV[c][30] += 1;
										SDV[d][30] += 1;
									}
								}
							}
						}
					}
				}
			}
		}

		// Accounting for overcounts
		for(int a(0); a<nb_vertices; ++a){
			SDV[a][3] /= 3;
			SDV[a][4] /= 3;
			SDV[a][5] /= 2;
			SDV[a][6] /= 2;
			SDV[a][7] /= 3;
			SDV[a][8] /= 3;
			SDV[a][15] /= 4;
			SDV[a][16] /= 2;
			SDV[a][17] /= 2;
			SDV[a][21] /= 2;
			SDV[a][22] /= 2;
			SDV[a][23] /= 24;
			SDV[a][24] /= 6;
			SDV[a][25] /= 6;
			SDV[a][26] /= 4;
			SDV[a][27] /= 4;
			SDV[a][28] /= 6;
			SDV[a][29] /= 6;
			SDV[a][30] /= 24;
			SDV[a][31] /= 24;
		}
		//int error(0);
		//for(int a(0); a<nb_vertices; ++a){
		//	if(!check_SDV(SDV[a])){
		//		++error;
		//		std::cout << "---- Invalid SDV for vertex " << V[a] << std::endl;
		//	}
		//}
		//if(error == 0){
		//	std::cout << "---- SDVs are all valid\n";
		//}
		std::ofstream myfile(outputfname.c_str());
		for(int a(0); a<nb_vertices; ++a){
			myfile << V[a] << ";" << SDV[a][0];
			for(int i(1); i<32; ++i){
				myfile << ";" << SDV[a][i];
			}
			myfile << ";\n";
		}
		myfile.close();
	};
};
