import sweeper.randomUtil as randomUtil
import pygame




class Tile:
    def __init__(self, x:int, y:int, world:World,val:float):
        self.x = x
        self.y = y
        self.biome = world.getBiomeAt(self.x, self.y)
        # Determine tile type based on mine density
        self.type = "mine" if val < getbiomedata(self.biome,"mineDensity") else "empty"
        # For mines, value is 1; for empty tiles, count adjacent mines

        mines = world.getMineValue(x, y)



        self.value = mines if self.type == "mine" else self.countAdjacentMines(x, y, world)
        self.uncovered = False
        self.flags = 0

    def uncover(self):
        """Reveal tile and return value (-value for mines, count for empty)."""
        self.uncovered = True
        if self.type == "mine":
            return -self.value
        else:
            return self.value

    def countAdjacentMines(self, x:int, y:int, world:World) -> int:
        """Count mines in 8 adjacent tiles."""
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
    """16x16 grid of tiles (512x512 pixels)."""
    def __init__(self, x:int, y:int,world:World):
        self.x = x
        self.y = y
        self.tiles = {}
        self.world = world
        self.generateTiles(world.gameseed)

    def generateTiles(self, gameseed:int):
        """Generate tiles using seeded RNG for deterministic placement."""
        rng = randomUtil.random.Random(randomUtil.coordinateRng(self.x, self.y, gameseed))
        for x in range(16):
            for y in range(16):
                r = rng.random()
                self.tiles[(x,y)] = Tile(x+16*self.x, y+16*self.y,self.world, r)

    def uncover(self, x:int, y:int):
        """Uncover tile at local chunk coordinates."""
        subChunkLoc = (x%16, y%16)
        if subChunkLoc in self.tiles:
            return self.tiles[subChunkLoc].uncover()

    def uncovered(self, x:int, y:int) -> bool:
        """Check if tile is already uncovered."""
        subChunkLoc = (x%16, y%16)
        return self.tiles[subChunkLoc].uncovered
    
    def flagged(self, x:int, y:int) -> bool:
        """Check if tile is flagged."""
        subChunkLoc = (x%16, y%16)
        return self.tiles[subChunkLoc].flags > 0


def getbiomedata(biome:str,key:str):
    if biome in World.BIOMEDATA:
        if key in World.BIOMEDATA[biome]:
            return World.BIOMEDATA[biome][key]
    return World.BIOMEDEFAULT[key]

class World:
    # Available biomes with mine density and background color
    BIOMELIST = ["vert", "cyan","orange", "rouge", "violet"]
    BIOMEDATA = {
        "vert": {"bg":(34, 139, 34)},
        "cyan": {"bg":(70, 130, 180),"maxmines": 3},
        "orange": {"mineDensity": 0.2,"bg":(255, 140, 0)},
        "rouge": {"mineDensity": 0.3,"bg":(220, 20, 60)},
        "violet": {"mineDensity": 0.2,"bg":(75, 0, 130),"maxmines": 2},
    }
    EMPTYTILE = pygame.image.load(f"assets/tiles/empty.png")
    FULLBG = pygame.image.load(f"assets/tiles/fullBG.png")

    BIOMEDEFAULT = {"mineDensity": 0.1,"bg":(200, 200, 200),"maxmines": 1}

    def __init__(self, gameseed:int, score:int = 0):
        self.gameseed = gameseed
        self.score = score
        self.biomeGen = randomUtil.VoronoiGen(self.gameseed, 16)
        self.chunks = {}
        self.pendingUncover = []  # Queue for tiles to uncover next tick

    def tickPending(self):
        """Process up to 10 pending uncovered tiles per tick."""
        for pos in self.pendingUncover[0:min(10, len(self.pendingUncover))]:
            self.uncoverAt(pos[0], pos[1], True, 0)
        for i in range(min(10, len(self.pendingUncover))):
            self.pendingUncover.pop(0)


    def uncoverAt(self, x:int, y:int, spread:bool=True, depth:int=0,chord=False):
        """Uncover tile; spread to adjacent if value is 0. Prevent deep recursion by queuing."""
        if depth > 10:
            self.pendingUncover.append((x,y))
            return
        chunkLoc = (x//16, y//16)
        if chunkLoc not in self.chunks:
            self.chunks[chunkLoc] = Chunk(chunkLoc[0], chunkLoc[1], self)
        chunk = self.chunks[chunkLoc]
        if not ((chunk.uncovered(x,y) and not chord) or chunk.flagged(x,y)):
            if not chunk.uncovered(x,y):
                if self.getMineValue(x,y)>0:
                    self.score-= self.getMineValue(x,y)*100
                else:
                    self.score+=1
            val = chunk.uncover(x, y)
            # If empty with 0 mines nearby, uncover adjacent tiles
            if (val == 0 and spread) or chord:
                if chord:
                    m = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx = x + dx
                            ny = y + dy
                            m += self.getFlagValue(nx,ny)
                    if val!= m:
                        return
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx = x + dx
                        ny = y + dy
                        if (self.getFlagValue(nx,ny)==0) or val==0:
                            self.uncoverAt(nx, ny,True, depth+1)

    def flagAt(self, x:int, y:int):
        """Toggle flag on tile."""
        chunkLoc = (x//16, y//16)
        if chunkLoc not in self.chunks:
            self.chunks[chunkLoc] = Chunk(chunkLoc[0], chunkLoc[1], self)
        chunk = self.chunks[chunkLoc]
        subChunkLoc = (x%16, y%16)
        tile = chunk.tiles[subChunkLoc]
        if not tile.uncovered:
            tile.flags +=1
            tile.flags %= getbiomedata(self.getBiomeAt(x,y),"maxmines") + 1 
            
        

    def getBiomeAt(self, x:int, y:int) -> str:
        """Get biome type at world coordinates using Voronoi generation."""
        return self.biomeGen.get_value(x, y,World.BIOMELIST)
    
    def getMineValue(self, x:int, y:int) -> int:
        """Return the tiles mine value, 0 otherwise. Generate if chunk not loaded."""
        if (x//16, y//16) in self.chunks.keys():
            return self.chunks[(x//16, y//16)].tiles[(x%16, y%16)].value if self.chunks[(x//16, y//16)].tiles[(x%16, y%16)].type == "mine" else 0
        else:
            # Generate tile on-demand using seeded RNG
            rng = randomUtil.random.Random(randomUtil.coordinateRng(x//16, y//16, self.gameseed))
            tileIndex = (x % 16) * 16 + (y % 16)
            for _ in range(tileIndex):
                rng.random()
            val = rng.random()
            if val < getbiomedata(self.getBiomeAt(x, y),"mineDensity"):
                v = 1
                biome = self.getBiomeAt(x,y)
                if getbiomedata(biome,"maxmines")>1:
                    v += int(val*14558453)%getbiomedata(biome,"maxmines")
                
                return v
            return 0
        
    def getFlagValue(self, x:int, y:int) -> int:
        """Return the tile s flag value, 0 otherwise."""
        if (x//16, y//16) in self.chunks.keys():
            return self.chunks[(x//16, y//16)].tiles[(x%16, y%16)].flags
        else:
            return 0
        
    
    def handle_click_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse click event. Returns button number if clicked, False otherwise."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            return event.button
        return False
    

    def render(self, screen, camera):
        """Render background biomes and uncovered tiles."""
        camPos = -camera.vector(0,0)
        renderCorner = (camPos // 32)*32
        
        # Draw biome background tiles (32x32 pixels each)
        for x in range(-32, screen.get_width()+32, 32):
           for y in range(-32, screen.get_height()+32, 32):
                corner = camera.vector(renderCorner[0]+x, renderCorner[1]+y)
                col = getbiomedata(self.getBiomeAt((renderCorner[0]+x)//32, (renderCorner[1]+y)//32),"bg")
                pygame.draw.rect(screen, col, (corner[0], corner[1], 32, 32))

        # Draw tiles from loaded chunks
        for x in range(0, screen.get_width()+512, 512):
            for y in range(0, screen.get_height()+512, 512):
                chunkLoc = ((renderCorner[0]+x)//512, (renderCorner[1]+y)//512)
                if chunkLoc in self.chunks:
                    for tilePos, tile in self.chunks[chunkLoc].tiles.items():
                        # Skip if tile is outside screen bounds
                        if not (tilePos[0]*32+chunkLoc[0]*512-renderCorner[0] in range(-32, screen.get_width()+32, 32) and tilePos[1]*32+chunkLoc[1]*512-renderCorner[1] in range(-32, screen.get_height()+32, 32)):
                            continue
                        if not tile.uncovered:
                            # Draw covered tile
                            screen.blit(World.EMPTYTILE, camera.vector(tilePos[0]*32+chunkLoc[0]*512, tilePos[1]*32+chunkLoc[1]*512))
                            
                            if tile.flags > 0:
                                # Draw flag overlay
                                flagImage = pygame.image.load(f"assets/tiles/flag_{tile.flags}.png")
                                screen.blit(flagImage, camera.vector(tilePos[0]*32+chunkLoc[0]*512, tilePos[1]*32+chunkLoc[1]*512))
                
                            
                            continue
                        
                        # Draw uncovered tile
                        if tile.type == "empty":   
                            tileImage = pygame.image.load(f"assets/tiles/{tile.value}.png")
                        else:
                            tileImage = pygame.image.load(f"assets/tiles/mine_{tile.value}.png")
                        screen.blit(tileImage, camera.vector(tilePos[0]*32+chunkLoc[0]*512, tilePos[1]*32+chunkLoc[1]*512))
                        
                else:
                    # Draw empty tiles for unloaded chunks
                    for a in range(16):
                        for b in range(16):
                            screen.blit(World.EMPTYTILE, camera.vector(a*32+chunkLoc[0]*512, b*32+chunkLoc[1]*512))
