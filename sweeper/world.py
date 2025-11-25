import sweeper.randomUtil as randomUtil
import pygame

class Tile:
    def __init__(self, x:int, y:int, world:World):
        self.x = x
        self.y = y
        self.rng = randomUtil.random.Random(randomUtil.coordinateRng(x, y, world.gameseed))
        self.biome = world.getBiomeAt(self.x, self.y)
        self.type = "mine" if self.rng.random() < World.BIOMEDATA[self.biome]["mineDensity"] else "empty"
        self.value = 1 if self.type == "mine" else self.countAdjacentMines(x, y, world)


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

    def generateTile(self, x:int, y:int, gameseed:int):
        subchunk = (x%16, y%16)
        self.tiles[subchunk] = Tile(x, y, self.world)

c = Chunk(0, 0, None)

class World:
    BIOMELIST = ["nul", "jsp"]
    BIOMEDATA = {
        "nul": {"mineDensity": 0.05},
        "jsp": {"mineDensity": 0.15}
    }
    def __init__(self, gameseed:int, biomeScale: int=20):
        self.gameseed = gameseed
        self.biomeGen = randomUtil.VoronoiGen(self.gameseed, biomeScale)
        self.chunks = {}

    def uncoverAt(self, x:int, y:int):
        subchunk = (x%16, y%16)
        chunkLoc = (x//16, y//16)
        if chunkLoc not in self.chunks:
            self.chunks[chunkLoc] = Chunk(chunkLoc[0], chunkLoc[1], self)
        chunk = self.chunks[chunkLoc]
        if subchunk not in chunk.tiles:
            chunk.generateTile(x, y, self.gameseed)
        

    def getBiomeAt(self, x:int, y:int) -> float:
        return self.biomeGen.get_value(x, y,World.BIOMELIST)
    
    def getMineValue(self, x:int, y:int) -> int:
        tileRng = randomUtil.random.Random(randomUtil.coordinateRng(x, y, self.gameseed))
        tileBiome = self.getBiomeAt(x, y)
        if tileRng.random() < World.BIOMEDATA[tileBiome]["mineDensity"]:
            return 1
        return 0
    

    def render(self, screen, camera):
        emptytile = pygame.image.load(f"assets/tiles/empty.png")
        camPos = -camera.vector(0,0)
        renderCorner = (camPos // 32)*32
        for x in range(-32, screen.get_width()+32, 32):
            for y in range(-32, screen.get_height()+32, 32):
                screen.blit(emptytile, camera.vector(renderCorner[0]+x, renderCorner[1]+y))
        for x in range(-32, screen.get_width()+32, 512):
            for y in range(-32, screen.get_height()+32, 512):
                chunkLoc = ((renderCorner[0]+x)//512, (renderCorner[1]+y)//512)
                if chunkLoc in self.chunks:
                    for tilePos, tile in self.chunks[chunkLoc].tiles.items():
                        if tile.type == "empty" and tile.value == 0:   
                            tileImage = pygame.image.load(f"assets/tiles/{tile.value}.png")
                        else:
                            tileImage = pygame.image.load(f"assets/tiles/mine.png")
                        screen.blit(tileImage, camera.vector(tilePos[0]*32+chunkLoc[0]*512, tilePos[1]*32+chunkLoc[1]*512))
        

