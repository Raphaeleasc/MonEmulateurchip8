
def decodeChip8(path):
    Text = open ("Text.txt","wt")
    with open(path, "rb") as f:
        romData = f.read()
    for i in range(0, len(romData), 2):
        Text.write(f"0x{0x200+i:03X}: {romData[i]<<8|romData[i+1]:04X} \n")

decodeChip8("Tetris [Fran Dachille, 1991].ch8")


memory = [0] * 4096