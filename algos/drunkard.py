import random
from algos.utils import find_random_tile_with_id, create_empty_map, fill_walls, is_valid_tile
from tile_data import T_WALL, T_GROUND
from main import MAP_X, MAP_Y, update_screen


DEFAULT_NUM_WALKS = 50
DEFAULT_MIN_STEPS_PER_WALK = 100
DEFAULT_MAX_STEPS_PER_WALK = 300

def create_drunkard_map(
        num_walks=DEFAULT_NUM_WALKS,
        min_steps=DEFAULT_MIN_STEPS_PER_WALK,
        max_steps=DEFAULT_MAX_STEPS_PER_WALK,
        diagonal_steps=False,
    ):
    new_map = create_empty_map()

    # set center space as walkable
    center_x = int(MAP_X//2)
    center_y = int(MAP_Y//2)    
    new_map[center_x][center_y] = T_GROUND

    for _ in range(num_walks):
        _gen_walk(
            new_map,
            random.randint(min_steps, max_steps),
        )        

    return new_map

def _gen_walk(gen_map, num_steps):
    walk_tiles = []
    count = 0

    cur_pos_xy = find_random_tile_with_id(
        gen_map,
        T_GROUND,
        )
    
    if cur_pos_xy is not None:
        cur_x, cur_y = cur_pos_xy        

        for i in range(num_steps):
            dir = random.choice(
                [
                    (0, -1),
                    (1, 0),
                    (0, 1),
                    (-1, 0),
                ]
            )

            if is_valid_tile(cur_x + dir[0], cur_y + dir[1]):
                cur_x = cur_x + dir[0]
                cur_y = cur_y + dir[1]
                gen_map[cur_x][cur_y] = T_GROUND
                walk_tiles.append((cur_x, cur_y))

                count += 1
                if count % 16 == 0:                    
                    update_screen(gen_map, highlight_tiles=walk_tiles)        

        update_screen(gen_map, highlight_tiles=walk_tiles)        
