import sys,struct,os
import tttCript

def u32(file):
    return struct.unpack("<I", file.read(4))[0]
def s16(file):
    return struct.unpack("<h", file.read(2))[0]
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def u8(file):
    return struct.unpack("B", file.read(1))[0]

TABLESTART = 0x1CAD40
TABLECOUNT = 748

class LUT(object):
    def __init__(self):
        self.offset = 0
        self.size = 0
        self.flags = 0
        self.id = 0
        self.unk2 = -1
        self.unk3 = 0
    def read(self,f):
        self.offset = (u32(f)-0x4820)*0x800
        self.size = (u32(f)-0x350a)
        self.flags = u16(f)
        self.id = u16(f)
        self.unk2 = u16(f)
        self.unk3 = u16(f)
f = open(sys.argv[1],'rb')
f.seek(TABLESTART)
lookups = []
for x in range(TABLECOUNT):
    cur = LUT()
    cur.read(f)
    lookups.append(cur)
f.close()
total = 0
offsets = []
fbin = open(sys.argv[2],'rb')
outDir = str(sys.argv[2]+"_Extract/")
os.makedirs(outDir, exist_ok=True)
for indx,x in enumerate(lookups):
    if(x.size):
        fbin.seek(x.offset)
        fil = open(outDir + str("%04i_%04x" % (indx,x.unk2)) + ".bin",'wb')
        dataOG = fbin.read(x.size)
        if(x.size > 0x800):
            header = dataOG[:0x800]
        else:
            header = dataOG
        if(x.unk2 != 0xFFFF):
            decrypted = tttCript.DecryptBlock(header,x.unk2)
            data = bytearray()
            data.extend(decrypted)
            if(x.size > 0x800):
                data.extend(dataOG[0x800:])
        else:
            data = dataOG
        
        fil.write(data)
    

#print(hex(total))
