import struct

def u32(block,index):
    return struct.unpack("<I", block[index:index+4])[0]
def w32(value):
    return struct.pack("<I", value)

def Multiply64(param_1, param_2):#Keep that value 64bit always(to conform python number)
    p1 = param_1 & 0xFFFFFFFFFFFFFFFF
    p2 = param_2 & 0xFFFFFFFFFFFFFFFF
    return (p1 * p2) & 0xFFFFFFFFFFFFFFFF
def InitSeedRNG(param):
    return ((param + 0xf3c) * 0x354cf + Multiply64(param - 0x348f,0x1234567)) & 0xFFFFFFFF
def SeedRNG(param_1):
    return Multiply64(param_1,0x71c3ab9) + 0x3941


def DecryptBlock(inputByte,seed):
    xorBlock = InitSeedRNG(seed)
    loopCount = 0x800
    if(len(inputByte)<loopCount):
        loopCount = len(inputByte)
    outputBytes = bytearray()
    for x in range(loopCount >> 2):
        inputValue = u32(inputByte,x*4)
        outputBytes.extend(w32((inputValue ^ xorBlock)&0xFFFFFFFF))
        xorBlock = SeedRNG(xorBlock)
    return outputBytes


    
    