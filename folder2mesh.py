import os
import sys 
from dolfin import *
from mshr import *
from Extmesh_utility import *

import asc2domain 
import domain2mesh
import mesh2xdmf 
def folder2mesh(path2folder):

	if not os.path.isdir(path2folder): return None

	off	   = make_adjacent_folder(path2folder,"Surface3D")
	meshfolder = make_adjacent_folder(path2folder,"Mesh")
	vtk       = make_adjacent_folder(path2folder,"Vtk")

	for i in os.listdir(path2folder):
		name = str(i).split(".")[0]
		asc2domain.asc2domain(path2folder+"/"+i,off+"/"+name+".off") 
	
	for i in os.listdir(off):
		name = str(i).split(".")[0]
		domain2mesh.domain2mesh(off+"/"+i,meshfolder+"/"+name+".xml.gz")
	
	for i in os.listdir(meshfolder):
		name = str(i).split(".")[0]
		print i
		mesh2xdmf.mesh2xdmf(meshfolder+"/"+i,vtk+"/"+name)

if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser(prog='folder2mesh.py')
	parser.add_argument('--i', nargs='?', help='path to folder')

	Z =parser.parse_args()
	
	folder2mesh(Z.i)
	
	

	

