import json
from world import World
from chunk import Chunk
from tile import Tile

class WorldSaver:
    def __init__(self, world):
        self.world = world

    def save(self, filepath):
        """Save world data to JSON file"""
        worldData = self.saveWorld()
        
        with open(filepath, 'w') as f:
            json.dump(worldData, f, indent=2)

    def saveWorld(self):
        """Convert world object to a dictionary"""
        return {
            "seed": self.world.seed,
            "chunks": self.saveChunks()
        }

    def saveChunks(self):
        """make a dict out of all chunks"""
        chunks = []
        for chunk in self.world.chunks:
            chunks.append({
                "x": chunk.x,
                "y": chunk.y,
                "tiles": saveTiles(chunk)
            })
        return chunks

    def saveTiles(self,chunk):
        """turn all tiles into a dict"""
        tiles = []
        for tile in chunk.tiles:
            tiles.append({
                "type": tile.type,
                "value": tile.value,
                "uncovered": tile.uncovered,
                "flags":tile.flags,
            })
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
            
            world = World(seed=worldData["seed"])
            world.chunks = self.loadChunks(worldData["chunks"], world)
            return world

        def loadChunks(self, chunksData, world):
            """Reconstruct chunks from data"""
            
            chunks = []
            for chunkData in chunksData:
                chunk = Chunk(chunkData["x"], chunkData["y"], world)
                chunk.tiles = self.loadTiles(chunkData["tiles"])
                chunks.append(chunk)
            return chunks

        def loadTiles(self, tilesData):
            """Reconstruct tiles from data"""
            
            tiles = []
            for tileData in tilesData:
                tile = Tile()
                tile.type = tileData["type"]
                tile.value = tileData["value"]
                tile.uncovered = tileData["uncovered"]
                tile.flags = tileData["flags"]
                tiles.append(tile)
            return tiles