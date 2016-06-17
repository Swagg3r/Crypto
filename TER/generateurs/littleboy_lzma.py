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
	i = size * 5500
if mod >= 2:
	i = size * 6200
if mod >= 3:
	i = size * 6355
if mod >= 4:
	i = size * 6500
if mod >= 5:
	i = size * 6600
if mod >= 6:
	i = size * 6630
if mod >= 7:
	i = size * 6670
if mod >= 8:
	i = size * 6695
if mod >= 9:
	i = size * 6720
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
if size < 176 :
	subprocess.call("tar -caf file.tar.lzma file", shell=True)
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

	#a = nombre de 0 a ajouter à chaque itération
	a = 10000

	#compression du fichier
	subprocess.call("tar -caf file.tar.lzma file", shell=True)

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.lzma", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	#print(taillecomp)
	tailledecomp = tailledecomp + a 
	#print(tailledecomp)

tailledecomp = tailledecomp - a
#tant qu'on ne trouve pas le max du fichier decompresse


while taillecomp != size and taillecomp > size - 3:
	with open("file", 'a+') as f:
		#position à la fin du fichier
	    f.seek(0,2)
	    pos=f.tell()
	    if size >= 176:
	    	#enlever 100 zeros de la fin
	    	f.truncate(pos-1000) 
	    	tailledecomp = tailledecomp - 1000
	f.close()

	#compression du fichier
	subprocess.call("tar -caf file.tar.lzma file", shell=True)

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.lzma", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	#print(taillecomp)
	#print(tailledecomp)