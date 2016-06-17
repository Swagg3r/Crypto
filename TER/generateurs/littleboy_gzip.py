#!/usr/bin/python
import sys, getopt, gzip, shutil, subprocess


header="%!PS\n/courier\n20 selectfont\n0 0 moveto"
tail="showpage"
data=""

#argument 1 = taille du fichier compresse voulu en octet
#creation des donnees 
i = 0
size=int(sys.argv[1])
mod = size/10000
#optimisation selon la taille voulue
if mod < 0.1 and mod > 0.01:
	i = size * 700
if mod >= 0.1:
	i = size * 999
if mod >= 1 :
 	i = size * 1025
if mod >= 2:
	i = size * 1026
if mod >= 3:
	i = size * 1027
if mod >= 4:
	i = size * 1028
if mod >= 8:
	i = size * 1028 + 30000
#initialisation
taillecomp = 0
tailledecomp = i
tmpcom = 0 
a = 0
#ouverture/creation du fichier - mode ecriture
file = open("file","w")
#1er remplissage de 0
data =""
for c in range(i):
	data=data+"0"
file.write(data)
file.close()
#cas particulier - si fichier compresse inferieur a 25 octets
if size <= 25:
	with open('file','rb') as f_in:
		with gzip.open('file.gz','wb') as f_out:
			shutil.copyfileobj(f_in,f_out)
	f_out.close()
	f_in.close()
	sys.exit()

#tant qu'on n'a pas la bonne taille voulue + 1
while taillecomp < size+1:
	file = open("file","a")
	data =""
	for b in range(a):
		data=data+"0"

	#ecriture des donnees
	file.write(data)
	file.close()

	#a = nombre de 0 a ajouter a chaque iteration
	a = 1000

	#compression du fichier
	with open('file','rb') as f_in:
		with gzip.open('file.gz','wb') as f_out:
			shutil.copyfileobj(f_in,f_out)
	f_out.close()
	f_in.close()

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.gz", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	#print(taillecomp)
	tailledecomp = tailledecomp + a 
	#print(tailledecomp)

tailledecomp = tailledecomp - a
#tant qu'on ne trouve pas le max du fichier decompresse
while taillecomp != size:
	with open("file", 'a+') as f:
		#position a la fin du fichier
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
	with open('file','rb') as f_in:
			with gzip.open('file.gz','wb') as f_out:
				shutil.copyfileobj(f_in,f_out)
	f_out.close()
	f_in.close()

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.gz", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	#print(taillecomp)
	#print(tailledecomp)
