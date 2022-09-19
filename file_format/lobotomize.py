# Description: Modifies the ELF header to make it harder to reverse. Zeros out the start of section,
# size of section, number of section headers, and section header string table index values. 
# Additional options provided for setting endianness and class.
#
# Refs:
# https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html
# https://papers.vx-underground.org/papers/Linux/Evasion/Programming%20Linux%20Anti-Reversing%20Techniques.pdf

from os import chmod
import sys
import stat
import getopt


def error(s):
    print('[ERR]: ' + s)
    exit(-1)


def help():
    print(f"Usage: {sys.argv[0]} -f file_name [options]")
    print("     -e {'none', 'little', 'big'}    set endianness")
    print("     -c {'none', '32', '64'}         set class")
    print("     -o <name>                       set output file name")
    exit(0)

def tobyte(b):
    return b.to_bytes(1, byteorder='big')

argv = sys.argv[1:]
inFile = None
outFile = None
ei_class = None
CLASS = {'32':b'\x01', '64':b'\x02'}
ei_data = None
DATA = {'little':b'\x01', 'big':b'\x02'}


try:
    opts, args = getopt.getopt(argv, "hf:e:c:o:")
except:
    help()

for opt, arg in opts:
    if opt == '-h':
        help()
    if opt == '-f':
        inFile = arg
    elif opt == '-o':
        outFile = arg
    elif opt == '-c':
        if arg in CLASS:
            ei_class = CLASS[arg]
        else:
            error('bad class, expected one of {32, 64}, got '+arg)
    elif opt == '-e':
        if arg in DATA:
            ei_data = DATA[arg]
        else:
            error('bad endianness, expected one of {little, big}, got '+arg)

if inFile is None:
    help()

if outFile is None:
    outFile = inFile + "_fk"

flip_endian = 1

with open(inFile, 'rb') as inF, open(outFile, 'wb') as outF:
    buf = inF.read()

    # ELF magic number
    outF.write(b'\x7FELF')

    # EI_CLASS
    if ei_class is not None:
        outF.write(ei_class)
    else:
        outF.write(tobyte(buf[0x04]))

    # EI_DATA
    if ei_data is not None:
        if ei_data != buf[0x05]:
            flip_endian = -1
        outF.write(ei_data)
    else:
        outF.write(tobyte(buf[0x05]))

    # EI_VERSION EI_OSABI EI_ABIVERSION EI_PAD
    outF.write(buf[0x06:0x10])

    # e_type e_machine
    outF.write(buf[0x10:0x14])

    # e_version
    outF.write(buf[0x14:0x18][::flip_endian])
    
    # e_entry e_phoff
    outF.write(buf[0x18:0x28])
    
    # e_shoff
    outF.write(b'\x00'*8)

    # e_flags
    outF.write(buf[0x30:0x34])

    # e_ehsize
    outF.write(buf[0x34:0x36][::flip_endian])

    # e_phentsize e_phnum
    outF.write(buf[0x36:0x3a])
    
    # e_shentsize e_shentnum e_shstrndx
    outF.write(b'\x00'*6)

    # the rest of the binary
    outF.write(buf[0x40:])

chmod(outFile, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
print("done!")
