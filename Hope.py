import pygame
import random
class Screen:
	def __init__(self):
		pygame.init()
		self.grandscreen = pygame.display.set_mode((640,320),pygame.RESIZABLE)
		self.screen = pygame.Surface((64,32))
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.screen.fill(self.black)
	def display(self):
		self.grandscreen.blit(pygame.transform.scale((self.screen),(640,320)),(0,0))
		pygame.display.flip()
	def clear(self):
		self.screen.fill(self.black)
class CHIP8:
	def __init__(self,Rompath):
		self.memoryCHIP = [0] * 4096
		self.V = [0] * 16
		self.Stack = [0]*16
		self.SP = 0
		self.I = 0
		self.PC = 0x200
		self.Keys = [False for i in range(16)]
		self.loadMemoryChip(Rompath)
		self.loadFonts()
		self.screen = Screen()
		self.DT = 0
		self.ST = 0
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
		print(f"{opcode:0X}")
		c1 = opcode & 0X000F
		c2 = (opcode & 0X00F0) >>4
		c3 = (opcode & 0X0F00) >>8
		c4 = (opcode & 0XF000) >>12
		if(c4 == 0):
			if(c2 == 0XE and c1 == 0XE):
				if(self.SP > 0):
					self.SP = self.SP-1
					self.PC = self.Stack[self.SP]
			elif(c2 == 0XE):
				self.screen.clear()
		elif(c4 == 1 ):
			self.PC = opcode & 0X0FFF
			self.PC -= 2
		elif(c4 ==2):
			if (self.SP<15):
				self.Stack[self.SP] = self.PC
				self.SP = self.SP+1
				self.PC = opcode & 0X0FFF
				self.PC -=2
		elif(c4 == 3):
			if (self.V[c3] == opcode&0X00FF):
				self.PC = self.PC+2
		elif(c4 == 4):
			if(self.V[c3] != opcode&0X00FF):
				self.PC = self.PC+2
		elif(c4 == 5):
			if(self.V[c3] == self.V[c2]):
				self.PC = self.PC+2
		elif(c4 == 6):
			self.V[c3] = (opcode&0X00FF)
		elif(c4 == 7):
			self.V[c3] =  (opcode&0X00FF) + self.V[c3]
			print(self.V[c3])
		elif(c4 == 8):
			match c1:
				case 0:
					self.V[c3] = self.V[c2]
				case 1:
					self.V[c3] |= self.V[c2]
				case 2:
					self.V[c3] &= self.V[c2]
				case 3:
					self.V[c3] ^= self.V[c2]
				case 4:
					self.V[15] = 0
					if(self.V[c3]+self.V[c2] > 255):
						self.V[15]=1
					self.V[c3] += self.V[c2]
				case 5:
					self.V[15] = 0
					if(self.V[c3]>self.V[c2]):
						self.V[15]=1
					self.V[c3] -= self.V[c2]
				case 6:
					self.V[15] = self.V[c3] & 0X1
					self.V[c3] = (self.V[c3]>>1)
				case 7:
					self.V[15] = 0
					if(self.V[c2]>self.V[c3]):
						self.V[15] = 1
					self.V[c3] = self.V[c2] - self.V[c3]
				case 0XE:
					self.V[15] = self.V[c3]>>7
					self.V[15] = self.V[c3]<<1
		elif(c4 == 0XA):
			self.I = opcode & 0X0FFF
		elif(c4==0XB):
			self.PC = (opcode & 0X0FFF)+self.V[0]
		elif(c4 == 0XC):
			self.V[c3] = random.randint(0,255) & (opcode&0X00FF)
		elif(c4 == 0XD):
			self.draw(c3,c2,c1)
		elif(c4 == 0XE):
			if (c2 == 0x9):
				if(self.Keys[c3] == True):
					self.PC += 2
			elif(c2 == 0XA):
				if(self.Keys[c3] == False):
					self.PC+=2
		elif(c4 ==0XF):
			match opcode&0X00FF:
				case 0X07:
					self.V[c3] = self.DT
				case 0X0A:
					self.keypressed
					for idx,val in enumerate(self.Keys):
						if(val == True):
							self.V[c3] = idx
				case 0X15:
					self.DT = c3
				case 0X18:
					self.ST = c3
				case 0X1E:
					self.I+=self.V[c3]
				case 0X29:
					self.I= c3*5
				case 0X33:
					self.memoryCHIP[self.I] = self.V[c3] // 100 													
					self.memoryCHIP[self.I+1] = (self.V[c3] - (self.memoryCHIP[self.I] * 100)) // 10 					
					self.memoryCHIP[self.I+2] = self.V[c3] - self.memoryCHIP[self.I]*100 - self.memoryCHIP[self.I+1]*10
				case 0X55:
					for i in range(c3+1):
						self.memoryCHIP[self.I+i]=self.V[i]
				case 0X65:
					for i in range(c3+1):
						self.V[i] = self.memoryCHIP[self.I+i]
		self.PC = self.PC+2

	def keypressed(self):
		Keypressed =False
		while(Keypressed == False):
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:
						self.Keys[0x1] = 1
					elif event.key == pygame.K_2:
						self.Keys[0x2] = 1
					elif event.key == pygame.K_3:
						self.Keys[0x3] = 1
					elif event.key == pygame.K_4:
						self.Keys[0xC] = 1
					elif event.key == pygame.K_q:
						self.Keys[0x4] = 1
					elif event.key == pygame.K_w:
						self.Keys[0x5] = 1
					elif event.key == pygame.K_e:
						self.Keys[0x6] = 1
					elif event.key == pygame.K_r:
						self.Keys[0xD] = 1
					elif event.key == pygame.K_a:
						self.Keys[0x7] = 1
					elif event.key == pygame.K_s:
						self.Keys[0x8] = 1
					elif event.key == pygame.K_d:
						self.Keys[0x9] = 1
					elif event.key == pygame.K_f:
						self.Keys[0xE] = 1
					elif event.key == pygame.K_z:
						self.Keys[0xA] = 1
					elif event.key == pygame.K_x:
						self.Keys[0x0] = 1
					elif event.key == pygame.K_c:
						self.Keys[0xB] = 1
					elif event.key == pygame.K_v:
						self.Keys[0xF] = 1
					Keypressed = True
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_1:
						self.Keys[0x1] = 0
					elif event.key == pygame.K_2:
						self.Keys[0x2] = 0
					elif event.key == pygame.K_3:
						self.Keys[0x3] = 0
					elif event.key == pygame.K_4:
						self.Keys[0xC] = 0
					elif event.key == pygame.K_q:
						self.Keys[0x4] = 0
					elif event.key == pygame.K_w:
						self.Keys[0x5] = 0
					elif event.key == pygame.K_e:
						self.Keys[0x6] = 0
					elif event.key == pygame.K_r:
						self.Keys[0xD] = 0
					elif event.key == pygame.K_a:
						self.Keys[0x7] = 0
					elif event.key == pygame.K_s:
						self.Keys[0x8] = 0
					elif event.key == pygame.K_d:
						self.Keys[0x9] = 0
					elif event.key == pygame.K_f:
						self.Keys[0xE] = 0
					elif event.key == pygame.K_z:
						self.Keys[0xA] = 0
					elif event.key == pygame.K_x:
						self.Keys[0x0] = 0
					elif event.key == pygame.K_c:
						self.Keys[0xB] = 0
					elif event.key == pygame.K_v:
						self.Keys[0xF] = 0


	def draw(self,c3,c2,c1):
		self.V[15] = 0
		for i in range(c1):
			bytes = self.memoryCHIP[self.I+i]
			y = c2+i
			if (y>self.screen.screen.get_height()):
					y -= self.screen.screen.get_height()
			for t in range(8):
				x = c3+t
				if (x>self.screen.screen.get_width()):
					x -= self.screen.screen.get_width()
				byte = (bytes & (0x1<<(7-t))) >>(7-t)
				color = self.screen.screen.get_at((x, y))
				if(color == self.screen.black):
					color = 1
				elif(color == self.screen.white):
					color = 0
				byte = color ^ byte
				self.screen.screen.set_at((x,y),(255*byte,255*byte,255*byte))
				if (color ==1 and byte == 1):
					self.V[15] =1
	def Mainchip8(self):
		clock = pygame.time.Clock()
		running = True
		while running ==True:
		#gestion de l'interuption de la boucle
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
				self.executeopcode(self.opcode())
				self.screen.display()
								




			





main = CHIP8("Tetris [Fran Dachille, 1991].ch8")

test1 = (main.opcode() & 0x00F0) >> 4
print(f"{test1:0X}")
main.Mainchip8()
vx = 0XEE >> 7
vy = 127 <<1
print(f"{vx}")
print(f"{vy}")