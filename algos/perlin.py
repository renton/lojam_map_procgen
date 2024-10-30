import random
import numpy as np
from noise import pnoise2

from algos.utils import create_empty_map
from main import MAP_X, MAP_Y

SCALE =  100.0
OCTAVES = 4
PERSISTENCE = 0.5
LACUNARITY = 2.0

SECOND_MAP_SCALE = 0.2
SECOND_MAP_OCTAVES = 16

def convert_to_255(value):
    # normalize -1 to 1 float to an integer between 0-255
    if -1 <= value <= 1:
        return int((value + 1) * 255 / 2)
    else:
        raise ValueError("input value must be between -1 and 1.")

def create_perlin_map(
        two_layer=False,
        terrain_mode=True,
    ):

    new_map = create_empty_map()
    world = np.zeros((MAP_X, MAP_Y))
    world2 = np.zeros((MAP_X, MAP_Y))
    base = random.randint(0, 255)
    base2 = random.randint(0, 255)

    for i in range(MAP_X):
        for j in range(MAP_Y):
            world[i][j] = pnoise2(
                i/SCALE,
                j/SCALE,
                octaves=OCTAVES,
                persistence=PERSISTENCE,
                lacunarity=LACUNARITY,
                repeatx=MAP_X,
                repeaty=MAP_Y,
                base=base
            )

            if two_layer:             
                world2[i][j] = pnoise2(
                    i/SCALE*(LACUNARITY**SECOND_MAP_SCALE),
                    j/SCALE*(LACUNARITY**SECOND_MAP_SCALE),
                    octaves=SECOND_MAP_OCTAVES,
                    persistence=PERSISTENCE,
                    lacunarity=LACUNARITY,
                    repeatx=MAP_X,
                    repeaty=MAP_Y,
                    base=base2
                )

                world[i][j] += world2[i][j]*(PERSISTENCE**SECOND_MAP_SCALE)

            if terrain_mode:
                if world[i][j] < -0.15:
                    # WATER
                    value = (47, 86, 233)
                elif world[i][j] < -0.05:
                    # SHALLOW
                    value = (67, 106, 253)
                elif world[i][j] < 0:
                    # SAND
                    value = (203, 189, 147)
                elif world[i][j] < 0.15:
                    # GRASS
                    value = (50, 150, 50)
                elif world[i][j] < 0.30:
                    # HILLS
                    value = (100, 100, 100)
                elif world[i][j] < 0.35:
                    # MOUNTAIN
                    value = (70, 70, 70)
                elif world[i][j] < 0.55:
                    # SNOW
                    value = (240, 240, 240)
            else:
                value=(
                    convert_to_255(world[i][j]),
                    convert_to_255(world[i][j]),
                    convert_to_255(world[i][j]),
                )

            new_map[i][j] = value

    return new_map