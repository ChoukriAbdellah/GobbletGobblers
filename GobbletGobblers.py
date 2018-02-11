#!/usr/bin/env python3
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
victoire = False

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
    plateau[(1,1)].append(grandeCaseOrange)
    plateau[(2,2)].append(grandeCaseOrange)
    #Pour l'exemple on met des pièces oranges sur une diagonale (pour tester la fonction qui teste la condition de victoire)
        
def getCouleur(x,y,numPiece):
    global plateau
    return plateau[(x,y)][numPiece][0]

def getTaille(x,y,numPiece):
    global plateau
    return plateau[(x,y)][numPiece][1]

def getNbPieces(x,y):
    global plateau
    return len(plateau[(x,y)])

def getDernierePiece(x,y):
    return getNbPieces(x,y)-1

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

def checkLigne(x,y,u,v,t,z):
    global victoire
    if(getNbPieces(x,y) > 0):
        c1 = getCouleur(x,y,getDernierePiece(x,y))
        if(getNbPieces(u,v) > 0):
            c2 = getCouleur(u,v,getDernierePiece(u,v))
            if(getNbPieces(t,z) > 0):
                c3 = getCouleur(t,z,getDernierePiece(t,z))
                if(c1 == c2 and c2 == c3):
                    victoire = True

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
    
    """ On considère qu'on note le plateau de jeu dans un plan de cette façon (avec O représentant les cases):
      0 1 2 (X)
    0 O O O
    1 O O O
    2 O O O
    (Y)


initPlateau()
initExemple()
verifVictoire()
print("Victoire ?",victoire)

"""
posX = int(input("Entrez une position X : "))
posY = int(input("Entrez une position Y : "))
#taper 0,0 pour l'exemple
           
print("Nombre de pieces a cette case = ",getNbPieces(posX,posY))
print("Couleur de la premiere piece = ",getCouleur(posX,posY,0))
print("Couleur de la deuxieme piece = ", getCouleur(posX,posY,1))
print("Taille de la premiere piece = ",getTaille(posX,posY,0))
print("Taille de la deuxieme piece = ", getTaille(posX,posY,1))
"""
