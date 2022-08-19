from html.entities import name2codepoint
from PIL import Image, ImageDraw
from math import ceil
from TilesClass import *
from ProgressBar import *

# this code is based on this website:
# https://github.com/TruePikachu/terraria-map-dump/wiki/Map-File-Format#data-zlib-deflate-compressed-data

def printBytes(bs):
    for b in bs:
        print(format(b,'08b'))
    return bs

print('_________________________________START______________________________________')
#smallworld
mapPath = 'C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/18be9e33-57de-405a-9055-796f8f31bd37.map'
#mediumWorld
# mapPath = "C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/d7eb393e-d9c2-4115-a3cc-f3ed26664c20.map"
#morty's world
# mapPath = "C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/dcc60b2c-3dca-4480-a511-01d184e91535 - Copy.map"

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


tileIDCountInt = int.from_bytes(nbTiles, 'little')
wallIDCountInt = int.from_bytes(nbWalls, 'little')
print("tileidcount: ",tileIDCountInt)
print("wallidcount: ",wallIDCountInt)

# stuck here

# bitArrayTileWithMultipleOptions = mapp.read(ceil(tileIDCountInt/8))
# bitArrayWallWithMultipleOptions = mapp.read(ceil(wallIDCountInt/8))

bytesRead = (ceil(tileIDCountInt/8) + ceil(wallIDCountInt/8))

print('bytes to read for tile : ', ceil(tileIDCountInt/8))
print('bytes to read for wall : ', ceil(wallIDCountInt/8))
print(bytesRead,' total')
n = 120
print(n," next bytes")
printBytes(bytearray(mapp.read(n)))
quit()

skip = mapp.read((189 - bytesRead))

# to here

print("decoding tiles")
newTilesCovered = 0
tiles = []
while True:
    data = mapp.read(1)
    if not data:
        # eof
        break
    # testing first1 bytes
    printInfo = True
    if printInfo:
        print("\n############################")
        print("tiles #",newTilesCovered)

    #if RLE was used, the light level was saved, and the tile isn't Unknown,
    #  a number of extra BYTEs are read, corresponding to the light level for each RLE-duplicated tile, in order."""

    tileHeader = TileHeader(data,mapp)
    firstTile = Tile(tileHeader,True)
    tiles.append(firstTile)
   
    for i in range(tileHeader.RLECount): # fear each extre tiles, and if RLE is used is already defined in class
        tiles.append(Tile(tileHeader,False)) # light level saved check is done in class as well as for the unknown type
        #updating ProgressBar
        UpdateProgress(i,tileHeader.RLECount)
    newTilesCovered +=1
print('')
print('')
print('length of tile list : ',len(tiles))


mapp.close()
quit()

testn = 500000
for i in range(testn):
    if not (i+1)%(testn/100):
        printProgressBar(i,testn,'',str(i+1) + '/' + str(testn) + ' tiles', length = 20)

print('')

img = Image.new('RGB',(widthInt,heightInt), color = (255,0,0))
# for reference -> 
# 
# bitwise operations
# https://www.devdungeon.com/content/working-binary-data-python

# https://www.onlinehexeditor.com/#


