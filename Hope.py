import pygame
import random
class Screen:
	def __init__(self):
		pygame.init()
		self.grandscreen = pygame.display.set_mode((1000,800),pygame.RESIZABLE)
		self.screen = pygame.Surface((64,32))
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.screen.fill(self.black)
	def display(self):
		self.grandscreen.blit(pygame.transform.scale(self.screen,(1000,800)),(0,0))
		pygame.display.flip()
	def clear(self):
		self.screen.fill(self.black)
class CHIP8:
	def __init__(self,Rompath):
		self.memoryCHIP = [0] * 4096
		self.V = [0] * 16
		self.Stack = [0]*16
		self.SP = 0
		self.PC = 0x200
		self.keys = [False for i in range(16)]
		self.loadMemoryChip(Rompath)
		self.loadFonts()
		self.screen = Screen()
	def loadFonts(self):
		fonts =[
			0xF0, 0x90, 0x90, 0x90, 0xF0, 	# 0
			0x20, 0x60, 0x20, 0x20, 0x70, 	# 1
			0xF0, 0x10, 0xF0, 0x80, 0xF0, 	# 2
			0xF0, 0x10, 0xF0, 0x10, 0xF0, 	# 3	
			0x90, 0x90, 0xF0, 0x10, 0x10, 	# 4
			0xF0, 0x80, 0xF0, 0x10, 0xF0, 	# 5
			0xF0, 0x80, 0xF0, 0x90, 0xF0, 	# 6
			0xF0, 0x10, 0x20, 0x40, 0x40, 	# 7
			0xF0, 0x90, 0xF0, 0x90, 0xF0, 	# 8
			0xF0, 0x90, 0xF0, 0x10, 0xF0, 	# 9
			0xF0, 0x90, 0xF0, 0x90, 0x90, 	# A
			0xE0, 0x90, 0xE0, 0x90, 0xE0, 	# B
			0xF0, 0x80, 0x80, 0x80, 0xF0, 	# C
			0xE0, 0x90, 0x90, 0x90, 0xE0, 	# D
			0xF0, 0x80, 0xF0, 0x80, 0xF0, 	# E
			0xF0, 0x80, 0xF0, 0x80, 0x80 	# F
			]
		for idx, val in enumerate(fonts): 	# For each byte
			self.memoryCHIP[idx] = val 	# We put it into the memory starting from the adress 0x0 which is easier for us, but it could be anywhere between 0x00 and 0x1FF because those memory cells are free and we only need 80 of them.			
	def loadMemoryChip(self,Rompath):
		with open(Rompath, "rb") as f:
			romData = f.read()
		for i in range(0, len(romData)):
			self.memoryCHIP[0x200+i] = romData[i]
	def decodeChip8(self):
		Text = open ("Text2.txt","wt")
		for i in range(0, len(self.memoryCHIP),2):
			Text.write(f"0x{0x000+i:03X}: {self.memoryCHIP[i]<<8|self.memoryCHIP[i+1]:04X} \n")
		Text.close()
	def opcode(self):
		result = self.memoryCHIP[self.PC]<<8|self.memoryCHIP[self.PC+1]
		return (result)
	def executeopcode(self,opcode):
		c1 = opcode & 0X00f
		c2 = (opcode & 0X00F0) >>4
		c3 = (opcode & 0X0F00) >>8
		c4 = (opcode & 0XF000) >>12
		if(c4 == 0):
			if(c2 == 0XE and c1 == 0XE):
				if(self.SP > 0):
					self.PC = self.Stack[self.SP]
					self.SP = self.SP-1
			elif(c2 == 0XE):
				self.screen.clear()




main = CHIP8("Tetris [Fran Dachille, 1991].ch8")

test1 = (main.opcode() & 0x00F0) >> 4
print(f"{test1:0X}")
running = True
while running ==True:
	#gestion de l'interuption de la boucle
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
	main.screen.display()