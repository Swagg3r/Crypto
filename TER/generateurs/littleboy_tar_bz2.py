#!/usr/bin/python
import sys, getopt, tarfile, shutil, subprocess

header="%!PS\n/courier\n20 selectfont\n0 0 moveto"
tail="showpage"
data=""

#argument 1 = taille du fichier compresse voulu en octet
#creation des donnees 
i = 0
size=int(sys.argv[1])
mod = size/1000
print(mod)
#optimisation selon la taille voulue
if mod <= 0.1 and mod >= 0.05:
	i = size * 500
if mod >= 0.5:
	i = size * 1000000
#initialisation
taillecomp = 0
tailledecomp = i
tmpcom = 0 
a = 0
#ouverture/creation du fichier - mode écriture
file = open("file","w")
#1er remplissage de 0
data =""
for c in range(i):
	data=data+"0"
file.write(data)
file.close()

#tant qu'on n'a pas la bonne taille voulue + 1
while taillecomp < size+2:
	file = open("file","a")
	data =""
	for b in range(a):
		data=data+"0"

	#ecriture des donnees
	file.write(data)
	file.close()

	#a = nombre de 0 a ajouter à chaque itération
	a = 2000000

	#compression du fichier
	tar = tarfile.open("file.tar.bz2", "w:bz2")
	for name in ["file"]:
	    tar.add(name)
	tar.close()

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.bz2", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	print(taillecomp)
	tailledecomp = tailledecomp + a 
	print(tailledecomp)

tailledecomp = tailledecomp - a
#tant qu'on ne trouve pas le max du fichier decompresse


while taillecomp != size and taillecomp > size - 3:
	with open("file", 'a+') as f:
		#position à la fin du fichier
	    f.seek(0,2)
	    pos=f.tell()
	    if size > 34:
	    	#enlever 100 zeros de la fin
	    	f.truncate(pos-100) 
	    	tailledecomp = tailledecomp - 100
	    elif size < 34:
	    	#enlever 1 zeros de la fin
	    	f.truncate(pos-1)
	    	tailledecomp = tailledecomp - 1
	f.close()

	#compression du fichier
	tar = tarfile.open("file.tar.bz2", "w:bz2")
	for name in ["file"]:
	    tar.add(name)
	tar.close()


	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.bz2", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	print(taillecomp)
	print(tailledecomp)
	print("_____")
