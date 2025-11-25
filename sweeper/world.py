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
            self.chunks[subchunk].generateTile(x, y, self.gameseed)
        

    def getBiomeAt(self, x:int, y:int) -> float:
        return self.biomeGen.get_value(x, y,World.BIOMELIST)
    
    def getMineValue(self, x:int, y:int) -> int:
        tileRng = randomUtil.random.Random(randomUtil.coordinateRng(x, y, self.gameseed))
        tileBiome = self.getBiomeAt(x, y)
        if tileRng.random() < World.BIOMEDATA[tileBiome]["mineDensity"]:
            return 1
        return 0
    

    def render(self, screen, camera):
        camPos = camera.vector(0,0)
        renderCorner = (camPos // 16 - 1)*16
        screen.blit(pygame.image.load("empty.png"), renderCorner)

    


w = World(42)
w.uncoverAt(0, 0)
        

