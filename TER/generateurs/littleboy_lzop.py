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
	i = size * 180
if mod >= 2:
	i = size * 200
if mod >= 10:
	i = size * 212
if mod >= 30:
	i = size * 215
if mod >= 50:
	i = size * 217
if mod >= 70:
	i = i + 75000
if mod >= 100:
	i = size * 219
if mod >= 400:
	i = i + 100000
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
if size < 221 :
	subprocess.call("tar -caf file.tar.lzo file", shell=True)
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
	a = 1000

	#compression du fichier
	subprocess.call("tar -caf file.tar.lzo file", shell=True)

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.lzo", shell=True)
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
	    if size >= 500:
	    	#enlever 100 zeros de la fin
	    	f.truncate(pos-50) 
	    	tailledecomp = tailledecomp - 50
	    if size < 500:
	    	#enlever 100 zeros de la fin
	    	f.truncate(pos-1) 
	    	tailledecomp = tailledecomp - 1
	f.close()

	#compression du fichier
	subprocess.call("tar -caf file.tar.lzo file", shell=True)

	#calcul de la taille du fichier compresse
	proc = subprocess.check_output("stat -c %s file.tar.lzo", shell=True)
	taillecomp = int(proc.decode('ascii')) ;
	#print(taillecomp)
	#print(tailledecomp)
