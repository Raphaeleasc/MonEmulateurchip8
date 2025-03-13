import pygame
import random

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
		



main = CHIP8("Tetris [Fran Dachille, 1991].ch8")

test1 = (main.opcode() & 0x00F0) >> 4
print(f"{test1:0X}")