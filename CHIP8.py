import pygame as pg
import random
import gestionScreen
class CHIP8:
	def __init__(self,Rompath):
		# Initialisation de la mémoire, des registres, de la pile et des autres composants
		self.memoryCHIP = [0] * 4096  # 4KB de mémoire pour CHIP-8
		self.V = [0] * 16  # 16 registres généraux
		self.Stack = [0]*16  # Pile pour stocker les adresses de retour
		self.SP = 0  # Pointeur de pile
		self.I = 0  # Registre d'index
		self.PC = 0x200  # Compteur de programme commence à 0x200
		self.Keys = [0 for i in range(16)]  # État du clavier (16 touches)
		self.loadMemoryChip(Rompath)  # Chargement de la ROM en mémoire
		self.loadFonts()  # Chargement des polices en mémoire
		self.screen = gestionScreen.Screen()  # Initialisation de l'affichage
		self.DT = 0  # Minuteur de délai
		self.ST = 0  # Minuteur sonore
		self.clock = pg.time.Clock()  # Horloge pour la gestion du temps

	def loadFonts(self):
		# Ensemble de polices CHIP-8 stocké en mémoire (chaque caractère fait 5 octets)
		fonts =[
			0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
			0x20, 0x60, 0x20, 0x20, 0x70,  # 1
			0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
			0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3	
			0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
			0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
			0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
			0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
			0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
			0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
			0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
			0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
			0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
			0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
			0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
			0xF0, 0x80, 0xF0, 0x80, 0x80   # F
		]
		for idx, val in enumerate(fonts):  # Chargement des polices en mémoire à partir de l'adresse 0x000
			self.memoryCHIP[idx] = val 

	def loadMemoryChip(self,Rompath):
		# Chargement du fichier ROM en mémoire à partir de l'adresse 0x200
		with open(Rompath, "rb") as f:
			romData = f.read()
		for i in range(0, len(romData)):
			self.memoryCHIP[0x200+i] = romData[i]

	def decodeChip8(self):
		# Décodage et écriture du contenu mémoire dans un fichier texte pour le débogage
		Text = open ("Text2.txt","wt")
		for i in range(0, len(self.memoryCHIP),2):
			Text.write(f"0x{0x000+i:03X}: {self.memoryCHIP[i]<<8|self.memoryCHIP[i+1]:04X} \n")
		Text.close()

	def opcode(self):
		# Récupération de la prochaine instruction en mémoire
		result = self.memoryCHIP[self.PC]<<8|self.memoryCHIP[self.PC+1]
		return (result)

	def executeopcode(self, opcode):
		# Décomposition de l'opcode en ses 4 composants hexadécimaux
		c1 = opcode & 0X000F         # Dernier chiffre (nibble)
		c2 = (opcode & 0X00F0) >> 4  # Troisième chiffre
		c3 = (opcode & 0X0F00) >> 8  # Deuxième chiffre
		c4 = (opcode & 0XF000) >> 12 # Premier chiffre

		# Assurer que les registres sont dans la plage 8 bits (0-255)
		self.V[c3] = self.V[c3] % (2**8)
		self.V[c2] = self.V[c2] % (2**8)

		# Analyse de l'opcode en fonction de son premier chiffre (c4)
		match c4:
			case 0:
				# Instruction 00EE : Retour de sous-routine
				if c2 == 0xE and c1 == 0xE:
					if self.SP > 0:
						self.SP -= 1
						self.PC = self.Stack[self.SP]
				# Instruction 00E0 : Effacer l'écran
				elif c2 == 0xE:
					self.screen.clear()

			case 1:
				# Instruction 1NNN : Saut à l'adresse NNN
				self.PC = opcode & 0X0FFF
				self.PC -= 2

			case 2:
				# Instruction 2NNN : Appel de sous-routine à l'adresse NNN
				if self.SP < 15:
					self.Stack[self.SP] = self.PC
					self.SP += 1
					self.PC = opcode & 0X0FFF
					self.PC -= 2

			case 3:
				# Instruction 3XNN : Sauter l'instruction suivante si V[X] == NN
				if self.V[c3] == (opcode & 0X00FF):
					self.PC += 2

			case 4:
				# Instruction 4XNN : Sauter l'instruction suivante si V[X] != NN
				if self.V[c3] != (opcode & 0X00FF):
					self.PC += 2

			case 5:
				# Instruction 5XY0 : Sauter l'instruction suivante si V[X] == V[Y]
				if self.V[c3] == self.V[c2]:
					self.PC += 2

			case 6:
				# Instruction 6XNN : Charger NN dans V[X]
				self.V[c3] = opcode & 0X00FF

			case 7:
				# Instruction 7XNN : Ajouter NN à V[X] (sans retenue)
				self.V[c3] += opcode & 0X00FF

			case 8:
				# Instructions arithmétiques et logiques 8XY_
				match c1:
					case 0:  self.V[c3] = self.V[c2]                # 8XY0 : V[X] = V[Y]
					case 1:  self.V[c3] |= self.V[c2]               # 8XY1 : V[X] |= V[Y]
					case 2:  self.V[c3] &= self.V[c2]               # 8XY2 : V[X] &= V[Y]
					case 3:  self.V[c3] ^= self.V[c2]               # 8XY3 : V[X] ^= V[Y]
					case 4:                                         # 8XY4 : Addition avec retenue
						self.V[15] = 1 if self.V[c3] + self.V[c2] > 255 else 0
						self.V[c3] += self.V[c2]
					case 5:                                         # 8XY5 : Soustraction V[X] -= V[Y]
						self.V[15] = 1 if self.V[c3] > self.V[c2] else 0
						self.V[c3] -= self.V[c2]
					case 6:                                         # 8XY6 : Décalage à droite
						self.V[15] = self.V[c3] & 0x1
						self.V[c3] >>= 1
					case 7:                                         # 8XY7 : V[X] = V[Y] - V[X]
						self.V[15] = 1 if self.V[c2] > self.V[c3] else 0
						self.V[c3] = self.V[c2] - self.V[c3]
					case 0xE:                                       # 8XYE : Décalage à gauche
						self.V[15] = self.V[c3] >> 7
						self.V[c3] <<= 1

			case 9:
				# Instruction 9XY0 : Sauter l'instruction suivante si V[X] != V[Y]
				if self.V[c3] != self.V[c2]:
					self.PC += 2

			case 0xA:
				# Instruction ANNN : Charger I avec l'adresse NNN
				self.I = opcode & 0X0FFF

			case 0xB:
				# Instruction BNNN : Saut à l'adresse NNN + V[0]
				self.PC = (opcode & 0X0FFF) + self.V[0]

			case 0xC:
				# Instruction CXNN : V[X] = nombre aléatoire & NN
				self.V[c3] = random.randint(0, 255) & (opcode & 0X00FF)

			case 0xD:
				# Instruction DXYN : Dessiner un sprite à (V[X], V[Y])
				self.draw(self.V[c3], self.V[c2], c1)

			case 0xE:
				# Gestion des touches
				if c2 == 0x9 and self.Keys[c3] == 1:  # EX9E : Sauter si touche pressée
					self.PC += 2
				elif c2 == 0xA and self.Keys[c3] == 0:  # EXA1 : Sauter si touche non pressée
					self.PC += 2

			case 0xF:
				# Instructions FX__
				match opcode & 0X00FF:
					case 0x07: self.V[c3] = self.DT          # FX07 : Lire la valeur du timer de retard
					case 0x0A:                                # FX0A : Attente de pression d'une touche
						wait = 0
						while wait == 1:
							self.listen()
							for idx, val in enumerate(self.Keys):
								if val == 1:
									self.V[c3] = idx
									wait = 1
					case 0x15: self.DT = c3                  # FX15 : Définir le timer de retard
					case 0x18: self.ST = c3                  # FX18 : Définir le timer de son
					case 0x1E: self.I += self.V[c3]          # FX1E : Ajouter V[X] à I
					case 0x29: self.I = self.V[c3] * 5               # FX29 : Charger l'adresse du sprite du caractère
					case 0x33:                               # FX33 : Stocker BCD de V[X] en mémoire
						self.memoryCHIP[self.I] = self.V[c3] // 100
						self.memoryCHIP[self.I + 1] = (self.V[c3] // 10) % 10
						self.memoryCHIP[self.I + 2] = self.V[c3] % 10
					case 0x55:                               # FX55 : Sauvegarde les registres V[0] à V[X] en mémoire
						for i in range(c3 + 1):
							self.memoryCHIP[self.I + i] = self.V[i]
					case 0x65:                               # FX65 : Charger les registres depuis la mémoire
						for i in range(c3 + 1):
							self.V[i] = self.memoryCHIP[self.I + i]

		# Incrémentation du compteur de programme
		self.PC += 2
	
	def listen(self):
		for event in pg.event.get():
			# Quitter le programme si l'événement QUIT est détecté
			if event.type == pg.QUIT:
				self.running = False

			# Gestion des timers (son et délai)
			elif event.type == self.DELAYSOUNDTIMER:
				if self.ST > 0:
					self.ST -= 1  # Décrémente le timer sonore
				self.playSound()  # Joue ou arrête le son en fonction du timer sonore

				if self.DT > 0:
					self.DT -= 1  # Décrémente le timer de délai

			# Fermer l'application en appuyant sur la touche Échap
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.running = False

		# Récupérer l'état des touches pressées
		keys = pg.key.get_pressed()
		for i, l in enumerate("1234azerqsdfwxcv"):
			self.Keys[i] = keys[self.screen.keys[l]]

		# Gestion de la configuration des touches avec la souris
		if pg.mouse.get_pressed()[0]:  # Si clic gauche
			x, y = pg.mouse.get_pos()
			
			# Vérifier si le clic est dans un rectangle virtuel
			collide = pg.Rect((x - self.screen.screen.get_width() * 10, y), (1, 1)).collidelist(self.screen.Virtualrect)

			if collide != -1:
				while not (e := pg.event.get(pg.KEYUP)):  # Attendre qu’une touche soit relâchée
					pass
				self.screen.keys["1234azerqsdfwxcv"[collide]] = e[0].key  # Associer la touche relâchée au bouton cliqué


	def playSound(self):
		# Si un son est en cours mais que le timer est à 0, on l’arrête
		if pg.mixer.get_busy() and self.ST <= 0:
			self.screen.sound.stop()

		# Si aucun son ne joue mais que le timer est actif, on joue le son en boucle
		elif not pg.mixer.get_busy() and self.ST > 0:
			self.screen.sound.play(-1)

	def draw(self, c3, c2, c1):
		self.V[15] = 0  # Registre VF utilisé pour détecter les collisions

		for i in range(c1):  # Parcours des lignes du sprite
			bytes = self.memoryCHIP[self.I + i]  # Récupérer un octet de la mémoire CHIP-8
			y = c2 + i  # Position Y d’affichage
			y %= self.screen.screen.get_height()  # Gérer le débordement vertical

			for t in range(8):  # Parcours des bits du sprite
				x = c3 + t  # Position X d’affichage
				x %= self.screen.screen.get_width()  # Gérer le débordement horizontal

				byte = (bytes & (0x1 << (7 - t))) >> (7 - t)  # Extraire le bit correspondant

				# Récupérer la couleur actuelle du pixel
				color = self.screen.screen.get_at((x, y))
				if color == self.screen.black:
					color = 0
				elif color == self.screen.white:
					color = 1

				# Détection des collisions (si un pixel actif est inversé)
				if color == 1 and byte == 1:
					self.V[15] = 1  # Indiquer une collision dans VF

				# XOR entre l'ancien pixel et le nouveau pixel
				byte = color ^ byte
				self.screen.screen.set_at((x, y), (255 * byte, 255 * byte, 255 * byte))  # Affichage en blanc ou noir

	def Mainchip8(self):
		self.running = True  # Indique que l’émulateur est en cours d’exécution
		self.DELAYSOUNDTIMER = 1  # Identifiant de l'événement timer
		pg.time.set_timer(self.DELAYSOUNDTIMER, round((1 / 60) * 1000))  # Déclencher un événement toutes les 1/60e de seconde

		while self.running:  # Boucle principale
			self.listen()  # Écouter les entrées utilisateur
			self.executeopcode(self.opcode())  # Exécuter une instruction CHIP-8
			self.screen.display()  # Mettre à jour l'affichage
			self.clock.tick(60 * 8)  # Réguler la vitesse de la boucle à 60*8 Hz