#!/usr/bin/env python3
# module: tkinter
from tkinter import *
from random import randrange
import tkinter.font as tkFont
import sys, time

#____Variables globales_____

choix="menu"
stop=False
mode = "Joueur VS Joueur" #par défaut
coupsJ2=0
coupsJ1=0
couleurJoueur='blue'
tourJoueur='Joueur 1'
gagnant="personne"
texte = ""
listePiecesIA3 = []
plateau = {}

def initialiserListeIA():
	global listePiecesIA
	listePiecesIA = []
	petitePieceRouge = [2,1]
	moyennePieceRouge = [2,2]
	grandePieceRouge = [2,3]

	listePiecesIA.append(petitePieceRouge)
	listePiecesIA.append(petitePieceRouge)
	listePiecesIA.append(moyennePieceRouge)
	listePiecesIA.append(moyennePieceRouge)
	listePiecesIA.append(grandePieceRouge)
	listePiecesIA.append(grandePieceRouge)

initialiserListeIA()

victoire = False

class Position:
	def __init__( self, var):
		self.var=var
	def getPosition(self):
		return self.var
	def setPosition(self, _var):
		 self.var= _var
_position= Position(0)


def changerTourJoueur(couleurJoueur):
	global tourJoueur
	if couleurJoueur=='blue':
		tourJoueur='Joueur 1'
	else:
		tourJoueur='Joueur 2'

def changerCouleur():
	global couleurJoueur
	if couleurJoueur=='blue' :
		couleurJoueur='red'
	else :
		couleurJoueur='blue'
		
class Bac_a_sable(Canvas):
	"Canevas modifié pour prendre en compte quelques actions de la souris"
	def __init__(self, boss, width=80, height=80, bg="white"):
	# invocation du constructeur de la classe parente :
		Canvas.__init__(self, boss, width=width, height=height, bg=bg)
		# association-liaison d'événements <souris> au présent widget :
		self.bind("<Button-1>", self.mouseDown)
		self.bind("<Button1-Motion>", self.mouseMove)
		self.bind("<Button1-ButtonRelease>", self.mouseUp)

	def mouseDown(self, event):
		"Opération à effectuer quand le bouton gauche de la souris est enfoncé"
		if (victoire):
			rejouer() #Quand la partie se termine et que le joueur clique n'importe où, on relance une autre partie
		self.currObject =None
		# event.x et event.y contiennent les coordonnées du clic effectué :
		self.x1, self.y1 = event.x, event.y
		# <find_closest> renvoie la référence du dessin le plus proche :
		self.selObject = self.find_closest(self.x1, self.y1)
		
		if (couleurJoueur==self.itemcget(self.selObject, "fill") ) :
			# modification de l'épaisseur du contour du dessin
			_position.setPosition(self.coords(self.selObject))
			self.itemconfig(self.selObject, width =3)
			# <lift> fait passer le dessin à l'avant-plan :
			self.lift(self.selObject)
			whatCase(event.x , event.y)
			if whatCase(event.x , event.y) !=(-1,-1):
					deleteDernierePiece(whatCase(event.x , event.y))
			
	def mouseMove(self, event):
		if (couleurJoueur==self.itemcget(self.selObject, "fill") ) :
			"Op. à effectuer quand la souris se déplace, bouton gauche enfoncé"
			x2, y2 = event.x, event.y
			dx, dy = x2 -self.x1, y2 -self.y1
			typeObjet=self.type(self.selObject)
			if self.selObject  and  typeObjet== "rectangle"  :
				self.move(self.selObject, dx, dy)
				self.x1, self.y1 = x2, y2
	def mouseUp(self, event):
		"Op. à effectuer quand le bouton gauche de la souris est relâché"
		if (couleurJoueur==self.itemcget(self.selObject, "fill")) :
			if self.selObject :
				if canAdd(whatCase(event.x , event.y), taille(self.coords(self.selObject))) == False  :
					couleur2=self.itemcget(self.selObject, "fill")
	
					Canevas.delete('Gobblet gobblers',self.selObject) 
					Canevas.create_rectangle(_position.getPosition(), outline='black', fill=couleur2)
				else :
					self.itemconfig(self.selObject, width =1)
				#self.selObject =None
		
					couleur=self.itemcget(self.selObject, "fill")
					typeObjet=self.type(self.selObject)

					if typeObjet== "rectangle"  :
						def getCouleurVoid():
							couleur =self.itemcget(self.selObject, "fill")
							return couleur
						def getTailleVoid():
							taille=taille(coordonneesRectangle)
							return taille
						couleur2Int(getCouleurVoid())
						coordonneesRectangle = self.coords(self.selObject)
						taille(coordonneesRectangle)

					""" On supprime un rec s'il s'agit d'un deplacement dans la grille"""	

					setCase(whatCase(event.x,event.y),couleur2Int(getCouleurVoid()), taille(coordonneesRectangle))
					placerPiece(whatCase(event.x, event.y), taille(coordonneesRectangle), self.selObject)
					nbCoups(couleurJoueur)
					checkVictoire()
					
					if victoire == False :
						global mode
						if mode == "Joueur VS Joueur": #Si c'est le mode JoueurVSJoueur, on change le tour du joueur
							changerCouleur()
							changerTourJoueur(couleurJoueur)
							modifJoueur()

						elif mode == "Joueur VS Ordinateur 1" : #Si c'est le mode IA aléatoire, on lance la fonction 
							changerCouleur()
							IAaleatoire()

						elif mode == "Joueur VS Ordinateur 2" : #Si c'est le mode IA aléatoire, on lance la fonction 
							changerCouleur()
							IAplus()
					
			else:
				whatCase(event.x , event.y)

			affichePlateau()

def checkVictoire():
	verifVictoire()
	if (victoire) :
		global texte
		Canevas.delete(texte)
		texte=Canevas.create_text(250,500,tag='victoire',text="Victoire!",fill=couleurJoueur,font=('Marker Felt','50','bold'))
		afficheScore()

def IAaleatoire():
	global listePiecesIA2, listePiecesIA3

	"""Détail du code:
	listePiecesIA = la liste des pièces(sous forme de liste de données) qu'il reste à placer
	listePiecesIA2 = la même liste mais avec les pièces sous forme d'objet graphiques (les dessins avec le canevas)
	listePiecesIA3 = liste avec les pièces qui sont déjà placées sur le plateau
	"""

	if (len(listePiecesIA) > 0 and canAddOne(listePiecesIA)) : #Tant qu'on a des pièces à placer on fait ça :
		tirage = randrange(0,len(listePiecesIA)) #on tire un chiffre au hasard parmi la liste des pièces qu'il reste à placer
		pieceHasard = listePiecesIA[tirage] #on recupère cette pièce avec l'index du chiffre tiré au hasard
		listePiecesIA.remove(pieceHasard)  #on enlève la pièce de la liste car on va la placer et elle sera plus à placer
		cleHasard = caseLibre(pieceHasard[1]) #caseLibre renvoie une clé tirée au hasard parmi une liste de cases où il est possible de placer la pièce qu'on vient de tirer
		placerPiece(cleHasard, pieceHasard[1], listePiecesIA2[tirage]) #placerPiece permet de placer l'objet graphique qui correspond à la pièce qu'on a tirée
										# et cet objet est dans la liste IA2 avec le même index que dans la liste IA1
		listePiecesIA3.append(listePiecesIA2[tirage]) #On ajoute à la liste IA3 l'objet qu'on vient de placer (car IA3 est la liste des objets qu'on place)
		del listePiecesIA2[tirage] #On supprime l'objet qu'on a placé de la liste IA2 car il n'est plus à placer
		setCase(cleHasard, 2, pieceHasard[1]) #setCase permet de rentrer les donnée de la pièce dans la structure de donnée du plateau
		#print("test ia3", listePiecesIA3)
	else : #Si on a plus de pièces à placer, l'IA va déplacer celles qui sont déjà placées
		listeIA4 = []
		listeIA4 = deplacementsPossibles(2,listePiecesIA3)
		#print("Déplacements possibles : ", listeIA4)
		tirage = randrange(0,len(listeIA4))  #Tirage au sort d'une pièce parmi les pièces placées
		pieceHasard = listeIA4[tirage]
		taillePieceHasard = taille(Canevas.coords(pieceHasard))
		cleHasard = caseLibre(taillePieceHasard)
		if (cleHasard == (-1, -1)):
			while (cleHasard == (-1,-1)):
				tirage = randrange(0,len(listeIA4))  #Tirage au sort d'une pièce parmi les pièces placées
				pieceHasard = listeIA4[tirage]
				taillePieceHasard = taille(Canevas.coords(pieceHasard))
				cleHasard = caseLibre(taillePieceHasard)

		ancienneCaseX = Canevas.coords(pieceHasard)[0]
		ancienneCaseY = Canevas.coords(pieceHasard)[1]
		print("case avant delete : ",plateau[whatCase(ancienneCaseX, ancienneCaseY)])
		deleteDernierePiece( whatCase(ancienneCaseX, ancienneCaseY))
		placerPiece(cleHasard, taillePieceHasard, pieceHasard) #Deplacement de la pièce tirée au sort vers la clé tirée au sort
		print( "TEST DELETE", whatCase(ancienneCaseX,ancienneCaseY))
		print("case après delete : ",plateau[whatCase(ancienneCaseX,ancienneCaseY)])
		setCase(cleHasard, 2, taillePieceHasard) #On met les données dans le plateau
		
	checkVictoire()
	nbCoups(couleurJoueur)
	changerCouleur()

def IAplus():
	if (coupsJ2 == 0): #Premier mouvement de l'IA améliorée = placer une pièce au hasard
		tirage = randrange(0,len(listePiecesIA))
		premierePiece = listePiecesIA[tirage]
		listePiecesIA.remove(premierePiece)
		cleHasard = caseLibre(premierePiece[1])
		placerPiece(cleHasard, premierePiece[1], listePiecesIA2[tirage])
		listePiecesIA3.append(listePiecesIA2[tirage])
		del listePiecesIA2[tirage]
		setCase(cleHasard, 2, premierePiece[1])
	else:
		piecePlacee = False

		#Mode Défense (l'IA bloque le joueur s'il aligne 2 pièces, et s'il peut rien faire il passe en mode attaque)

		lignesJoueur = calculNbPiecesBleues() #renvoie la liste des lignes où le joueur a 2 pièces alignées
		print("Lignes joueur : ", lignesJoueur)

		if (canAddOne(listePiecesIA) and len(listePiecesIA) > 0):
			last = len(listePiecesIA)-1
			plusGrossePiece = listePiecesIA[last]
			for ligne in lignesJoueur:
				if(getNbPieces(ligne[0]) > 0):
					if (getCouleur(ligne[0],getDernierePiece(ligne[0])) != 2 and piecePlacee == False):
						if (canAdd(ligne[0], plusGrossePiece[1])):
							listePiecesIA.remove(plusGrossePiece)
							placerPiece(ligne[0], plusGrossePiece[1], listePiecesIA2[last])
							listePiecesIA3.append(listePiecesIA2[last])
							del listePiecesIA2[last]
							setCase(ligne[0], 2, plusGrossePiece[1])
							piecePlacee = True
				else:
					if (piecePlacee == False):
						listePiecesIA.remove(plusGrossePiece)
						placerPiece(ligne[0], plusGrossePiece[1], listePiecesIA2[last])
						listePiecesIA3.append(listePiecesIA2[last])
						del listePiecesIA2[last]
						setCase(ligne[0], 2, plusGrossePiece[1])
						piecePlacee = True

				if(getNbPieces(ligne[1]) > 0):
					if (getCouleur(ligne[1],getDernierePiece(ligne[1])) != 2 and piecePlacee == False):
						if (canAdd(ligne[1], plusGrossePiece[1])):
							listePiecesIA.remove(plusGrossePiece)
							placerPiece(ligne[1], plusGrossePiece[1], listePiecesIA2[last])
							listePiecesIA3.append(listePiecesIA2[last])
							del listePiecesIA2[last]
							setCase(ligne[1], 2, plusGrossePiece[1])
							piecePlacee = True
				else:
					if (piecePlacee == False):
						listePiecesIA.remove(plusGrossePiece)
						placerPiece(ligne[1], plusGrossePiece[1], listePiecesIA2[last])
						listePiecesIA3.append(listePiecesIA2[last])
						del listePiecesIA2[last]
						setCase(ligne[1], 2, plusGrossePiece[1])
						piecePlacee = True

				if(getNbPieces(ligne[2]) > 0):
					if (getCouleur(ligne[2],getDernierePiece(ligne[2])) != 2 and piecePlacee == False):
						if (canAdd(ligne[2], plusGrossePiece[1])):
							listePiecesIA.remove(plusGrossePiece)
							placerPiece(ligne[2], plusGrossePiece[1], listePiecesIA2[last])
							listePiecesIA3.append(listePiecesIA2[last])
							del listePiecesIA2[last]
							setCase(ligne[2], 2, plusGrossePiece[1])
							piecePlacee = True
				else:
					if (piecePlacee == False):
						listePiecesIA.remove(plusGrossePiece)
						placerPiece(ligne[2], plusGrossePiece[1], listePiecesIA2[last])
						listePiecesIA3.append(listePiecesIA2[last])
						del listePiecesIA2[last]
						setCase(ligne[2], 2, plusGrossePiece[1])
						piecePlacee = True

		else:
			listeIA4 = []
			listeIA4 = deplacementsPossibles(2,listePiecesIA3)
			tirage = randrange(0,len(listeIA4))  #Tirage au sort d'une pièce parmi les pièces placées
			pieceHasard = listeIA4[tirage]
			taillePieceHasard = taille(Canevas.coords(pieceHasard))
			cleHasard = caseLibre(taillePieceHasard)
			if (cleHasard == (-1, -1)):
				while (cleHasard == (-1,-1)):
					tirage = randrange(0,len(listeIA4))  #Tirage au sort d'une pièce parmi les pièces placées
					pieceHasard = listeIA4[tirage]
					taillePieceHasard = taille(Canevas.coords(pieceHasard))
					cleHasard = caseLibre(taillePieceHasard)
			ancienneCaseX = Canevas.coords(pieceHasard)[0]
			ancienneCaseY = Canevas.coords(pieceHasard)[1]
			print("case avant delete : ",plateau[whatCase(ancienneCaseX, ancienneCaseY)])
			deleteDernierePiece( whatCase(ancienneCaseX, ancienneCaseY))
			placerPiece(cleHasard, taillePieceHasard, pieceHasard) #Deplacement de la pièce tirée au sort vers la clé tirée au sort
			print( "TEST DELETE", whatCase(ancienneCaseX,ancienneCaseY))
			print("case après delete : ",plateau[whatCase(ancienneCaseX,ancienneCaseY)])
			setCase(cleHasard, 2, taillePieceHasard) #On met les données dans le plateau
			piecePlacee = True

		#Mode Attaque (l'IA place ses pièces dans le but de gagner, il essaye d'aligner une ligne)
		

		if (piecePlacee == False and canAddOne(listePiecesIA)): 
			if (len(listePiecesIA) > 0) :
				lignesPossibles = calculNbPiecesRouges() #renvoie la liste des lignes possibles (une ligne possible = une liste où l'IA a posé le + de pièces)
				last = len(listePiecesIA)-1
				plusGrossePiece = listePiecesIA[last]
				print("Lignes possibles : ", lignesPossibles)

				for ligne in lignesPossibles:
					if(getNbPieces(ligne[0]) > 0):
						if (getCouleur(ligne[0],getDernierePiece(ligne[0])) != 2 and piecePlacee == False):
							if (canAdd(ligne[0], plusGrossePiece[1])):
								listePiecesIA.remove(plusGrossePiece)
								placerPiece(ligne[0], plusGrossePiece[1], listePiecesIA2[last])
								listePiecesIA3.append(listePiecesIA2[last])
								del listePiecesIA2[last]
								setCase(ligne[0], 2, plusGrossePiece[1])
								piecePlacee = True
					else:
						if (piecePlacee == False):
							listePiecesIA.remove(plusGrossePiece)
							placerPiece(ligne[0], plusGrossePiece[1], listePiecesIA2[last])
							listePiecesIA3.append(listePiecesIA2[last])
							del listePiecesIA2[last]
							setCase(ligne[0], 2, plusGrossePiece[1])
							piecePlacee = True

					if(getNbPieces(ligne[1]) > 0):
						if (getCouleur(ligne[1],getDernierePiece(ligne[1])) != 2 and piecePlacee == False):
							if (canAdd(ligne[1], plusGrossePiece[1])):
								listePiecesIA.remove(plusGrossePiece)
								placerPiece(ligne[1], plusGrossePiece[1], listePiecesIA2[last])
								listePiecesIA3.append(listePiecesIA2[last])
								del listePiecesIA2[last]
								setCase(ligne[1], 2, plusGrossePiece[1])
								piecePlacee = True
					else:
						if (piecePlacee == False):
							listePiecesIA.remove(plusGrossePiece)
							placerPiece(ligne[1], plusGrossePiece[1], listePiecesIA2[last])
							listePiecesIA3.append(listePiecesIA2[last])
							del listePiecesIA2[last]
							setCase(ligne[1], 2, plusGrossePiece[1])
							piecePlacee = True

					if(getNbPieces(ligne[2]) > 0):
						if (getCouleur(ligne[2],getDernierePiece(ligne[2])) != 2 and piecePlacee == False):
							if (canAdd(ligne[2], plusGrossePiece[1])):
								listePiecesIA.remove(plusGrossePiece)
								placerPiece(ligne[2], plusGrossePiece[1], listePiecesIA2[last])
								listePiecesIA3.append(listePiecesIA2[last])
								del listePiecesIA2[last]
								setCase(ligne[2], 2, plusGrossePiece[1])
								piecePlacee = True
					else:
						if (piecePlacee == False):
							listePiecesIA.remove(plusGrossePiece)
							placerPiece(ligne[2], plusGrossePiece[1], listePiecesIA2[last])
							listePiecesIA3.append(listePiecesIA2[last])
							del listePiecesIA2[last]
							setCase(ligne[2], 2, plusGrossePiece[1])
							piecePlacee = True

				if (piecePlacee == False): #Si après avoir testé toutes les lignes possibles, aucun cas n'est envisageable, on place alors une case au hasard
					tirage = randrange(0,len(listePiecesIA))
					piece = listePiecesIA[tirage]
					listePiecesIA.remove(piece)
					cleHasard = caseLibre(piece[1])
					placerPiece(cleHasard, piece[1], listePiecesIA2[tirage])
					listePiecesIA3.append(listePiecesIA2[last])
					del listePiecesIA2[tirage]
					setCase(cleHasard, 2, piece[1])
					piecePlacee = True

		


#... pas fini

	checkVictoire()
	nbCoups(couleurJoueur)
	changerCouleur()

def deplacementsPossibles(col, l):
#Cette fonction renvoie seulement les pièces déjà placées qu'on peut déplacer (donc ces pièces se situent à la dernière position d'une case)
	coordonnees = '012'
	res = []
	for piece in l:
		for i in list(coordonnees):
			for j in list(coordonnees):
				if (getNbPieces((int(i),int(j))) > 0):
					if( getCouleur( (int(i),int(j)),getDernierePiece( (int(i),int(j)) )) == col and taille(Canevas.coords(piece)) == getTaille( (int(i),int(j) ),getDernierePiece( (int(i),int(j)) ))):
				#print("coords", Canevas.coords(piece))
						res.append(piece)
	return res
	

def canAddOne(liste):
	coordonnees = '012'
	for piece in liste:
		for i in list(coordonnees):
			for j in list(coordonnees):
				if (canAdd((int(i),int(j)), piece[1])):
					return True
	return False


def calculNbPiecesLigne(x,y,u,v,t,z,col):
	nb = 0
	if(getNbPieces((x,y)) > 0):
		if (getCouleur((x,y),getDernierePiece((x,y))) == col):
			nb+=1
	if(getNbPieces((u,v)) > 0):
		if (getCouleur((u,v),getDernierePiece((u,v))) == col):
			nb+=1
	if(getNbPieces((t,z)) > 0):
		if (getCouleur((t,z),getDernierePiece((t,z))) == col):
			nb+=1
	return nb

def calculNbPiecesRouges():
	#Lignes horizontales :
	n1 = calculNbPiecesLigne(0,0,1,0,2,0,2)
	n2 = calculNbPiecesLigne(0,1,1,1,2,1,2)
	n3 = calculNbPiecesLigne(0,2,1,2,2,2,2)
	#Lignes verticales :
	n4 = calculNbPiecesLigne(0,0,0,1,0,2,2)
	n5 = calculNbPiecesLigne(1,0,1,1,1,2,2)
	n6 = calculNbPiecesLigne(2,0,2,1,2,2,2)
	#Diagonales :
	n7 = calculNbPiecesLigne(0,0,1,1,2,2,2)
	n8 = calculNbPiecesLigne(2,0,1,1,0,2,2)
	l=[]
	l.append(n1)
	l.append(n2)
	l.append(n3)
	l.append(n4)
	l.append(n5)
	l.append(n6)
	l.append(n7)
	l.append(n8)
	max = getMax(l)
	res = []
	if (n1 == max):
		res.append([(0,0),(1,0),(2,0)])
	if (n2 == max):
		res.append([(0,1),(1,1),(2,1)])
	if (n3 == max):
		res.append([(0,2),(1,2),(2,2)])
	if (n4 == max):
		res.append([(0,0),(0,1),(0,2)])
	if (n5 == max):
		res.append([(1,0),(1,1),(1,2)])
	if (n6 == max):
		res.append([(2,0),(2,1),(2,2)])
	if (n7 == max):
		res.append([(0,0),(1,1),(2,2)])
	if (n8 == max):
		res.append([(2,0),(1,1),(0,2)])
	return res

def calculNbPiecesBleues():
	#Lignes horizontales :
	n1 = calculNbPiecesLigne(0,0,1,0,2,0,1)
	n2 = calculNbPiecesLigne(0,1,1,1,2,1,1)
	n3 = calculNbPiecesLigne(0,2,1,2,2,2,1)
	#Lignes verticales :
	n4 = calculNbPiecesLigne(0,0,0,1,0,2,1)
	n5 = calculNbPiecesLigne(1,0,1,1,1,2,1)
	n6 = calculNbPiecesLigne(2,0,2,1,2,2,1)
	#Diagonales :
	n7 = calculNbPiecesLigne(0,0,1,1,2,2,1)
	n8 = calculNbPiecesLigne(2,0,1,1,0,2,1)
	res =  []
	if (n1 == 2):
		res.append([(0,0),(1,0),(2,0)])
	if (n2 == 2):
		res.append([(0,1),(1,1),(2,1)])
	if (n3 == 2):
		res.append([(0,2),(1,2),(2,2)])
	if (n4 == 2):
		res.append([(0,0),(0,1),(0,2)])
	if (n5 == 2):
		res.append([(1,0),(1,1),(1,2)])
	if (n6 == 2):
		res.append([(2,0),(2,1),(2,2)])
	if (n7 == 2):
		res.append([(0,0),(1,1),(2,2)])
	if (n8 == 2):
		res.append([(2,0),(1,1),(0,2)])
	return res
		

def getMax(liste):
	max = 0
	for n in liste:
		if n > max:
			max = n
	return max
	
#Renvoie une clé correspondant aux coordonnées d'une case libre pour une taille donnée
def caseLibre(taille): 
	listeCasesDispo = []
	coordonnees = '012'
	for i in list(coordonnees):
		for j in list(coordonnees):
			if (canAdd((int(i),int(j)), taille)):
				listeCasesDispo.append(((int(i),int(j))))
	cleHasard = (-1,-1)
	if (len(listeCasesDispo) > 0):
		cleHasard = listeCasesDispo[randrange(0,len(listeCasesDispo))]
	print("Cle hasard : ", cleHasard)
	return cleHasard


def placerPiece(cle, taille, objet): #Fonction pour placer une pièce au centre d'une case qu'on donne en paramètre
	if cle == (0,0) :
		if taille == 1 :
			Canevas.coords(objet,55,55,95,95)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,36,37,116,117)
			Canevas.lift(objet)	
		if taille == 3 :
			Canevas.coords(objet,26,27,126,127)
			Canevas.lift(objet)
	if cle == (0,1) :
		if taille == 1 :
			Canevas.coords(objet,57,245,97,205)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,36,266,116,186)
			Canevas.lift(objet)
		if taille == 3 :
			Canevas.coords(objet,26,174,126,274)
			Canevas.lift(objet)

	if cle == (0,2) :
		if taille == 1 :
			Canevas.coords(objet,57,394,97,354)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,36,414,116,334)	
			Canevas.lift(objet)
		if taille == 3 :
			Canevas.coords(objet,26,324,126,424)
			Canevas.lift(objet)

	if cle == (1,0) :
		if taille == 1 :
			Canevas.coords(objet,205,57,245,97)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,185,37,265,117)
			Canevas.lift(objet)
		if taille == 3 :
			Canevas.coords(objet,174,127,274,27)
			Canevas.lift(objet)

	if cle == (1,1) :
		if taille == 1 :
			Canevas.coords(objet,205,205,245,245)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,185,187,265,267)
			Canevas.lift(objet)	
		if taille == 3 :
			Canevas.coords(objet,174,174,273,274)
			Canevas.lift(objet)

	if cle == (1,2) :
		if taille == 1 :
			Canevas.coords(objet,206,394,246,354)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,186,415,266,335)
			Canevas.lift(objet)	
		if taille == 3 :
			Canevas.coords(objet,175,424,275,324)
			Canevas.lift(objet)

	if cle == (2,0) :
		if taille == 1 :
			Canevas.coords(objet,406,99,366,59)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,424,119,344,39)
			Canevas.lift(objet)	
		if taille == 3 :
			Canevas.coords(objet,434,127,334,27)
			Canevas.lift(objet)

	if cle == (2,1) :
		if taille == 1 :
			Canevas.coords(objet,405,205,365,245)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,426,187,346,267)
			Canevas.lift(objet)
		if taille == 3 :
			Canevas.coords(objet,434,174,334,274)
			Canevas.lift(objet)

	if cle == (2,2) :
		if taille == 1 :
			Canevas.coords(objet,405,394,365,354)
			Canevas.lift(objet)
		if taille == 2 :
			Canevas.coords(objet,426,415,346,335)
			Canevas.lift(objet)
		if taille == 3 :
			Canevas.coords(objet,434,424,334,324)
			Canevas.lift(objet)


def nbCoups(couleur):
	global coupsJ1,coupsJ2
	if couleur=="red":
		coupsJ2= coupsJ2+1
	else :
		coupsJ1=coupsJ1+1
	#print("gagnant ",  gagnant)
        
def afficheScore():
	global  gagnant
	if gagnant=='red':
		print("Le joueur rouge gagne la partie avec",coupsJ2," déplacements")
	else:
		print("Le joueur bleu gagne la partie avec",coupsJ1, " déplacements")
def  couleur2Int(c):
	couleurInt=0
	if c=="red":
		couleurInt=2
	else :
		couleurInt=1
	
	#print(" couleur=" ,couleurToString(couleurInt))
	return couleurInt

def taille( _taille):
	tailleRrectangle=0

	if _taille[2]-_taille[0] <=40 : 
		tailleRrectangle=1
	else:
		if _taille[2]-_taille[0] <=80  and _taille[2]-_taille[0] > 40  : 
				tailleRrectangle=2
		else:
			if _taille[2]-_taille[0] <=100 : 
				tailleRrectangle=3
	
	#print( "taille:", tailleToString(tailleRrectangle))
	return tailleRrectangle
																																																																																																																																																																			
def teste(a,b):
	print("Case (" , a ,", " , b,")")

def whatCase(a,b):
	if a<149 :
		if b<169:
			a,b=0,0

		if b>169 and b<300 :
			a,b=0,1
		if b>300:
			a,b=0,2	
	if a>149 and a<300:
		if b<169:
			if b<169:
				a,b=1,0

		if b>169 and b<300 :
				a,b=1,1

		if b>300:
			a,b=1,2
				
	if a>300 and a<470 :
		if b<169:
			if b<169:
				a,b=2,0

		if b>169 and b<300 :
				a,b=2,1

		if b>300:
			a,b=2,2
	"""a ou b hors de la grille"""
	if a<3:
		"""teste(a,b)	"""		
		return a,b
	
	else :
		return -1,-1

def modifJoueur():
	global texte
	Canevas.delete(texte)
	texte=Canevas.create_text(250,500,tag='joueur',text=tourJoueur,fill=couleurJoueur,font=('Marker Felt','50','bold'))
	
def Effacer():
	Canevas.delete(ALL)

def rejouer():
	global victoire, coupsJ1, coupsJ2, couleurJoueur, listePiecesIA3
	Effacer()
	listePiecesIA3 = []
	couleurJoueur='blue'
	tourJoueur='Joueur 1'
	coupsJ1=0
	coupsJ2=0
	initPlateau() #On refait un nouveau plateau
	initialiserListeIA() #On ré-initialise les pièces jouables par l'IA
	victoire = False #On ré-initialise la variable de victoire pour la prochaine partie
	affiche()

def modifChoix(newChoice):
	global choix
	choix=newChoice

def fermerFenetre():
	global choix, mode
	if choix=="menu" and mode!="aucun":
		menuQuitter()
	if choix=="jeu":
		maFenetreQuitter()
	else:
		menuQuitter_option()
	
	
def maFenetreQuitter():
	global couleurJoueur, tourJoueur
	couleurJoueur='blue'
	tourJoueur = 'Joueur 1'
	modifChoix("menu")
	Mafenetre.destroy()

def QuitterOption():
	modifChoix("menu")
	fenetreOption.destroy()


def menuQuitter():
	modifChoix("jeu")
	menu2.destroy()

def menuQuitter_option():
	modifChoix("option")
	menu2.destroy()

def quitter():
	fermerFenetre()
	global stop
	stop=True

def modifMode(newMode):
	global mode
	mode=newMode

#____________Structure de données____________
"""	
Représentation des couleurs:
1 = bleu
2 = rouge
Représentation des tailles:
1 = petit
2 = moyen
3 = grand
Représentation des pièces:
Une pièce = une liste sous la forme [numCouleur,numTaille]
ex : petite pièce bleue = [1,1]
Représentation des cases du plateau:
Une case du plateau de coordonnée (x,y) = un élément du dictionnaire plateau avec une clé (x,y)
Chaque case du plateau est une liste
On peut ajouter à chaque case une liste de 3 pièces maximum imbriquées de 0 à 2 de la plus petite pièce à la plus grande
"""
def initPlateau():
	global plateau
	coordonnees = '012'
	for i in list(coordonnees):
		for j in list(coordonnees):
				plateau[(int(i),int(j))] = []
def getCase(cle):
	global plateau
	coordonnees = '012'
	for i in list(coordonnees):
		for j in list(coordonnees):
			if a==i and b==j:
				return plateau[(int(cle))]
	
def setCase(cle, couleur, taille):
	plateau[cle].append([couleur, taille])

def affichePlateau():
	global victoire, listePiecesIA
	print("Contenu du plateau à cet instant : ")
	print("__________________________________ ")
	for cle in plateau.keys():
		print("Nombre de pieces a la case = ",cle,":",getNbPieces(cle))
		#print("Couleur de la deuxieme piece = ", getDernierePiece(cle))
		if getNbPieces(cle) > 0 :
			print("Taille de la derniere piece a la case = ", cle,":",getTaille(cle,getDernierePiece(cle)))
			print("Couleur de la derniere piece a la case = ", cle,":", getCouleur(cle,getDernierePiece(cle)))
	verifVictoire()
	print("Victoire ?", victoire)
        
def getCouleur(cle,numPiece):
	global plateau
	return plateau[cle][numPiece][0]

def getTaille(cle,numPiece):
	global plateau
	return plateau[cle][numPiece][1]

def getNbPieces(cle):
	global plateau
	return len(plateau[cle])

def canAdd(cle, tailleCourante):
	if cle == (-1,-1) :
		return False
	if getNbPieces(cle) == 0 :
		return True
	if getNbPieces(cle) < 3 :
		if tailleCourante > getTaille(cle,getDernierePiece(cle)) :
			return True
		else :
			return False
	else :
		return False

def getDernierePiece(cle):
	return getNbPieces(cle)-1

def deleteDernierePiece(cle):
	plateau[cle] = plateau[cle][:getNbPieces(cle)-1]
				
def tailleToString(x):
	if x == 1:
		return "petite"
	elif x == 2:
		return "moyenne"
	elif x == 3:
		return "grande"

def couleurToString(x):
	if x == 1:
		return "blue"
	elif x == 2:
		return "red"
		
def checkLigne(x,y,u,v,t,z):
	global victoire
	global gagnant
	if(getNbPieces((x,y)) > 0):
		c1 = getCouleur((x,y),getDernierePiece((x,y)))
		if(getNbPieces((u,v)) > 0):
			c2 = getCouleur((u,v),getDernierePiece((u,v)))
			if(getNbPieces((t,z)) > 0):
				c3 = getCouleur((t,z),getDernierePiece((t,z)))
				if(c1 == c2 and c2 == c3):
					victoire = True
					gagnant=c1

def verifVictoire():
	#Lignes horizontales :
	checkLigne(0,0,1,0,2,0)
	checkLigne(0,1,1,1,2,1)
	checkLigne(0,2,1,2,2,2)
	#Lignes verticales :
	checkLigne(0,0,0,1,0,2)
	checkLigne(1,0,1,1,1,2)
	checkLigne(2,0,2,1,2,2)
	#Diagonales :
	checkLigne(0,0,1,1,2,2)
	checkLigne(2,0,1,1,0,2)
    
""" On note le plateau de jeu dans un plan de cette façon (avec O représentant les cases)
 	  0 1 2 (X)
	0 O O O
	1 O O O
	2 O O O
	(Y) """
	

#_______________Fenêtre de jeu______________#



if __name__ == '__main__':
	while stop!=True:
		print("mode de jeu en cours : ", mode)
		if choix=="jeu":
			Mafenetre = Tk()
			Mafenetre.title('GobbletGobblers')
			Mafenetre.geometry('800x700+400+300')# mise en place du canevas 
			Largeur = 780
			Hauteur = 550

			Canevas = Bac_a_sable(Mafenetre, width =Largeur, height =Hauteur, bg ='ivory')


			def affiche():
				Canevas.pack(padx =5, pady =5)
				global texte
				texte=Canevas.create_text(250,500,tag='joueur',text=tourJoueur,fill=couleurJoueur,font=('Marker Felt','50','bold'))

				Canevas.create_rectangle(560, 20, 600, 60, outline='black', fill='blue')
				Canevas.create_rectangle(620, 20, 660, 60, outline='black', fill='blue')

				Canevas.create_rectangle(520, 80, 600, 160, outline='black', fill='blue')
				Canevas.create_rectangle(620, 80, 700, 160, outline='black', fill='blue')
			
				Canevas.create_rectangle(500, 180, 600, 280, outline='black', fill='blue')
				Canevas.create_rectangle(620, 180, 720, 280, outline='black', fill='blue')

				p1 = Canevas.create_rectangle(560, 300, 600, 340, outline='black', fill='red')
				p2 = Canevas.create_rectangle(620, 300, 660, 340, outline='black', fill='red')

				p3 = Canevas.create_rectangle(520, 360, 600, 440, outline='black', fill='red')	
				p4 = Canevas.create_rectangle(620, 360, 700, 440, outline='black', fill='red')

				p5 = Canevas.create_rectangle(500, 460, 600, 560, outline='black', fill='red')
				p6 = Canevas.create_rectangle(620, 460, 720, 560, outline='black', fill='red')

				global listePiecesIA2
				listePiecesIA2 = []
				listePiecesIA2.append(p1)
				listePiecesIA2.append(p2)
				listePiecesIA2.append(p3)
				listePiecesIA2.append(p4)
				listePiecesIA2.append(p5)
				listePiecesIA2.append(p6)

				Canevas.create_line(5,5,5,450)
				Canevas.create_line(150,5,150,450)
				Canevas.create_line(300,5,300,450)
				Canevas.create_line(470,5,470,450)
				Canevas.create_line(5,5,470,5)

				Canevas.create_line(5,450,470,450)
				Canevas.create_line(5,300,470,300)
				Canevas.create_line(5,150,470,150)
		
			affiche()

			bouton=Button(Mafenetre, text="Rejouer", command= rejouer)
			bouton.pack()

			bouton=Button(Mafenetre, text= "Retour au menu", command=maFenetreQuitter)
			bouton.pack()

			bouton=Button(Mafenetre, text="Fermer", command= quitter)
			bouton.pack()


			initPlateau()
			Mafenetre.mainloop()

		if choix=="option":
			fenetreOption = Tk()
			fenetreOption.title('Gobblet Gobblers')
			fenetreOption.geometry('550x450+420+220')
		# Entete de la page

			Entete=Label(fenetreOption, text='Options', font=("Helvetica", 25), fg="orange")
			Entete.pack()


			def ModifChaineMode():
				global mode
				chaineMode.configure(text = "Mode selectionné : " + mode)
				chaineMode.pack()

			cadre=Frame(fenetreOption, width=250, height=350, borderwidth=2)
			cadre.pack(fill=BOTH)

			def selectMode1():
				global mode 
				modifMode("Joueur VS Joueur")
				ModifChaineMode()
			def selectMode2():
				global mode
				modifMode("Joueur VS Ordinateur 1")
				ModifChaineMode()
			def selectMode3():
				global mode
				modifMode("Joueur VS Ordinateur 2")
				ModifChaineMode()
			def exitOption():
				fenetreOption.destroy()
				global stop
				stop=True


			#image des boutons
			imageJvsJ = PhotoImage(file ='JvsJ.gif')
			imageJvIa= PhotoImage(file ='JvsIA.gif')
			imageIavsIa= PhotoImage(file ='ia2.gif')
			JvsJ = Button(fenetreOption, text="Joueur VS Joueur", image=imageJvsJ,command=selectMode1)
			JvsJ.pack()

			JvsIA = Button(fenetreOption, text="Joueur VS Ordinateur", image=imageJvIa, command=selectMode2)
			JvsIA.pack()

			IAvsIA = Button(fenetreOption, text="Ordinateur VS Ordinateur",image=imageIavsIa,  command=selectMode3)
			IAvsIA.pack()

			chaineMode=Label(fenetreOption,text="Mode selectionné  : ",font=("Helvetica", 18))
			chaineMode.pack()

			#Boutton pied de page
			
			boutton_Valider=Button(cadre, text='Retour',font=("Helvetica", 16), fg='green', command=QuitterOption)

			boutton_Quitter=Button(cadre,text='Quitter',font=("Helvetica", 16), fg='red', command=exitOption)

			boutton_Valider.pack(side=LEFT)

			boutton_Quitter.pack(side= RIGHT)

			fenetreOption.mainloop()

		if choix=="menu":
			menu2 = Tk()
			#var = IntVar()
			menu2.title('menu 2')
			menu2.geometry('550x500+420+120')

			canvas = Canvas(menu2, width=550, height=120,bg= 'light blue')
			canvas.create_rectangle(0, 0, 60, 120, outline='black', fill='blue')
			canvas.create_rectangle(490, 0, 550, 120, outline='black', fill='red')
			font=('Marker Felt','30','bold')
			#titre=PhotoImage(file ='aa.gif')
			canvas.create_text(260, 50, text="Gobblet Gobblers", font=font, fill='red')
			canvas.pack()
			#zone_dessin = Canvas(menu2,width=500,height=500,bg='yellow',bd=8,relief="ridge")

			#photo = PhotoImage(file ='dragon.gif')
			#item = zone_dessin.create_text(250, 250, text =photo)

			#zone_dessin.pack()
			def exit():
				menu2.destroy()
				global stop
				stop=True

			cadre=Frame(menu2, width=450, height=450, borderwidth=2,bg= 'light blue')

			cadre.pack(fill=BOTH)
			monFont=tkFont.Font(family='Helvetica', size=36, weight='bold')
			#menu = PhotoImage(file ='menu.gif')
				
		#canvas.pack()

			can1 = Canvas(menu2, width =160, height =160, bg ='white')
			#titre=PhotoImage(file ='aa.gif')
			play = PhotoImage(file ='play.gif')
			option= PhotoImage(file ='option.gif')
			Quitter= PhotoImage(file ='quitter.gif')
			#boutton_Option=Button(canvas, image =titre,fg='green')
			#boutton_Option.pack()
			item = can1.create_image(80, 80, image =play)
			item2 = can1.create_image(80, 80, image =option)
			item3 = can1.create_image(80, 80, image =Quitter)



			boutton_Valider=Button(cadre, image =play,fg='green', command=menuQuitter)
			boutton_Valider.pack()
				
			boutton_Valider=Button(cadre , fg='green', image=option, command=menuQuitter_option)
			boutton_Valider.pack()
			boutton_Valider=Button(cadre, fg='green', image=Quitter, command=exit)
			boutton_Valider.pack()


			label = Label(menu2)
			label.pack()
			menu2.mainloop()
