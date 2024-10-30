import random
from algos.utils import create_empty_map, is_valid_tile
from main import MAP_X, MAP_Y, update_screen, T_GROUND


DEFAULT_NUM_WALKS = 6000

def create_diffusion_limited_aggregation_map(
        num_walks=DEFAULT_NUM_WALKS,
    ):
    new_map = create_empty_map()

    # set center space as walkable
    center_x = int(MAP_X//2)
    center_y = int(MAP_Y//2)    
    new_map[center_x][center_y] = T_GROUND

    for _ in range(num_walks):
        gen_walk(
                new_map,
                (                    
                    random.randint(0, MAP_X-1),
                    random.randint(0, MAP_Y-1),
                ),
            )

    return new_map

def gen_walk(gen_map, cur_xy):
    cur_x, cur_y = cur_xy

    while(True):
        dir = random.choice(
            [
                (0, -1),
                (1, 0),
                (0, 1),
                (-1, 0),
            ]
        )


        # out of bounds - stop walk
        if not is_valid_tile(cur_x + dir[0], cur_y+ dir[1]):
            return
        else:
            # move randomly until you hit the map cluster
            if gen_map[cur_x+dir[0]][cur_y+dir[1]] == T_GROUND:
                gen_map[cur_x][cur_y] = T_GROUND
                update_screen(gen_map, highlight_tiles=[(cur_x, cur_y)]) 
                break 
            cur_x = cur_x + dir[0]
            cur_y = cur_y + dir[1]
