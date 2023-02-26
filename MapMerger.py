from multiprocessing.pool import MapResult
import MAPReader


print('_________________________________START______________________________________')
## smallworld
mapPath = 'C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/18be9e33-57de-405a-9055-796f8f31bd37.map'
mapPathPlayer2 = "C:/Users/trepa/Documents/My Games/Terraria/Players/i_should_not/18be9e33-57de-405a-9055-796f8f31bd37.map"
## mediumWorld
# mapPath = "C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/d7eb393e-d9c2-4115-a3cc-f3ed26664c20.map"
## morty's world
# mapPath = "C:/Users/trepa/Documents/My Games/Terraria/Players/FrankOfFlesh_XD_QC_/dcc60b2c-3dca-4480-a511-01d184e91535 - Copy.map"

mapMergedPath = "C:/Users/trepa/Desktop/TerrariaMapMerging/testHeader.map"

map1 = open(mapPath,'rb')
map2 = open(mapPathPlayer2,'rb')

print('######## map 1 #########')
tmap1 = MAPReader.Tmap(map1)
print('######## map 2 #########')
tmap2 = MAPReader.Tmap(map2)

mergedFile = open('testHeader.map', 'wb')

mergedMapp = MAPReader.Tmap.Merge2Maps(tmap1,tmap2)
MAPReader.Tmap.GenerateImageFromMap(mergedMapp)

mergedMapp.PackHeader(mergedFile)
mergedMapp.EncodeTiles(mergedFile)

mergedFile.close()



# mapMerged = open(mapMergedPath, 'rb')
# tmapMerged = MAPReader.Tmap(mapMerged)