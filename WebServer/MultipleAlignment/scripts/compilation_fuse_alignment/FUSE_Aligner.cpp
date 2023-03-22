//============================================================================
// Name        :
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#define NDEBUG

#include "FUSE_Aligner.h"

#include "SQ_Matrix.h"



/**
 * Defining the various types
 */

typedef MNA_SBM_T< SQ_Matrix >	Worker_T;



int main(int argc, char** argv) {
	int status;
	Worker_T slave;
	status = slave.work(argc, argv);

	return(status);
};
