import pygame as pg
import random

#Chemin de fichier a émuler
PATH = "Tetris [Fran Dachille, 1991].ch8"

class Screen:
	def __init__(self):
		self.sound = pg.mixer.Sound("hey_listen.wav")
		self.grandscreen = pg.display.set_mode((860,320),pg.RESIZABLE)
		self.screen = pg.Surface((64,32))
		self.virtualpad = pg.Surface((220,320))
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.screen.fill(self.black)
		self.virtualpad.fill(self.white)
		self.font = pg.font.SysFont("arial",32)
		self.keys = {
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
		self.Virtualrect = [pg.Rect(0,0,0,0)]*16

	def updatvirtualpad(self):
		for i,(k,v) in enumerate(self.keys.items()):
				virtualbutton = pg.Surface((55,80))
				text = self.font.render(k,True,self.white)
				virtualbutton.blit(text,(55/2-text.get_width()/2,0))
				text = self.font.render(pg.key.name(v),True,self.white)
				virtualbutton.blit(text,(55/2-text.get_width()/2,32))
				self.Virtualrect[i] = self.virtualpad.blit(virtualbutton,(55*(i%4),80*(i//4)))
	def display(self):
		self.updatvirtualpad()
		self.grandscreen.blit(pg.transform.scale((self.screen),(640,320)),(0,0))
		self.grandscreen.blit(self.virtualpad,(640,0))
		pg.display.flip()
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
		self.Keys = [0 for i in range(16)]
		self.loadMemoryChip(Rompath)
		self.loadFonts()
		self.screen = Screen()
		self.DT = 0
		self.ST = 0
		self.clock = pg.time.Clock()
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
		c1 = opcode & 0X000F
		c2 = (opcode & 0X00F0) >>4
		c3 = (opcode & 0X0F00) >>8
		c4 = (opcode & 0XF000) >>12
		self.V[c3] = self.V[c3] % (2**8)
		self.V[c2] = self.V[c2] % (2**8)
		match c4:
			case 0:
				if(c2 == 0XE and c1 == 0XE):
					if(self.SP > 0):
						self.SP = self.SP-1
						self.PC = self.Stack[self.SP]
				elif(c2 == 0XE):
					self.screen.clear()
			case 1:
				self.PC = opcode & 0X0FFF
				self.PC -= 2
			case 2:
				if (self.SP<15):
					self.Stack[self.SP] = self.PC
					self.SP = self.SP+1
					self.PC = opcode & 0X0FFF
					self.PC -=2
			case 3:
				if (self.V[c3] == opcode&0X00FF):
					self.PC = self.PC+2
			case 4:
				if(self.V[c3] != opcode&0X00FF):
					self.PC = self.PC+2
			case 5:
				if(self.V[c3] == self.V[c2]):
					self.PC = self.PC+2
			case 6:
				self.V[c3] = (opcode&0X00FF)
			case 7:
				self.V[c3] =  (opcode&0X00FF) + self.V[c3]
			case 8:
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
						self.V[c3] = self.V[c3]<<1
			case 9:
				if(self.V[c3] != self.V[c2]):
					self.PC = self.PC+2	
			case 0XA:
				self.I = opcode & 0X0FFF
			case 0XB:
				self.PC = (opcode & 0X0FFF)+self.V[0]
			case 0XC:
				self.V[c3] = random.randint(0,255) & (opcode&0X00FF)
			case 0XD:
				self.draw(self.V[c3],self.V[c2],c1)
			case 0XE:
				if (c2 == 0x9):
					if(self.Keys[c3] == 1):
						self.PC += 2
				elif(c2 == 0XA):
					if(self.Keys[c3] == 0):
						self.PC+=2
			case 0XF:
				match opcode&0X00FF:
					case 0X07:
						self.V[c3] = self.DT
					case 0X0A:
						wait = 0
						while wait == 1:
							self.listen()
							for idx,val in enumerate(self.Keys):
								if(val == 1):
									self.V[c3] = idx
									wait = 1
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
	def listen(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.running = False
			elif event.type == self.DELAYSOUNDTIMER:
				if self.ST>0:
					self.ST -= 1
				self.playSound()
				if self.DT > 0:
					self.DT -=1
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.running = False
			keys = pg.key.get_pressed()
			for i, l in enumerate("1234azerqsdfwxcv"):
				self.Keys[i] = keys[self.screen.keys[l]]
			if pg.mouse.get_pressed()[0]:
				x,y = pg.mouse.get_pos()
				collide = pg.Rect((x-self.screen.screen.get_width()*10,y),(1,1)).collidelist(self.screen.Virtualrect)
				print(self.screen.Virtualrect)
				if collide != -1:
					while not (e:=pg.event.get(pg.KEYUP)): pass
					self.screen.keys["1234azerqsdfwxcv"[collide]] = e[0].key
				

	def playSound(self):
		if pg.mixer.get_busy() and self.ST<=0:
			self.screen.sound.stop()
		elif not pg.mixer.get_busy() and self.ST>0:
			self.screen.sound.play(-1)

	def draw(self,c3,c2,c1):
		self.V[15] = 0
		for i in range(c1):
			bytes = self.memoryCHIP[self.I+i]
			y = c2+i
			y %= self.screen.screen.get_height()
			for t in range(8):
				x = c3+t
				x %= self.screen.screen.get_width()
				byte = (bytes & (0x1<<(7-t))) >>(7-t)
				color = self.screen.screen.get_at((x, y))
				if(color == self.screen.black):
					color = 0
				elif(color == self.screen.white):
					color = 1
				if (color ==1 and byte == 1):
					self.V[15] =1
				byte = color ^ byte
				self.screen.screen.set_at((x,y),(255*byte,255*byte,255*byte))
	def Mainchip8(self):
		self.running = True
		self.DELAYSOUNDTIMER = 1
		pg.time.set_timer(self.DELAYSOUNDTIMER, round((1/60)*1000))
		while self.running ==True:
		#gestion de l'interuption de la boucle
			self.listen()
			self.executeopcode(self.opcode())
			self.screen.display()
			self.clock.tick(60*8)
								




			





pg.init()
main = CHIP8(PATH)

main.Mainchip8()
