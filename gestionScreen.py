import pygame as pg
class Screen:
	"""Déclaration de la classe Screen, responsable de l'affichage et du pavé numérique."""
	def __init__(self):
		self.sound = pg.mixer.Sound("hey_listen.wav") # Chargement du son
		self.grandscreen = pg.display.set_mode((860,320),pg.RESIZABLE) # Création de la fenêtre principale avec une taille de 860x320 pixels et possibilité de redimensionnement
		self.screen = pg.Surface((64,32)) # Création de la surface de jeu avec une résolution de 64x32 pixels
		self.virtualpad = pg.Surface((220,320)) # Création de la surface affichant les commandes avec une résolution de 220x320 pixels
		self.black = (0,0,0) # Définition de la couleur noire en RGB
		self.white = (255,255,255) # Définition de la couleur blanche en RGB
		self.screen.fill(self.black) # Remplissage de la surface de jeu avec la couleur noire
		self.virtualpad.fill(self.white) # Remplissage de la surface des commandes avec la couleur blanche
		self.font = pg.font.SysFont("arial",32) # Définition de la police de caractères Arial avec une taille de 32
		self.keys = { # Dictionnaire associant des touches clavier à des valeurs Pygame correspondantes
			"1" : pg.K_1,
			"2" : pg.K_2,
			"3" : pg.K_3,
			"4" : pg.K_4,
			"a" : pg.K_a,
			"z" : pg.K_z,
			"e" : pg.K_e,
			"r" : pg.K_r,
			"q" : pg.K_q,
			"s" : pg.K_s,
			"d" : pg.K_d,
			"f" : pg.K_f,
			"w" : pg.K_w,
			"x" : pg.K_x,
			"c" : pg.K_c,
			"v" : pg.K_v,
		}
		self.Virtualrect = [pg.Rect(0,0,0,0)]*16 # Initialisation d'une liste de 16 rectangles pour les boutons du pavé de commande

	def updatvirtualpad(self):
		"""Affichage et mise à jour du pavé tactile"""
		for i,(k,v) in enumerate(self.keys.items()): # Boucle parcourant le dictionnaire des touches pour afficher chaque bouton
			virtualbutton = pg.Surface((55,80)) # Création d'une surface de 55x80 pixels pour chaque bouton virtuel
			text = self.font.render(k,True,self.white) # Rendu du texte correspondant à la touche en blanc
			virtualbutton.blit(text,(55/2-text.get_width()/2,0)) 
			text = self.font.render(pg.key.name(v),True,self.white) # Rendu du nom de la touche en blanc
			virtualbutton.blit(text,(55/2-text.get_width()/2,32))
			self.Virtualrect[i] = self.virtualpad.blit(virtualbutton,(55*(i%4),80*(i//4))) # Affichage du bouton sur le pavé virtuel avec une disposition en grille

	def display(self):
		"""Méthode pour mettre à jour et afficher tous les éléments graphiques à l'écran."""
		self.updatvirtualpad()
		self.grandscreen.blit(pg.transform.scale((self.screen),(640,320)),(0,0)) # Redimensionnement et affichage de la surface de jeu sur la fenêtre principale
		self.grandscreen.blit(self.virtualpad,(640,0)) # Affichage du pavé de commandes sur la fenêtre principale
		pg.display.flip() # Rafraîchissement de l'affichage pour appliquer les modifications

	def clear(self):
		"""Méthode pour nettoyer l'écran de jeu en le remplissant de noir."""
		self.screen.fill(self.black) # Remplissage de la surface de jeu avec du noir pour effacer le contenu précédent
