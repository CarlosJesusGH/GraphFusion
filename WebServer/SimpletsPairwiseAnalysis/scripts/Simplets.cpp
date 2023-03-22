//============================================================================
// Name        : Simplets.cpp
// Author      : NMD
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include"Simplicial_Complex.h"
#include<string>
using namespace std;

int main(int argc, char**argv) {
	std::string ifname(argv[1]);
	std::string ofname(argv[2]);
	Simplicial_Complex S(ifname);
	S.count(ofname);
	return 0;
}
