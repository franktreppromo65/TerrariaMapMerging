from PIL import Image
from math import ceil
from TilesClass import *
from ProgressBar import *
import io
import zlib


# this code is based on this website:
# https://github.com/TruePikachu/terraria-map-dump/wiki/Map-File-Format#data-zlib-deflate-compressed-data

def printBytes(bs):
    for b in bs:
        print(format(b,'08b'))
    return bs

def readUntilEndAndPrintCount():
    count = 0
    value = mapp.read(1)
    while value:
        value = mapp.read(1)
        count += 1
    print('bytes left in file : ', count)

print('_________________________________START______________________________________')
## smallworld
# mapPath = 'C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/18be9e33-57de-405a-9055-796f8f31bd37.map'
## mediumWorld
# mapPath = "C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/d7eb393e-d9c2-4115-a3cc-f3ed26664c20.map"
## morty's world
mapPath = "C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/dcc60b2c-3dca-4480-a511-01d184e91535 - Copy.map"

mapp = open(mapPath,'rb')


fileVersion = mapp.read(4)
magicRelogic = mapp.read(7)
magic = mapp.read(1)
revision = mapp.read(4)
fav = mapp.read(8)
nameLength = int.from_bytes(mapp.read(1),'little')
mapName = [b'0']*(nameLength)
count = 0
while count < nameLength :
    char = mapp.read(1)
    mapName[count] = char
    count +=1
worldID = mapp.read(4)
height = bytearray(mapp.read(4))
width = bytearray(mapp.read(4))
heightInt = int.from_bytes(height,"little")
widthInt = int.from_bytes(width,'little')
nbTiles = mapp.read(2)
nbWalls = mapp.read(2)
nbLiquids = mapp.read(2)
nbSkyShade = mapp.read(2)
nbDirtTypes = mapp.read(2)
nbRockTypes = mapp.read(2)
print('fileVersion : ', fileVersion[0], '.', fileVersion[1], '.', fileVersion[2], '.', fileVersion[3])
print(str(magicRelogic).replace("b'",'').replace("',",'').replace('b"','').replace('",','').replace("'",''))
print('magic : ',int.from_bytes(magic,'little'))
print('revision : ', int.from_bytes(bytearray(revision),'little'))
print('isFavorite : ', int.from_bytes(bytearray(fav),'little'))
print('nameLength : ', nameLength)
print(str(mapName).replace("b'",'').replace("',",'').replace('b"','').replace('",',''))
print('world ID : ', int.from_bytes(bytearray(worldID),'little'))
print('height : ',heightInt)
print('width : ',widthInt)
print('total Tiles To Read : ', heightInt*widthInt)
print("nb of tiles: "+str(int.from_bytes(nbTiles,'little')))
print("nb of Walls: "+str(int.from_bytes(nbWalls,'little')))
print("nb of Liquids: "+str(int.from_bytes(nbLiquids,'little')))
print("nb of SkyShade: "+str(int.from_bytes(nbSkyShade,'little')))
print("nb of DirtTypes: "+str(int.from_bytes(nbDirtTypes,'little')))
print("nb of RockTypes: "+str(int.from_bytes(nbRockTypes,'little')))



# nbTiles = int.from_bytes(nbTiles, 'little')
# nbWalls = int.from_bytes(nbWalls, 'little')

# def iter_bits(bytes_obj):
#             for byte in bytes_obj:
#                 for n in (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80):
#                     yield byte&n==n
# tile_has_multiple_options = mapp.read(math.ceil(nbTiles/8))
# wall_has_multiple_options = mapp.read(math.ceil(nbWalls/8))
# tile_option_count = [(mapp.read(1)[0] if has_mo else 1) for i,has_mo in zip(range(nbTiles),iter_bits(tile_has_multiple_options))]
# wall_option_count = [(mapp.read(1)[0] if has_mo else 1) for i,has_mo in zip(range(nbTiles),iter_bits(wall_has_multiple_options))]


tileIDCountInt = int.from_bytes(nbTiles, 'little')
wallIDCountInt = int.from_bytes(nbWalls, 'little')
print("tileidcount: ",tileIDCountInt)
print("wallidcount: ",wallIDCountInt)


bytesToReadTile = ceil(tileIDCountInt/8)
bytesToReadWall = ceil(wallIDCountInt/8)
tileIDMultipleOptionsArray = [None]*tileIDCountInt
wallIDMultipleOptionsArray = [None]*wallIDCountInt
print('bytes to read for tile : ', bytesToReadTile)
print('bytes to read for wall : ', bytesToReadWall)


masks = [None]*8
masks[0] = mask1
masks[1] = mask2
masks[2] = mask3
masks[3] = mask4
masks[4] = mask5
masks[5] = mask6
masks[6] = mask7
masks[7] = mask8

tileWithOptionsCount = 0
wallWithOptionsCount = 0

for i in range(bytesToReadTile):
    byte = mapp.read(1)[0]
    for bit in range(8):
        if (i*8)+bit >= tileIDCountInt :
            break
        value = (masks[bit] & byte) >> bit
        tileIDMultipleOptionsArray[(i*8)+bit] = value
        if value:
            tileWithOptionsCount += 1

for i in range(bytesToReadWall):
    byte = mapp.read(1)
    byte = int.from_bytes(byte,'little')
    for bit in range(8):
        if (i*8)+bit >= wallIDCountInt :
            break
        value = (masks[bit] & byte) >> bit
        wallIDMultipleOptionsArray[(i*8)+bit] = value
        if value:
            wallWithOptionsCount += 1

print("tile with options : ", tileWithOptionsCount)
print("wall with otpions : ", wallWithOptionsCount)
# print(tileIDMultipleOptionsArray)
# print(wallIDMultipleOptionsArray)

tileWithOptionsIDAndNumberOfOptions = []
wallWithOptionsIDAndNumberOfOptions = []
for ID,value in enumerate(tileIDMultipleOptionsArray):
    if value:
        tileWithOptionsIDAndNumberOfOptions.append((ID,mapp.read(1)[0]))
for ID,value in enumerate(wallIDMultipleOptionsArray):
    if value:
        wallWithOptionsIDAndNumberOfOptions.append((ID,mapp.read(1)[0]))


print("decompressing Data")

# https://www.delftstack.com/howto/python/python-zlib/#:~:text=of%20the%20data.-,Decompress%20Data%20With%20the%20zlib.,%3B%20data%20%2C%20wbits%20%2C%20and%20bufsize
uncompressedData = io.BytesIO(zlib.decompress(mapp.read(),wbits=-15))
mapp.close()
print("decoding tiles")
newTilesCovered = 0
tiles = []
while True:
    try :
        data = uncompressedData.read(1)[0]
    except:
        # eof
        break

    printInfo = True
    
        

    tileHeader = TileHeader(data,uncompressedData, False)
    firstTile = Tile(tileHeader,True)
    tiles.append(firstTile)

    #if RLE was used, the light level was saved, and the tile isn't Unknown,
    #  a number of extra BYTEs are read, corresponding to the light level for each RLE-duplicated tile, in order."""
    for i in range(tileHeader.RLECount): # fear each extre tiles, and if RLE is used is already defined in class
        tiles.append(Tile(tileHeader,False)) # light level saved check is done in class as well as for the unknown type
        
        if printInfo:
            UpdateProgress(len(tiles),heightInt*widthInt)
        #updating ProgressBar for each segments (realy not efficient, it was used just for testing)
        # UpdateProgress(i,tileHeader.RLECount)
    
print('')
print('')
print('length of tile list : ',len(tiles))

def GetColor(classification):
    options = { 0b000   :   (0,0,0),
                0b001   :   (200,200,100),
                0b010   :   (50,50,50),
                0b011   :   (0,0,128),
                0b100   :   (255,100,100),
                0b101   :   (100,255,255),
                0b110   :   (100,100,255),
                0b111   :   (100,200,200),}
    return options.get(classification)


img = Image.new('RGB',(widthInt,heightInt), color = (0,0,0))
x = 0
y = 0
for tile in tiles:
    light = tile.lightLevel/255.0
    colors = GetColor(tile.tileClassification)
    for c in colors:
        c *= light
    
    
    img.putpixel((x,y),colors)
    x += 1
    if x == widthInt:
        y += 1
        x = 0


img.show()
img.save('lightmap.png')


quit()



# for reference -> 
# 
# bitwise operations
# https://www.devdungeon.com/content/working-binary-data-python

# https://www.onlinehexeditor.com/#


