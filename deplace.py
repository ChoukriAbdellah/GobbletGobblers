#!/usr/bin/env python3
# module: tkinter
from tkinter import *
from random import randrange
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
		self.currObject =None
		# event.x et event.y contiennent les coordonnées du clic effectué :
		self.x1, self.y1 = event.x, event.y
		# <find_closest> renvoie la référence du dessin le plus proche :
		self.selObject = self.find_closest(self.x1, self.y1)
		# modification de l'épaisseur du contour du dessin :
		self.itemconfig(self.selObject, width =3)
		# <lift> fait passer le dessin à l'avant-plan :
		self.lift(self.selObject)
	def mouseMove(self, event):
		"Op. à effectuer quand la souris se déplace, bouton gauche enfoncé"
		x2, y2 = event.x, event.y
		dx, dy = x2 -self.x1, y2 -self.y1
		if self.selObject:
			self.move(self.selObject, dx, dy)
			self.x1, self.y1 = x2, y2
	def mouseUp(self, event):
		"Op. à effectuer quand le bouton gauche de la souris est relâché"
		if self.selObject:
			self.itemconfig(self.selObject, width =1)
			self.selObject =None

if __name__ == '__main__':
# ---- Programme de test ----
	Mafenetre = Tk()
	Mafenetre.title('Gobblet gobblers')
	Mafenetre.geometry('800x700+400+300')# mise en place du canevas 
	
	Largeur = 780
	Hauteur = 550

	Canevas =Bac_a_sable(Mafenetre, width =Largeur, height =Hauteur, bg ='ivory')

	Canevas.pack(padx =5, pady =5)
	def affiche():
		Canevas.create_rectangle(600, 40, 640, 80, outline='blue', fill='red')
		Canevas.create_rectangle(550, 40, 590, 80, outline='blue', fill='red')

		Canevas.create_rectangle(500, 90, 580, 150, outline='blue', fill='red')
		Canevas.create_rectangle(590, 90, 670, 150, outline='blue', fill='red')
			
		Canevas.create_rectangle(480, 170, 580, 270, outline='blue', fill='red')
		Canevas.create_rectangle(590, 170, 690, 270, outline='blue', fill='red')


		Canevas.create_rectangle(600, 280, 640, 320, outline='red', fill='blue')
		Canevas.create_rectangle(550, 280, 590, 320, outline='red', fill='blue')

		Canevas.create_rectangle(500, 330, 580, 410, outline='red', fill='blue')	
		Canevas.create_rectangle(590, 330, 670, 410, outline='red', fill='blue')

		Canevas.create_rectangle(480, 420, 580, 520, outline='red', fill='blue')
		Canevas.create_rectangle(590, 420, 690, 520, outline='red', fill='blue')


		Canevas.create_line(5,5,5,450)
		Canevas.create_line(150,5,150,450)
		Canevas.create_line(300,5,300,450)
		Canevas.create_line(470,5,470,450)
		Canevas.create_line(5,5,470,5)

		Canevas.create_line(5,450,470,450)
		Canevas.create_line(5,300,470,300)
		Canevas.create_line(5,150,470,150)
	affiche()
	def Effacer():
		Canevas.delete(ALL)
	def rejouer():
		Effacer()
		affiche()
	bouton=Button(Mafenetre, text="Fermer", command=Mafenetre.quit)
	bouton.pack()

	bouton=Button(Mafenetre, text="rejouer", command= rejouer)
	bouton.pack()

	Mafenetre.mainloop()
