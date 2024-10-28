import random, time
import itertools
from tile_data import T_GROUND, T_WALL, TILE_DATA
from main import MAP_X, MAP_Y, update_screen

def create_empty_map():
    empty_map = []

    for x in range(MAP_X):
        empty_map.append([])
        for y in range(MAP_Y):
            empty_map[x].append(None)

    return empty_map

def create_random_map(walkable_dist=0.5):
    new_map = []
    for x in range(MAP_X):
        new_map.append([])
        for y in range(MAP_Y):
            if random.randint(0, 100) >= (walkable_dist*100):
                new_tile = T_WALL
            else:
                new_tile = T_GROUND

            new_map[x].append(new_tile)

    return new_map

def find_random_tile_with_id(
        search_map,
        tile_id,
        require_w=None,
        require_h=None,
        allow_overlap=False,
    ):
    valid_tiles = []

    for i in range(len(search_map)):
        for j in range(len(search_map[i])):
            if ((tile_id in TILE_DATA and (search_map[i][j] is not None) and search_map[i][j] == tile_id) or \
                (tile_id is None and search_map[i][j] is None)) and \
                (i != 0) and (j != 0) and (i != MAP_X-1) and (j != MAP_Y-1):


                valid_coords = True
                if (require_w is not None and require_h is not None):
                    if (require_w+i > MAP_X) or (require_h+j > MAP_Y):
                        valid_coords = False
                        break

                    if not allow_overlap:
                        for testx in range(require_w):
                            for testy in range(require_h):
                                if not is_valid_tile(i+testx, j+testy) or search_map[i+testx][j+testy] != None:
                                    valid_coords = False
                                    break
                            if valid_coords == False:
                                break
                    
                
                if valid_coords:                    
                    valid_tiles.append((i, j))

    if len(valid_tiles) == 0:
        return None

    return random.choice(valid_tiles)

def get_adjacent_tiles(x, y):
    offsets = itertools.product([-1, 0, 1], repeat=2)
    return [(x + dx, y + dy) for dx, dy in offsets if (dx, dy) != (0, 0)]

def is_valid_tile(x, y):    
    return x >= 0 and y >= 0 and x < MAP_X and y < MAP_Y

def fill_walls(fill_map):
    count = 0
    for i in range(len(fill_map)):
        for j in range(len(fill_map[i])):
            # replaces ground at edge of the screen boundary with walls
            if (i == 0 or j == 0 or i == MAP_X-1 or j == MAP_Y-1) and fill_map[i][j] == T_GROUND:
                fill_map[i][j] = T_WALL

            # replace edges of walkable map with walls
            if fill_map[i][j] is None:
                for check_x, check_y in get_adjacent_tiles(i, j):
                    if is_valid_tile(check_x, check_y) and fill_map[check_x][check_y] == T_GROUND:
                        fill_map[i][j] = T_WALL

                        count += 1
                        if count % 20 == 0:
                            update_screen(fill_map)
                        break

            # turn single wall tiles surrounded by ground to ground
            if fill_map[i][j] == T_WALL:
                ground_count = 0              
                for check_x, check_y in get_adjacent_tiles(i, j):
                    if is_valid_tile(check_x, check_y) and fill_map[check_x][check_y] == T_GROUND:
                        ground_count += 1

                if ground_count >= 8:
                    fill_map[i][j] = T_GROUND
                    update_screen(fill_map)

def gen_random_colour():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

def fix_connectivitiy(fix_map, tunnel_variablity=0):    
    first_run = True

    while first_run == True or len(group_tiles.keys()) > 1:

        first_run = False
        group_tiles = {}
        cur_group_id = gen_random_colour()

        for x in range(len(fix_map)):
            for y in range(len(fix_map[x])):
                explored_tiles = explore(
                    fix_map,
                    x,
                    y,
                    cur_group_id
                )
                if len(explored_tiles):
                    group_tiles[cur_group_id] = explored_tiles
                    cur_group_id = gen_random_colour()

        update_screen(fix_map)

        if len(group_tiles.keys()) > 1:

            group_a, group_b = random.sample(list(group_tiles.keys()), 2)
            group_a_tile = random.choice(group_tiles[group_a])
            group_b_tile = random.choice(group_tiles[group_b])

            make_tunnel(fix_map, group_a_tile, group_b_tile, group_a, rand_step_chance=tunnel_variablity)
            
            update_screen(fix_map)
            time.sleep(1)

        # convert back to T_GROUND
        for x in range(len(fix_map)):
            for y in range(len(fix_map[x])):
                if isinstance(fix_map[x][y], tuple):
                    fix_map[x][y] = T_GROUND

def make_tunnel(
        fix_map,
        from_tile,
        to_tile,
        marker,
        rand_step_chance=0
    ):
    
    cur_x, cur_y = from_tile

    count = 0

    while ((cur_x, cur_y) != to_tile):

        fix_map[cur_x][cur_y] = marker

        if rand_step_chance > random.randint(0, 100):
            if random.randint(0, 1) == 0:
                next_x = random.choice([cur_x+1, cur_x-1])
                if is_valid_tile(next_x, cur_y):
                    cur_x = next_x
            else:
                next_y = random.choice([cur_y+1, cur_y-1])            
                if is_valid_tile(cur_x, next_y):
                    cur_y = next_y
        else:

            # X tunnel
            if cur_x > to_tile[0]:
                cur_x -= 1
            elif cur_x < to_tile[0]:
                cur_x += 1

            # Y tunnel
            elif cur_y > to_tile[1]:
                cur_y -= 1
            elif cur_y < to_tile[1]:
                cur_y += 1

        count += 1
        if count % 4 == 0:
            update_screen(fix_map)

def explore(explore_map, cur_x, cur_y, marker):
    to_explore_stack = []
    explored_tiles = []

    if explore_map[cur_x][cur_y] != T_GROUND:
        return explored_tiles

    to_explore_stack.append((cur_x, cur_y))
    
    steps = 0

    while len(to_explore_stack):
        cur_x, cur_y = to_explore_stack.pop()

        if is_valid_tile(cur_x, cur_y):
            if explore_map[cur_x][cur_y] == T_GROUND:
                explore_map[cur_x][cur_y] = marker
                explored_tiles.append((cur_x, cur_y))
                for coords in get_neighbour_coords(cur_x, cur_y):
                    to_explore_stack.append(coords)

                steps += 1
                if steps % 50 == 0:
                    update_screen(explore_map)

    return explored_tiles


def get_neighbour_coords(x, y):
    return [
        (x+1, y),
        (x-1, y),
        (x, y-1),
        (x, y+1),
    ]