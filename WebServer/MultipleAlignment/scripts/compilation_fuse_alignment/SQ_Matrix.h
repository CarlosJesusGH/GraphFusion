/*
 * SQ_Matrix.h
 *
 *  Created on: April 2014
 *  Author: N. Malod-Dognin
 */

#ifndef SQ_MATRIX_H_
#define SQ_MATRIX_H_

#include <vector>
#include <map>
#include <algorithm>

using namespace std;

/**
 * A sparse square matrix, useful when most entries are zero
 */
template <class K, class V> class SQ_Matrix {
public:
	typedef K Key_T;
	typedef V Value_T;
	typedef map<Key_T, map<Key_T, Value_T> > Matrix_T;
	typedef typename Matrix_T::iterator NZ_Row_Iterator;
	typedef typename map<Key_T, Value_T>::iterator NZ_Iterator;


	/** The 2D map that contains the linearised matrix */
	Matrix_T matrix;

	/** The number of non_zero row */
	size_t N;

	/** The number of non_zero entries */
	size_t NZ;


	/** First constructor: create a NxM matrix */
	inline SQ_Matrix():
		N(0), NZ(0)
	{
		;
	};

	/** Return the nb of non-zero rows */
	inline size_t get_NZ_row_size()			{	return(N);};

	/** Return the nb of non_zero entries of the matrix */
	inline size_t get_NZ_size()			{	return(NZ);};

	/** Return the nb of non_zero entries of in row K
	 * 	This is a O(log(N)) time operation
	 * */
	inline size_t get_NZ_size_of_row(Key_T key)
	{
		NZ_Row_Iterator row_it( matrix.find(key) );
		if(row_it == matrix.end()){
			return(0);
		}
		return(row_it->second.size());
	};

	/** Reset the values of the matrix to zero */
	inline void clear() 				{	matrix.clear();	};


	/** Set a given entry to the given value */
	inline void set(Key_T row, Key_T col, Value_T value)
	{
		if(value == 0){
			//this is a deletion operation
			//taking care of row-col
			NZ_Row_Iterator row_it( matrix.find(row) );
			if(row_it != matrix.end()){
				//there are some values in the row
				NZ_Iterator col_it( row_it->second.find(col) );
				if(col_it != row_it->second.end()){
					//row-col exist, now deleting it
					row_it->second.erase(col_it);
					NZ--;
				}
				//if row is now empty, deleting it
				if(row_it->second.empty()){
					matrix.erase(row_it);
					N--;
				}
			}
			//taking care of col-row
			row_it = matrix.find(col);
			if(row_it != matrix.end()){
				//there are some values in the row
				NZ_Iterator col_it( row_it->second.find(row) );
				if(col_it != row_it->second.end()){
					//row-col exist, now deleting it
					row_it->second.erase(col_it);
					NZ--;
				}
				//if row is now empty, deleting it
				if(row_it->second.empty()){
					matrix.erase(row_it);
					N--;
				}
			}
		}
		else{
			//First, update row-col
			//this is either an edition or a replacement operation
			NZ_Row_Iterator row_it( matrix.find(row) );
			if(row_it == matrix.end()){
				//row does not exist, insert it and insert value
				pair<NZ_Row_Iterator, bool> inserted(matrix.insert(pair<Key_T, map<Key_T,Value_T> >(row, map<Key_T, Value_T>())));
				row_it = inserted.first;
				N++;
			}
			NZ_Iterator col_it( row_it->second.find(col) );
			if(col_it == row_it->second.end()){
				//row exist, but does not have a value in the given column
				// so we insert the new value
				row_it->second[col] = value;
				NZ++;
			}
			else{
				//their is a value in row/col, we just update it
				col_it->second = value;
			}

			//Second, update col-row
			//this is either an edition or a replacement operation
			row_it = matrix.find(col);
			if(row_it == matrix.end()){
				//row does not exist, insert it and insert value
				pair<NZ_Row_Iterator, bool> inserted(matrix.insert(pair<Key_T, map<Key_T,Value_T> >(col, map<Key_T, Value_T>())));
				row_it = inserted.first;
				N++;
			}
			col_it = row_it->second.find(row);
			if(col_it == row_it->second.end()){
				//row exist, but does not have a value in the given column
				// so we insert the new value
				row_it->second[row] = value;
				NZ++;
			}
			else{
				//there is a value in col/row, we just update it
				col_it->second = value;
			}
		}
	};

	/** Get the value of the given entry
	 *  This is a O(2log(N)) time operation
	 * */
	inline Value_T get(Key_T row, Key_T col){
		NZ_Row_Iterator row_it( matrix.find(row) );
		if(row_it == matrix.end()){
			return(0);
		}
		NZ_Iterator col_it( row_it->second.find(col) );
		if(col_it == row_it->second.end()){
			return(0);
		}
		return(col_it->second);
	};

	/** Remove a row (equivalent to setting all its element to 0)
	 *  This is a O(k.log(N)) time operation, where k is the number of NZs in the row
	 * */
	inline void erase_row(Key_T row){
		NZ_Row_Iterator row_it( matrix.find(row) );
		if(row_it != matrix.end()){
			vector<Key_T> valid_col;
			valid_col.reserve(row_it->second.size());
			for(NZ_Iterator cols(row_it->second.begin()); cols != row_it->second.end(); ++cols){
				valid_col.push_back( cols->first );
			}
			for(typename vector<Key_T>::iterator col(valid_col.begin()); col!=valid_col.end();++col){
				this->set(row,*col,0);
			}
		}
	};

	/**
	 * Search for the best value in the matrix
	 * This is a O(NZ) time operation
	 */
	inline pair<pair<Key_T, Key_T>, Value_T> find_max(){
		Key_T best_row, best_col;
		Value_T best_value(0);
		for(NZ_Row_Iterator row_it( matrix.begin() ); row_it != matrix.end(); ++row_it){
			for(NZ_Iterator col_it(row_it->second.begin() ); col_it != row_it->second.end(); ++col_it){
				if(col_it->second>best_value){
					best_row = row_it->first;
					best_col = col_it->first;
					best_value = col_it->second;
				}
			}
		}
		return( pair<pair<Key_T, Key_T>, Value_T >( pair<Key_T,Key_T>(best_row, best_col), best_value)  );
	}




	inline NZ_Row_Iterator begin(){
		return matrix.begin();
	}

	inline NZ_Row_Iterator end(){
		return matrix.end();
	}

	inline NZ_Row_Iterator find_NZ_row(Key_T key){
		return matrix.find(key);
	}

	inline NZ_Iterator row_begin(Key_T row){
		return matrix[row].begin();
	}

	inline NZ_Iterator row_end(Key_T row){
		return matrix[row].end();
	}

	/** default destructor */
	inline ~SQ_Matrix() 		{;};


};










#endif /* SQ_MATRIX_H_ */
