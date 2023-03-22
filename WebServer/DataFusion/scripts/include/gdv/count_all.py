#!/usr/bin/env python
"""
	The code to identify the graphlet signatures of all nodes in a network
	using the ORCA method.
	
	The script does the formatting of the given LEDA file to the format that 
	ORCA code can run. Then it reformats the output of the ORCA into ndump2 format.
	
	Run as:
		./count.py <LEDA_formatted_network>.gw
		
		Outputs: <LEDA_formatted_network>.ndump2 in the same folder with the input file
	
	Implemented by:
		Omer Nebil Yaveroglu
		05.11.2013 - 16:15
"""

import os
import sys
import os.path

indir = sys.argv[1]

# filelist = os.listdir(indir)
filelist = [sys.argv[2]]

for ifile in filelist:
	if ifile.split('.')[1]=='edgelist':
		if not os.path.isfile("%s/%s.ndump2"%(indir,ifile.split('.')[0])):
			print "\nProcessing ", ifile
			cmd = "python count.py %s/%s"%(indir,ifile)
			cmd = "python ../../scripts/include/gdv/count.py %s/%s"%(indir,ifile)
			os.system(cmd)
		else:
			print "Skipping %s"%(ifile)

