import os
import sys 
from dolfin import *
from mshr import *
from Extmesh_utility import *



def domain2mesh(path2file,OUT):
	"""
	Note  : 
		Domain is not reference to CSGCGALDomain3D, but 
		to avoid similarities to binary surface files.
	
	Usage :
		Automatic transformation from surface file to 
		mesh. 
	
	"""
	if check_domain(path2file):
		#domain= CSGCGALDomain3D()
		#geometry= MeshGeometry()
		srf = Surface3D(path2file)
		domain =  CSGCGALDomain3D(srf)
		mesh= Mesh()
		generator = CSGCGALMeshGenerator3D()
		generator.generate(domain,mesh)

		
		if OUT.endswith(".hdf5"):	
			f = HDF5File(mesh.mpi_comm(), OUT, 'w')
			f.write(mesh, OUT)
		elif OUT.endswith(".xml.gz"):
			File(OUT) << mesh
		else: 
			raise TypeError("Error, unknown outputfile extension")
	


if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser(prog='hdf5 to vtk.py')
	parser.add_argument('--i', nargs='?', help='path to folder or file')
	parser.add_argument('--o', nargs='?', help='path to out to folder or file')	
	
	Z =parser.parse_args()

	domain2mesh(Z.i,Z.o)
	
	
	
