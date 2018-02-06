#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Structure de données pour le projet Gobblet Gobblers
____________________________________________________

Représentation des couleurs:
1 = bleu
2 = orange

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

plateau = {}
#dictionnaire

def initPlateau():
    global plateau
    coordonnees = '0123'
    for i in list(coordonnees):
        for j in list(coordonnees):
            plateau[(int(i),int(j))] = []

def initExemple():
    global plateau
    petiteCaseBleue = [1,1]
    grandeCaseOrange = [2,3]
    plateau[(0,0)].append(petiteCaseBleue)
    plateau[(0,0)].append(grandeCaseOrange)
#pour l'exemple on rajoute 2 pièces à la case 0,0
        
def getCouleur(x,y,numPiece):
    global plateau
    return couleurToString(plateau[(x,y)][numPiece][0])

def getTaille(x,y,numPiece):
    global plateau
    return tailleToString(plateau[(x,y)][numPiece][1])

def getNbPieces(x,y):
    global plateau
    return len(plateau[(x,y)])

def tailleToString(x):
    if x == 1:
        return "petite"
    elif x == 2:
        return "moyenne"
    elif x == 3:
        return "grande"

def couleurToString(x):
    if x == 1:
        return "bleue"
    elif x == 2:
        return "orange"

initPlateau()
initExemple()
posX = int(input("Entrez une position X : "))
posY = int(input("Entrez une position Y : "))
#taper 0,0 pour l'exemple
           
print "Nombre de pieces a cette case = ",getNbPieces(posX,posY)
print "Couleur de la premiere piece = ",getCouleur(posX,posY,0)
print "Couleur de la deuxieme piece = ", getCouleur(posX,posY,1)
print "Taille de la premiere piece = ",getTaille(posX,posY,0)
print "Taille de la deuxieme piece = ", getTaille(posX,posY,1)
