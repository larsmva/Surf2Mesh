import os
import sys 
from dolfin import *
from mshr import *

def Facet_normals(v1,v2,v3):
	"""
	Usage : Computes the unit normal of a surface triangle 
		in case of writing a stl-file.

	======== =========================================
	Argument Explaination
	======== =========================================
	v1 	 Vector of the coordinates of vertex no1 
		 in surface triangle
	v2 	 Vector of the coordinates of vertex no2 
		 in surface triangle
	v3 	 Vector of the coordinates of vertex no3 
		 in surface triangle	
	"""
	vec1_x = v2[0]-v1[0]
	vec1_y = v2[1]-v1[1]
        vec1_z = v2[2]-v1[2]
        vec2_x = v3[0]-v1[0]
        vec2_y = v3[1]-v1[1]
        vec2_z = v3[2]-v1[2]
        n_i=vec1_y*vec2_z - vec1_z*vec2_y
        n_j=vec1_z*vec2_x - vec1_x*vec2_z
        n_k=vec1_x*vec2_y - vec1_y*vec2_x
        size =( n_i*n_i + n_j*n_j +n_k*n_k)**0.5
        return (n_i/size,n_j/size,n_k/size)

def Tuplemap(operation,string):
	"""
	Usage : Used to help convert asc surface files to off
		or stl format.
	========  =========================================
	Argument  Explaination
	========  =========================================
	operation An operation, which can be applied to a 
		  string, such as  float, int and so on.
	string    An string for which the operation will
		  be used on.	
	"""
	return tuple(map(operation,string.split()))[0:3]

def srf2off(filename, outputfile):
	"""
	Usage : Convert asc surface file to off-format file 
		
	========  =========================================
	Argument  Explaination
	========  =========================================
	filename  Path to asc surface file
		  
	Outputfie Path to the converted off file.   

	"""
	orig_stdout=sys.stdout
	data= open(filename).read().splitlines()
	f = file(outputfile,'w')
	sys.stdout=f
	print "OFF"
	(num_v,num_f)=map(int,data[1].split())
	print data[1]+" 0"
	for line in data[2:num_v+2]:
		print "%e %e %e"%Tuplemap(float,line)
	for line in data[num_v+2::]:
		print "3 %d %d %d"%Tuplemap(int,line)

	sys.stdout=orig_stdout	
	f.close()


def srf2stl(filename, outputfile):
	"""
	Usage : Convert asc surface file to stl-format file 
		to off 
	========  =========================================
	Argument  Explaination
	========  =========================================
	filename  Path to asc surface file
		  
	Outputfie Path to the converted stl file.   

	"""
	output= """facet normal %e %e %e
		outer loop
			vertex %e %e %e
			vertex %e %e %e
			vertex %e %e %e
		endloop   
		endfacet"""
	orig_stdout=sys.stdout
	data = open(filename).read().splitlines()
	f = file(outputfile,'w')
	sys.stdout=f
	(num_v,num_f)=map(int,data[1].split())

	print "solid %s"%filename
	for line in data[num_v+2::]:
		vertices = [int(i)+2 for i in line.split()[0:3]]
    		(v1,v2,v3)=[Tuplemap(float,data[i]) for i in vertices]
		normals=Facet_normals(v1,v2,v3)
		print output%(normals+v1+v2+v3)
	print "endsolid"                
	sys.stdout=orig_stdout		
	f.close()	
	

def check_file(filename):
	"""
	Usage : Check if the asc surface file has the right
		format.
	========  =========================================
	Argument  Explaination
	========  =========================================
	filename  Path to asc surface file 

	"""

	if not os.path.isfile(filename):
		print "File does not exsist"
		sys.exit(0)
	(path,extension)= os.path.splitext(filename)
	if extension==".asc" or extension==".srf":
		data = open(filename).read().splitlines()
	else :
		print "Error not supported file format"
		sys.exit(0)
	try:
		(num_v, num_f)=map(int,data[1].split())
		if len(data[3].split())!=4:
			print "Error 1"
			return False

		elif len(data[num_v+2].split())!=4:
			print "Error 2"
			return False

		elif len(data)!=(num_v+num_f+2):
			print "Error 3"
			return False
	except: 
		print "Error 0"
		return False

	return True


def make_adjacent_folder(path2folder,name):
	"""
	Usage : make adjacent folder to an specified folder.
		
	========      =========================================
	Argument       Explaination
	========      =========================================
	path2folder   Path to folder.
	name  	      Name of the adjacent folder.
	"""
	parent_path = path2folder.rsplit("/",1)[0]

	new_path= parent_path+"/"+name
	if not os.path.isdir(new_path):
	    os.mkdir(new_path)
		
	return new_path

def check_domain(path2file):
	"""
	Note: 
		Domain is not reference to CSGCGALDomain3D, but 
		to avoid similarities to binary surface files.
	Usage:
		Check if domain as correct extensions.
		
	========      =========================================
	Argument       Explaination
	========      =========================================
	path2file      Path to file
	"""
	if path2file.endswith(".off") or path2file.endswith(".stl"): 
		return True
	else :
		return False


