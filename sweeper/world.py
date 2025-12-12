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
        self.flags = 0

    def uncover(self):
        self.uncovered = True
        if self.type == "mine":
            return -self.value
        else:
            return self.value


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
                r = rng.random()
                #print(r, self.world.getMineValue(x+16*self.x, y+16*self.y))
                self.tiles[(x,y)] = Tile(x+16*self.x, y+16*self.y,self.world, r)

    def uncover(self, x:int, y:int):
        subChunkLoc = (x%16, y%16)
        if subChunkLoc in self.tiles:
            return self.tiles[subChunkLoc].uncover()

    def uncovered(self, x:int, y:int) -> bool:
        subChunkLoc = (x%16, y%16)
        return self.tiles[subChunkLoc].uncovered
    
    def flagged(self, x:int, y:int) -> bool:
        subChunkLoc = (x%16, y%16)
        return self.tiles[subChunkLoc].flags > 0


class World:
    BIOMELIST = ["nul", "jsp","feur", "non", "bril"]
    BIOMEDATA = {
        "nul": {"mineDensity": 0.1,"bg":(34, 139, 34)},
        "feur": {"mineDensity": 0.1,"bg":(70, 130, 180)},
        "non": {"mineDensity": 0.2,"bg":(255, 140, 0)},
        "bril": {"mineDensity": 0.3,"bg":(220, 20, 60)},
        "jsp": {"mineDensity": 0.4,"bg":(75, 0, 130)},
    }
    EMPTYTILE = pygame.image.load(f"assets/tiles/empty.png")
    FULLBG = pygame.image.load(f"assets/tiles/fullBG.png")

    def __init__(self, gameseed:int):
        self.gameseed = gameseed
        self.biomeGen = randomUtil.VoronoiGen(self.gameseed, 16)
        self.chunks = {}
        self.pendingUncover = []

    def tickPending(self):
        for pos in self.pendingUncover[0:min(10, len(self.pendingUncover))]:
            self.uncoverAt(pos[0], pos[1], True, 0)
        for i in range(min(10, len(self.pendingUncover))):
            self.pendingUncover.pop(0)
        

    def uncoverAt(self, x:int, y:int, spread:bool=True, depth:int=0):
        if depth > 10:
            self.pendingUncover.append((x,y))
            return
        chunkLoc = (x//16, y//16)
        if chunkLoc not in self.chunks:
            self.chunks[chunkLoc] = Chunk(chunkLoc[0], chunkLoc[1], self)
        chunk = self.chunks[chunkLoc]
        if not (chunk.uncovered(x,y) or chunk.flagged(x,y)):
            val = chunk.uncover(x, y)
            if val == 0 and spread:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx = x + dx
                        ny = y + dy
                        self.uncoverAt(nx, ny,True, depth+1)
            
        

    def getBiomeAt(self, x:int, y:int) -> float:
        return self.biomeGen.get_value(x, y,World.BIOMELIST)
    
    def getMineValue(self, x:int, y:int) -> int:
        if (x//16, y//16) in self.chunks.keys():
            return 1 if self.chunks[(x//16, y//16)].tiles[(x%16, y%16)].type == "mine" else 0
        else:
            rng = randomUtil.random.Random(randomUtil.coordinateRng(x//16, y//16, self.gameseed))
            tileIndex = (x % 16) * 16 + (y % 16)
            for _ in range(tileIndex):
                rng.random()
            val = rng.random()
            if val < World.BIOMEDATA[self.getBiomeAt(x, y)]["mineDensity"]:
                return 1
            return 0
        
    
    def handle_click_event(self, event: pygame.event.Event) -> bool:
        """Handle a single pygame event. Returns True if the button was clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN:
                return event.button
        return False
    

    def render(self, screen, camera):
        
        camPos = -camera.vector(0,0)
        renderCorner = (camPos // 32)*32
        #screen.blit(World.FULLBG, camera.vector(renderCorner[0], renderCorner[1]))
        for x in range(-32, screen.get_width()+32, 32):
           for y in range(-32, screen.get_height()+32, 32):
                corner = camera.vector(renderCorner[0]+x, renderCorner[1]+y)
                col = self.BIOMEDATA[self.getBiomeAt((renderCorner[0]+x)//32, (renderCorner[1]+y)//32)]["bg"]
                pygame.draw.rect(screen, col, (corner[0], corner[1], 32, 32))


        for x in range(0, screen.get_width()+512, 512):
            for y in range(0, screen.get_height()+512, 512):
                chunkLoc = ((renderCorner[0]+x)//512, (renderCorner[1]+y)//512)
                if chunkLoc in self.chunks:
                    for tilePos, tile in self.chunks[chunkLoc].tiles.items():
                        
                        
                        if not (tilePos[0]*32+chunkLoc[0]*512-renderCorner[0] in range(-32, screen.get_width()+32, 32) and tilePos[1]*32+chunkLoc[1]*512-renderCorner[1] in range(-32, screen.get_height()+32, 32)):
                            continue
                        if not tile.uncovered:
                            screen.blit(World.EMPTYTILE, camera.vector(tilePos[0]*32+chunkLoc[0]*512, tilePos[1]*32+chunkLoc[1]*512))
                            continue
                        
                        if tile.type == "empty":   
                            tileImage = pygame.image.load(f"assets/tiles/{tile.value}.png")
                        else:
                            tileImage = pygame.image.load(f"assets/tiles/mine.png")
                        screen.blit(tileImage, camera.vector(tilePos[0]*32+chunkLoc[0]*512, tilePos[1]*32+chunkLoc[1]*512))
                else:
                    for a in range(16):
                        for b in range(16):
                            screen.blit(World.EMPTYTILE, camera.vector(a*32+chunkLoc[0]*512, b*32+chunkLoc[1]*512))

