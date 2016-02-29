import os
import sys 
from dolfin import *
from mshr import *


def mesh2xdmf(path,out):
	"""
	Note : 
		Recursive code

	"""
	if  os.path.isdir(path):
		for i in os.listdir(path):
			mesh2xdmf(path+"/"+i)

	elif  os.path.isfile(path):
		if path.endswith(".hdf5"):
			mesh = Mesh()
			f = HDF5File(mpi_comm_world(),path, 'r')
			name = path.split(".")[0]
			f.read(mesh, name,False)
			V = FunctionSpace(mesh,"CG",1)
			u= Function(V)
		elif path.endswith(".xml.gz"):
			mesh =Mesh(path)
			V = FunctionSpace(mesh,"CG",1)
			u= Function(V)

		
		File(out+".xdmf") << u 
			
	else:
		return None

	


if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser(prog='hdf5 to vtk.py')
	parser.add_argument('--i', nargs='?', help='path to folder or file')

	Z =parser.parse_args()
	
	mesh2xdmf(Z.i)
	
