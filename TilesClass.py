


mask1 = int('0000 0001'.replace(' ',''), 2)
mask2 = int('0000 0010'.replace(' ',''), 2)
mask3 = int('0000 0100'.replace(' ',''), 2)
mask4 = int('0000 1000'.replace(' ',''), 2)
mask5 = int('0001 0000'.replace(' ',''), 2)
mask6 = int('0010 0000'.replace(' ',''), 2)
mask7 = int('0100 0000'.replace(' ',''), 2)
mask8 = int('1000 0000'.replace(' ',''), 2)






#####################################
#               TILES               #
#####################################
class Tile:
    """ only used if in tileHeader RLE count"""
    def __init__(self, TileHeader, isHeader):
        self.colorID = TileHeader.colorID
        self.specificTileType = TileHeader.tileTypeSpecific
        self.tileClassification = TileHeader.tileClassification
        self.tileLightIsSaved = TileHeader.tileLightIsSaved
        if isHeader:
            self.lightLevel = TileHeader.lightLevel
        else:
            self.lightLevel = self.GetLightLevel(TileHeader.mapFile,TileHeader.lightLevel)

    def GetLightLevel(self, mapFile, default):
        if self.tileLightIsSaved:
            return mapFile.read(1)[0]
        else:
            return default


class TileHeader:
    

    def __init__(self, data, mapFile, infoPrint):
        self.PrintInfo = infoPrint
        self.mapFile = mapFile

        self.data = data
        if self.PrintInfo:
            print('byte to decode : ',format(self.data,'08b'))

        self.ParseData()
        self.RetreiveInfoFromParsedData()
        if self.PrintInfo:
            self.PrintTileInfo()

        
    def ParseData(self):
        self.colorExist = (self.data & mask1)                           # has paint
        self.tileClassification = (self.data & (mask4|mask3|mask2))>> 1 # classification, see : GetTileClassificationTypeString()
        self.tileTypeFieldlengthIsWord = (self.data & mask5)>> 4        # word type
        self.tileLightIsSaved = (self.data & mask6)>> 5  # 255 otherwise
        self.RLESizeIsByte = (self.data & mask7)>> 6 # RLE is 1 byte
        self.RLESizeIsWord = (self.data & mask8) >> 7 # RLE is 2 bytes

        # self.colorExist = (self.data & mask8)>>7  
        # self.tileClassification = (self.data & (mask7|mask6|mask5))>> 4
        # self.tileTypeFieldlength = (self.data & mask4)>> 3 
        # self.tileLightIsSaved = (self.data & mask3)>> 2  # 255 otherwise
        # self.RLESizeIsByte = (self.data & mask2)>> 1 # RLE is 1 byte
        # self.RLESizeIsWord = (self.data & mask1) # RLE is 2 bytes

    def RetreiveInfoFromParsedData(self):

        self.GetColorID()
        self.GetSpecificTileType()
        self.GetLightLevel()
        self.GetRLECount()
      

    def GetColorID(self):
        """if it exists, the color ID for the tile is read.
         It is a BYTE, but left-shifted by one 
         (the low bit doesn't appear to be utilized at this time)."""
        if self.colorExist:
            self.colorID = int.from_bytes(self.mapFile.read(1),'little') >> 1
        else:
            self.colorID = 0

    def GetSpecificTileType(self):
        """if the map tile classification is either a tile, wall, dirt, or rock,
         a BYTE or WORD (depending on flags) is read to better specify the map tile type."""
        if self.tileClassification in {0b001, 0b010, 0b111}:
            if self.tileTypeFieldlengthIsWord:
                self.tileTypeSpecific = int.from_bytes(self.mapFile.read(2),'little')
            else:
                self.tileTypeSpecific = int.from_bytes(self.mapFile.read(1),'little')
        else:
            self.tileTypeSpecific = 0

    def GetLightLevel(self):
        """if the light level is saved,
         it is read (as a BYTE).
         But if Tile light level was not saved (assume 255, unless Unknown tile type)"""
        if self.tileLightIsSaved:
            self.lightLevel = self.mapFile.read(1)[0]
        elif self.tileClassification == 0b000:
            self.lightLevel = 0
        else:
            self.lightLevel = 255

    def GetRLECount(self):
        """ if a RLE count is saved, it is read (BYTE or WORD)."""
        if self.RLESizeIsByte or self.RLESizeIsWord:
            if self.RLESizeIsByte:
                self.RLECount = int.from_bytes(self.mapFile.read(1),'little')
            else :
                self.RLECount = int.from_bytes(self.mapFile.read(2),'little')
        else:
            self.RLECount = 0
    
    def PrintTileInfo(self):
        short = False
        if not short:
            print('')
            print('colorExist :', self.colorExist)
            print('colorID : ',self.colorID)
            print('')
            print('tileClassification : '+ self.GetTileClassificationTypeString())
            print('tileTypeFieldlengthIsWord : ', self.tileTypeFieldlengthIsWord)
            print('tileTypeSpecific : ',self.tileTypeSpecific)
            print('')
            print('lightIsSaved : ', self.tileLightIsSaved)
            print('lightLevel : ',self.lightLevel)
            print('')
            print('RLEIsByte : ',self.RLESizeIsByte)
            print('RLEIsWord : ', self.RLESizeIsWord)
            print('RLECount : ',self.RLECount)
        else:
            print('')
            print('colorID : ',self.colorID)

            print('tileTypeSpecific : ',self.tileTypeSpecific)

            print('lightLevel : ',self.lightLevel)
            
            print('RLECount : ',self.RLECount)
    def GetTileClassificationTypeString(self):
        options = { 0b000   :   'unknown',
                    0b001   :   'tile',
                    0b010   :   'wall',
                    0b011   :   'water',
                    0b100   :   'lava',
                    0b101   :   'honey',
                    0b110   :   'sky or hell',
                    0b111   :   'dirt or rock',}
        return str(options.get(self.tileClassification))
