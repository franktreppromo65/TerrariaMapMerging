from email import header
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





class Tmap:
    def Merge2Maps(mapp1, mapp2, printInfo = True):
        mappMerged = mapp1
        tileIndex = 0
        x = 0
        y = 0
        for tile in mapp1.tiles:
            if printInfo:
                UpdateProgress(x+y*mapp1.widthInt,mapp1.heightInt*mapp1.widthInt)

            tileMap1 = tile
            tileMap2 = mapp2.tiles[tileIndex]
            tileMapMerged = tileMap1

            if tileMap1 != tileMap2:
                if tileMap2.tileClassification != 0b000:
                    tileMapMerged = tileMap2

            mappMerged.tiles[tileIndex] = tileMapMerged

            tileIndex+=1
            x += 1
            if x == mapp1.widthInt:
                y += 1
                x = 0

        return mappMerged

    def __init__(self, mapp):

        self.printInfo = True
        self.UnPackHeader(mapp)
        self.DecodeTiles(mapp)
        self.GenerateImageFromSelf()
            
        
    def UnPackHeader(self, mapp):

        self.fileVersion = mapp.read(4)
        self.magicRelogic = mapp.read(7)
        self.magic = mapp.read(1)
        self.revision = mapp.read(4)
        self.fav = mapp.read(8)
        self.nameLength = int.from_bytes(mapp.read(1),'little')
        self.mapName = mapp.read(self.nameLength)
        self.worldID = mapp.read(4)
        self.height = bytearray(mapp.read(4))
        self.width = bytearray(mapp.read(4))
        self.heightInt = int.from_bytes(self.height,"little")
        self.widthInt = int.from_bytes(self.width,'little')
        self.nbTiles = mapp.read(2)
        self.nbWalls = mapp.read(2)
        self.nbLiquids = mapp.read(2)
        self.nbSkyShade = mapp.read(2)
        self.nbDirtTypes = mapp.read(2)
        self.nbRockTypes = mapp.read(2)
        print('fileVersion : ', self.fileVersion[0], '.', self.fileVersion[1], '.', self.fileVersion[2], '.', self.fileVersion[3])
        print('relogic : ', self.magicRelogic.decode("utf-8"))
        print('magic : ',int.from_bytes(self.magic,'little'))
        print('revision : ', int.from_bytes(bytearray(self.revision),'little'))
        print('isFavorite : ', int.from_bytes(bytearray(self.fav),'little'))
        print('nameLength : ', self.nameLength)
        print('worldName : ', self.mapName.decode('utf-8'))
        print('world ID : ', int.from_bytes(bytearray(self.worldID),'little'))
        print('height : ',self.heightInt)
        print('width : ',self.widthInt)
        print('total Tiles To Read : ', self.heightInt*self.widthInt)
        print("nb of tiles: "+str(int.from_bytes(self.nbTiles,'little')))
        print("nb of Walls: "+str(int.from_bytes(self.nbWalls,'little')))
        print("nb of Liquids: "+str(int.from_bytes(self.nbLiquids,'little')))
        print("nb of SkyShade: "+str(int.from_bytes(self.nbSkyShade,'little')))
        print("nb of DirtTypes: "+str(int.from_bytes(self.nbDirtTypes,'little')))
        print("nb of RockTypes: "+str(int.from_bytes(self.nbRockTypes,'little')))



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


        self.tileIDCountInt = int.from_bytes(self.nbTiles, 'little')
        self.wallIDCountInt = int.from_bytes(self.nbWalls, 'little')
        print("tileidcount: ",self.tileIDCountInt)
        print("wallidcount: ",self.wallIDCountInt)


        self.bytesToReadTile = ceil(self.tileIDCountInt/8)
        self.bytesToReadWall = ceil(self.wallIDCountInt/8)
        self.tileIDMultipleOptionsArray = [None]*self.tileIDCountInt
        self.wallIDMultipleOptionsArray = [None]*self.wallIDCountInt
        print('bytes to read for tile : ', self.bytesToReadTile)
        print('bytes to read for wall : ', self.bytesToReadWall)


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

        for i in range(self.bytesToReadTile):
            byte = mapp.read(1)[0]
            for bit in range(8):
                if (i*8)+bit >= self.tileIDCountInt :
                    break
                value = (masks[bit] & byte) >> bit
                self.tileIDMultipleOptionsArray[(i*8)+bit] = value
                if value:
                    tileWithOptionsCount += 1

        for i in range(self.bytesToReadWall):
            byte = mapp.read(1)
            byte = int.from_bytes(byte,'little')
            for bit in range(8):
                if (i*8)+bit >= self.wallIDCountInt :
                    break
                value = (masks[bit] & byte) >> bit
                self.wallIDMultipleOptionsArray[(i*8)+bit] = value
                if value:
                    wallWithOptionsCount += 1

        print("tile with options : ", tileWithOptionsCount)
        print("wall with otpions : ", wallWithOptionsCount)
        # print(tileIDMultipleOptionsArray)
        # print(wallIDMultipleOptionsArray)

        self.tileWithOptionsIDAndNumberOfOptions = []
        self.wallWithOptionsIDAndNumberOfOptions = []
        for ID,value in enumerate(self.tileIDMultipleOptionsArray):
            if value:
                self.tileWithOptionsIDAndNumberOfOptions.append((ID,mapp.read(1)[0]))
        for ID,value in enumerate(self.wallIDMultipleOptionsArray):
            if value:
                self.wallWithOptionsIDAndNumberOfOptions.append((ID,mapp.read(1)[0]))


    def PackHeader(self, file):
        file.write(self.fileVersion)
        file.write(self.magicRelogic)
        file.write(self.magic)
        file.write(self.revision)
        file.write(self.fav)
        file.write(self.nameLength.to_bytes(1,'little'))
        file.write(self.mapName)
        file.write(self.worldID)
        file.write(self.height)
        file.write(self.width)
        file.write(self.nbTiles)
        file.write(self.nbWalls)
        file.write(self.nbLiquids)
        file.write(self.nbSkyShade)
        file.write(self.nbDirtTypes)
        file.write(self.nbRockTypes)

        for i in range(self.bytesToReadTile):
            byte = 0
            for bit in range(8):
                if (i*8)+bit >= self.tileIDCountInt :
                    break
                value = self.tileIDMultipleOptionsArray[(i*8)+bit]
                byte |= (value<<bit)
            file.write(byte.to_bytes(1,'little'))

        for i in range(self.bytesToReadWall):
            byte = 0
            for bit in range(8):
                if (i*8)+bit >= self.wallIDCountInt :
                    break
                value = self.wallIDMultipleOptionsArray[(i*8)+bit]
                byte |= (value<<bit)
            file.write(byte.to_bytes(1,'little'))

        count = 0
        for ID,value in enumerate(self.tileWithOptionsIDAndNumberOfOptions):
            byte = self.tileWithOptionsIDAndNumberOfOptions[count]
            file.write(byte[1].to_bytes(1,'little'))
            count +=1
        count = 0
        for ID,value in enumerate(self.wallWithOptionsIDAndNumberOfOptions):
            byte = self.wallWithOptionsIDAndNumberOfOptions[count]
            file.write(byte[1].to_bytes(1,'little'))
            count +=1
        return


    def DecodeTiles(self, mapp):
        

        print("decompressing Data")
        # https://www.delftstack.com/howto/python/python-zlib/#:~:text=of%20the%20data.-,Decompress%20Data%20With%20the%20zlib.,%3B%20data%20%2C%20wbits%20%2C%20and%20bufsize
        uncompressedData = io.BytesIO(zlib.decompress(mapp.read(),wbits=-15))
        mapp.close()
        print("decoding tiles")
        newTilesCovered = 0
        self.tiles = []
        while True:
            try :
                data = uncompressedData.read(1)[0]
            except:
                # eof
                break
            
            tileHeader = TileHeader(data,uncompressedData, False)
            firstTile = Tile(tileHeader,True)
            self.tiles.append(firstTile)

            #if RLE was used, the light level was saved, and the tile isn't Unknown,
            #  a number of extra BYTEs are read, corresponding to the light level for each RLE-duplicated tile, in order."""
            for i in range(tileHeader.RLECount): # fear each extre tiles, and if RLE is used is already defined in class
                self.tiles.append(Tile(tileHeader,False)) # light level saved check is done in class as well as for the unknown type
                
                if self.printInfo:
                    UpdateProgress(len(self.tiles),self.heightInt*self.widthInt)
                #updating ProgressBar for each segments (realy not efficient, it was used just for testing)
                # UpdateProgress(i,tileHeader.RLECount)
        return

    def EncodeTiles(self, file):
        print("encoding tiles")
        encodedTiles = ''

        # TODO, inversing the encoding
        
        newTilesCovered = 0
        self.tiles = []
        while True:
            try :
                data = uncompressedData.read(1)[0]
            except:
                # eof
                break
            
            tileHeader = TileHeader(data,uncompressedData, False)
            firstTile = Tile(tileHeader,True)
            self.tiles.append(firstTile)

            #if RLE was used, the light level was saved, and the tile isn't Unknown,
            #  a number of extra BYTEs are read, corresponding to the light level for each RLE-duplicated tile, in order."""
            for i in range(tileHeader.RLECount): # fear each extre tiles, and if RLE is used is already defined in class
                self.tiles.append(Tile(tileHeader,False)) # light level saved check is done in class as well as for the unknown type
                
                if self.printInfo:
                    UpdateProgress(len(self.tiles),self.heightInt*self.widthInt)
                #updating ProgressBar for each segments (realy not efficient, it was used just for testing)
                # UpdateProgress(i,tileHeader.RLECount)


        print("compressing Data")
        # https://www.delftstack.com/howto/python/python-zlib/#:~:text=of%20the%20data.-,Decompress%20Data%20With%20the%20zlib.,%3B%20data%20%2C%20wbits%20%2C%20and%20bufsize
        uncompressedData = io.BytesIO(zlib.compress(encodedTiles,wbits=-15))
        
        

        return

    def GenerateImageFromSelf(self):
        print('')
        print('')
        print('generating image from tiles')

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

        img = Image.new('RGB',(self.widthInt,self.heightInt), color = (0,0,0))
        x = 0
        y = 0
        for tile in self.tiles:
            if self.printInfo:
                UpdateProgress(x+y*self.widthInt,self.heightInt*self.widthInt)

            light = tile.lightLevel/255.0
            colors = GetColor(tile.tileClassification)
            for c in colors:
                c *= light
            
            
            img.putpixel((x,y),colors)
            x += 1
            if x == self.widthInt:
                y += 1
                x = 0


        img.show()
        img.save('lightmap.png')
        return

    def GenerateImageFromMap(mapp):
        print('')
        print('')
        print('generating image from tiles')
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

        img = Image.new('RGB',(mapp.widthInt,mapp.heightInt), color = (0,0,0))
        x = 0
        y = 0
        for tile in mapp.tiles:
            if mapp.printInfo:
                UpdateProgress(x+y*mapp.widthInt,mapp.heightInt*mapp.widthInt)

            light = tile.lightLevel/255.0
            colors = GetColor(tile.tileClassification)
            for c in colors:
                c *= light
            
            
            img.putpixel((x,y),colors)
            x += 1
            if x == mapp.widthInt:
                y += 1
                x = 0


        img.show()
        img.save('lightmapMerged.png')
        return

# for reference -> 
# 
# bitwise operations
# https://www.devdungeon.com/content/working-binary-data-python

# https://www.onlinehexeditor.com/#


