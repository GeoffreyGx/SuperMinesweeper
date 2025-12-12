import math
import random
def coordinateRng(x: float, y: float, seed: float) -> float:
    """Generate a random value based on coordinates and seed.
    """
    random.seed((seed*81734) ^ int(x*127492) ^ int(y*5830492)) #Joli ranndom tout beau tout propre :D
    return random.random()

def coordinateChoice(x: float, y: float, seed: float, choices: list) -> any:
    """Choose a random element from a list based on coordinates and seed.
    """
    random.seed((seed*730201) ^ int(x*82345) ^ int(y*777643))
    return random.choice(choices)



class VoronoiGen:
    """Voronoi noise generator class. Used for biome generation."""

    def __init__(self, seed: int, scale: int) -> None:
        self.seed = seed
        self.scale = scale
        self.pointMap = {}
        self.pointBiomeMap = {}

    def get_value(self, x: int, y: int, biomes: list) -> any:
        """Get Voronoi noise value at given coordinates.

        Generate the point grid around the coordinates, find the closest
        point and return its biome based on Voronoi cell pattern.
        """
        closestDist = float('inf')
        closestPoint = None

        # Check all surrounding grid cells
        for i in range(-1, 2):
            for j in range(-1, 2):
                gridX = (x // self.scale + i) * self.scale
                gridY = (y // self.scale + j) * self.scale

                # Generate or retrieve point for this grid cell
                if (gridX, gridY) not in self.pointMap:
                    ptX = gridX + coordinateRng(gridX, gridY, self.seed) * self.scale
                    ptY = gridY + coordinateRng(gridX, gridY, self.seed + 1) * self.scale
                    self.pointMap[(gridX, gridY)] = (ptX, ptY)
                    self.pointBiomeMap[(gridX, gridY)] = coordinateChoice(gridX, gridY, self.seed + 2, biomes)
                
                ptX, ptY = self.pointMap[(gridX, gridY)]
                dist = math.hypot(ptX - x, ptY - y)
                
                if dist < closestDist:
                    closestDist = dist
                    closestPoint = (gridX, gridY)

        return self.pointBiomeMap[closestPoint]


