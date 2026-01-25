import json
from sweeper.world import *

class WorldSaver:
    def __init__(self, world, path):
        self.world = world
        self.save(path)

    def save(self, filepath):
        """Save world data to JSON file"""
        worldData = self.saveWorld()
        
        with open(filepath, 'w') as f:
            json.dump(worldData, f, indent=2)

    def saveWorld(self):
        """Convert world object to a dictionary"""
        return {
            "seed": self.world.gameseed,
            "score": self.world.score,
            "chunks": self.saveChunks()
        }

    def saveChunks(self):
        """make a dict out of all chunks"""
        chunks = []
        for chunk in self.world.chunks.values():
            chunks.append({
                "x": chunk.x,
                "y": chunk.y,
                "tiles": self.saveTiles(chunk)
            })
        return chunks

    def saveTiles(self,chunk):
        """turn all tiles into a dict"""
        tiles = {}
        for k in chunk.tiles:
            tile = chunk.tiles[k]
            t = "1" if tile.type == "mine" else "0"
            u = "1" if tile.uncovered else "0"
            tiles[str(k[0])+";"+str(k[1])]=t+u+str(tile.flags)+str(tile.value)
        return tiles
    

class WorldLoader:
    def __init__(self):
        pass

    def load(self, filepath):
        """Load world data from JSON file"""
        with open(filepath, 'r') as f:
            worldData = json.load(f)
        
        return self.loadWorld(worldData)

    def loadWorld(self, worldData):
        """Convert dictionary back to world object"""
        self.world = World(worldData["seed"],worldData["score"])
        self.world.chunks = self.loadChunks(worldData["chunks"], self.world)
        return self.world

    def loadChunks(self, chunksData, world):
        """Reconstruct chunks from data"""
        
        chunks = {}
        for chunkData in chunksData:
            chunk = Chunk(chunkData["x"], chunkData["y"], world)
            chunk.tiles = self.loadTiles(chunkData["tiles"])
            chunks[chunkData["x"], chunkData["y"]]=chunk
        return chunks

    def loadTiles(self, tilesData):
        """Reconstruct tiles from data"""
        
        tiles = {}
        for k in tilesData:
            tileData = tilesData[k]
            ks = k.split(";")
            tile = Tile(int(ks[0]),int(ks[1]),self.world,0)
            tile.type = "mine" if tileData[0] == "1" else "empty"
            tile.uncovered = True if tileData[1] == "1" else False
            tile.flags = int(tileData[2])
            tile.value = int(tileData[2:])
            if tile.type == "mine":
                tile.mines = tile.value
            tiles[(int(ks[0]),int(ks[1]))] = tile
        return tiles