import math
import random
def coordinateRng(x: int, y: int, seed: int) -> float:
    """Generate a random value based on coordinates and seed.
    """
    random.seed((seed*81734) ^ (x*127492) ^ (y*5830492)) #Joli ranndom tout beau tout propre :D
    return random.random()

def coordinateChoice(x: int, y: int, seed: int, choices: list) -> any:
    """Choose a random element from a list based on coordinates and seed.
    """
    random.seed(seed ^ x ^ y)
    return random.choice(choices)



class VoronoiGen:
    """Voronoi noise generator class. Used for biome generation."""

    def __init__(self, seed: int, scale: int) -> None:
        self.seed = seed
        self.scale = scale

    def get_value(self, x: int, y: int, biomes:list) -> float:
        """Get Voronoi noise value at given coordinates.

        Generate the point grid around the coordinates, find the closest
        point and return its distance to (x, y).
        """
        grid_origin_x = x // self.scale
        grid_origin_y = y // self.scale
        closest_dist = float('inf')
        closest_point = None

        for i in range(-1, 2):
            for j in range(-1, 2):
                grid_x = grid_origin_x + i
                grid_y = grid_origin_y + j
                grid_x_scaled = grid_x * self.scale
                grid_y_scaled = grid_y * self.scale
                
                offset_x = coordinateRng(grid_x_scaled, grid_y_scaled, self.seed)
                offset_y = coordinateRng(grid_x_scaled, grid_y_scaled, self.seed + 1)
                
                pt_x = (grid_x + offset_x) * self.scale
                pt_y = (grid_y + offset_y) * self.scale
                
                dist = math.hypot(pt_x - x, pt_y - y)
                
                if dist < closest_dist:
                    closest_dist = dist
                    closest_point = (pt_x, pt_y)

        return coordinateChoice(int(closest_point[0]), int(closest_point[1]), self.seed + 2,biomes)



if __name__ == "__main__":
    gen = VoronoiGen(42, 50)
    print(gen.get_value(1101, 200))