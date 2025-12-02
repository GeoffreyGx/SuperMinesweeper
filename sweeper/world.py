import sweeper.randomUtil as randomUtil
import pygame

class Tile:
    def __init__(self, x:int, y:int, world:World,val:float):
        self.x = x
        self.y = y
        self.biome = world.getBiomeAt(self.x, self.y)
        self.type = "mine" if val < World.BIOMEDATA[self.biome]["mineDensity"] else "empty"
        self.value = 1 if self.type == "mine" else self.countAdjacentMines(x, y, world)
        self.uncovered = False

    def uncover(self):
        self.uncovered = True


    def countAdjacentMines(self, x:int, y:int, world:World) -> int:
        mineCount = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                mineCount += world.getMineValue(nx, ny)
        return mineCount
        



class Chunk:
    def __init__(self, x:int, y:int,world:World):
        self.x = x
        self.y = y
        self.tiles = {}
        self.world = world
        self.generateTiles(world.gameseed)

    def generateTiles(self, gameseed:int):
        rng = randomUtil.random.Random(randomUtil.coordinateRng(self.x, self.y, gameseed))
        for x in range(16):
            for y in range(16):  
                self.tiles[(x,y)] = Tile(x+self.x, y+self.y, self.world,rng.random())

    def uncover(self, x:int, y:int):
        subChunkLoc = (x%16, y%16)
        if subChunkLoc in self.tiles:
            self.tiles[subChunkLoc].uncover()

    def uncovered(self, x:int, y:int) -> bool:
        subChunkLoc = (x%16, y%16)
        return self.tiles[subChunkLoc].uncovered


class World:
    BIOMELIST = ["nul", "jsp"]
    BIOMEDATA = {
        "nul": {"mineDensity": 0.05},
        "jsp": {"mineDensity": 0.15}
    }
    EMPTYTILE = pygame.image.load(f"assets/tiles/empty.png")
    FULLBG = pygame.image.load(f"assets/tiles/fullBG.png")

    def __init__(self, gameseed:int):
        self.gameseed = gameseed
        self.biomeGen = randomUtil.VoronoiGen(self.gameseed, 16)
        self.chunks = {}

    def uncoverAt(self, x:int, y:int):
        chunkLoc = (x//16, y//16)
        if chunkLoc not in self.chunks:
            self.chunks[chunkLoc] = Chunk(chunkLoc[0], chunkLoc[1], self)
        chunk = self.chunks[chunkLoc]
        if not chunk.uncovered(x,y):
            chunk.uncover(x, y)
        

    def getBiomeAt(self, x:int, y:int) -> float:
        return self.biomeGen.get_value(x, y,World.BIOMELIST)
    
    def getMineValue(self, x:int, y:int) -> int:
        tileRng = randomUtil.random.Random(randomUtil.coordinateRng(x, y, self.gameseed))
        tileBiome = self.getBiomeAt(x, y)
        if tileRng.random() < World.BIOMEDATA[tileBiome]["mineDensity"]:
            return 1
        return 0
    

    def render(self, screen, camera):
        
        camPos = -camera.vector(0,0)
        renderCorner = (camPos // 32)*32
        screen.blit(World.FULLBG, camera.vector(renderCorner[0], renderCorner[1]))
        #screen.blit(fullBG, camera.vector(renderCorner[0], renderCorner[1]))
#        for x in range(-32, screen.get_width()+32, 32):
#            for y in range(-32, screen.get_height()+32, 32):
#                screen.blit(EMPTYTILE, camera.vector(renderCorner[0]+x, renderCorner[1]+y))
        for x in range(0, screen.get_width()+512, 512):
            for y in range(0, screen.get_height()+512, 512):
                chunkLoc = ((renderCorner[0]+x)//512, (renderCorner[1]+y)//512)
                if chunkLoc in self.chunks:
                    for tilePos, tile in self.chunks[chunkLoc].tiles.items():

                        if not tile.uncovered:
                            continue
                        
                        if not (tilePos[0]*32+chunkLoc[0]*512-renderCorner[0] in range(-32, screen.get_width()+32, 32) and tilePos[1]*32+chunkLoc[1]*512-renderCorner[1] in range(-32, screen.get_height()+32, 32)):
                            continue
                        
                        if tile.type == "empty":   
                            tileImage = pygame.image.load(f"assets/tiles/{tile.value}.png")
                        else:
                            tileImage = pygame.image.load(f"assets/tiles/mine.png")
                        screen.blit(tileImage, camera.vector(tilePos[0]*32+chunkLoc[0]*512, tilePos[1]*32+chunkLoc[1]*512))
        

