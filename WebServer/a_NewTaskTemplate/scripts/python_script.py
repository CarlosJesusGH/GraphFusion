import os
import sys

# add path to sys if needed
# sys.path.append(os.path.join(sys.path[0], '../psb/scripts/')); # print("sys.path", sys.path)
# from ResultsAnalysis.enrichementAnalysis import *

# ---------------------------------------------------------------
# ADD FUNCTIONS

# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------
def main():
    print("flag: python main")
    print("os.getcwd()", os.getcwd())
    
    args = sys.argv[1:]
    print("args", args)

    

if __name__ == "__main__":
    main()


