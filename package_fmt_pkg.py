import struct,sys,os

def u8(file):
    return struct.unpack("B", file.read(1))[0]
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def u32(file):
    return struct.unpack("<I", file.read(4))[0]
def rR(f,o,l):#Read n Return, Takes file,offset,size returns data
    c = f.tell()
    f.seek(o)
    d = f.read(l)
    f.seek(c)
    return d

class PKG(object):
    def __init__(self):
        self.files = []
    def read(self,f):
        count = u32(f)
        mappings = []
        for _a in range(count+1):
            mappings.append([u32(f),u32(f)])
        for a in mappings:
            f.seek(a[0])
            self.files.append(f.read(a[1]))
pkg_file = open(sys.argv[1], "rb")
pkg_in = PKG()
pkg_in.read(pkg_file)
pkg_file.close()
outDir = str(sys.argv[1]+"_Extract/")
os.makedirs(outDir, exist_ok=True)
for idx,x in enumerate(pkg_in.files):
    if(x):
        fil = open(outDir + str("%04i" % idx) + ".bin",'wb')
        fil.write(x)
        fil.close()