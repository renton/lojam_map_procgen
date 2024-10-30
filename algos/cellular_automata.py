import time
from algos.utils import get_adjacent_tiles, create_random_map, is_valid_tile
from main import update_screen, T_GROUND, T_WALL

# ALIVE = WALL
# DEAD = GROUND

DEFAULT_WALKABLE_DIST = 0.6
DEFAULT_GENERATIONS = 8

GENERATION_SLEEP_TIME = 0.5

BIRTH_LIMIT = 4
DEATH_LIMIT = 3

def create_cellular_automata_map(
        init_walkable_dist=DEFAULT_WALKABLE_DIST,
        num_generations=DEFAULT_GENERATIONS,
    ):

    new_map = create_random_map(init_walkable_dist)
    update_screen(new_map)
    time.sleep(GENERATION_SLEEP_TIME)

    for _ in range(num_generations):
        _step_generation(new_map)

    return new_map

def _step_generation(gen_map):
    changed_tiles = []

    orig_map = gen_map[:]

    for i in range(len(gen_map)):
        for j in range(len(gen_map[i])):
            neighbour_wall_count = 0

            for check_x, check_y in get_adjacent_tiles(i, j):
                if is_valid_tile(check_x, check_y):
                    if orig_map[check_x][check_y] == T_WALL:
                        neighbour_wall_count += 1

            # if ALIVE
            if orig_map[i][j] == T_WALL:
                if neighbour_wall_count < DEATH_LIMIT:
                    gen_map[i][j] = T_GROUND
                    changed_tiles.append((i,j))

            # if DEAD
            elif orig_map[i][j] == T_GROUND:
                if neighbour_wall_count > BIRTH_LIMIT:
                    gen_map[i][j] = T_WALL
                    changed_tiles.append((i,j))

    update_screen(gen_map)
    time.sleep(1)
