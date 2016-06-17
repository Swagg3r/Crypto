#!/usr/bin/python
import sys, getopt, subprocess

header="%!PS\n/courier\n20 selectfont\n0 0 moveto"
tail="showpage"
data=""

#argument 1 = taille du fichier compresse voulu en octet
#creation des donnees 
i = 0
size=int(sys.argv[1])
mod = size/1000
#optimisation selon la taille voulue
if mod >= 1:
	i = size * 5800
if mod >= 2:
	i = size * 6450
if mod >= 3:
	i = size * 6650
if mod >= 4:
	i = size * 6750
if mod >= 5:
	i = size * 6820
if mod >= 6:
	i = size * 6870
if mod >= 7:
	i = size * 6900
if mod >= 8:
	i = size * 6922
if mod >= 9:
	i = size * 6942
if mod >= 10:
	i = size * 7000
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
if size < 145 :
	subprocess.call("tar -caf file.tar.lz file", shell=True)
	sys.exit()
#tant qu'on n'a pas la bonne taille voulue + 2
while taillecomp < size+2:
	file = open("file","a")
	data =""
	for b in range(a):
		data=data+"0"

	#ecriture des donnees
	file.write(data)
	file.close()

	#a = nombre de 0 a ajouter a chaque iteration
	a = 4000

	#compression du fichier
	subprocess.call("tar -caf file.tar.lz file", shell=True)

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.lz", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	#print(taillecomp)
	tailledecomp = tailledecomp + a 
	#print(tailledecomp)

tailledecomp = tailledecomp - a
#tant qu'on ne trouve pas le max du fichier decompresse


while taillecomp != size and taillecomp > size - 3:
	with open("file", 'a+') as f:
		#position a la fin du fichier
	    f.seek(0,2)
	    pos=f.tell()
	    if size > 34:
	    	#enlever 100 zeros de la fin
	    	f.truncate(pos-500) 
	    	tailledecomp = tailledecomp - 500
	f.close()

	#compression du fichier
	subprocess.call("tar -caf file.tar.lz file", shell=True)

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.lz", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	#print(taillecomp)
	#print(tailledecomp)
	#print("_____")
