import sys
import os
import argparse
from Extmesh_utility import *

#Note: NEED finishing touch regarding parser

def asc2domain(IN,OUT=""): # Change parameter names
	"""
	Usage : Convert asc surface file to stl-format file 
		or off-format
		
	========      =========================================
	Argument       Explaination
	========      =========================================
	IN            Path to folder.
	OUT  	      Name of the adjacent folder.
	"""
	if check_file(IN):

		if OUT=="":
			(path,extension)= os.path.splitext(IN)
			outpath=path+".off"
		else :
			outpath = OUT
		
		
		if outpath.endswith(".off"):
			srf2off(IN,outpath)
		elif outpath.endswith(".stl"):
			srf2stl(IN,outpath)
		else :
			raise TypeError("Error, unknown outputfile extension")
	 

if __name__=='__main__':
	
	parser = argparse.ArgumentParser(prog='asc2domain.py')
	parser.add_argument('--i', nargs='?', help='path to inputfile with extension .asc or .srf')
	parser.add_argument('--o',nargs='?',default="", help='path to outputfile with extension .off or .stl')
	Z = parser.parse_args()

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(0)

	asc2domain(Z.i,Z.o)




