###################################################################
# Change boost path to local installation to recompile
BOOSTPATH = cs/academic/phd3/gaudelet/libs/boost_1_61_0/stage/lib
###################################################################

CXX = g++
CXXFLAGS = -std=c++11 -O3 -fopenmp -L/$(BOOSTPATH) -static



all: run_hypercounter

string.o: string.h string.cpp

hypergraph.o: hypergraph.h hypergraph.cpp
	$(CXX) $(CXXFLAGS) -c hypergraph.cpp

hyperkernel.o: hypercounter.h hypercounter.cpp string.o
	$(CXX) $(CXXFLAGS) -c hyperkernel.cpp string.o

run_hypercounter: run_hypercounter.cpp hypercounter.o hypergraph.o string.o
	$(CXX) $(CXXFLAGS) $(LIBS) run_hypercounter.cpp hypercounter.o hypergraph.o string.o -o $@


clean:
	rm -rf run_hypercounter *.o *.*~ *~ core *.dSYM

