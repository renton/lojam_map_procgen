import random, time
import itertools
from collections import deque
from main import MAP_X, MAP_Y, update_screen, T_WALL, T_GROUND

def create_empty_map(tile_id=None):
    empty_map = []

    for x in range(MAP_X):
        empty_map.append([])
        for y in range(MAP_Y):
            empty_map[x].append(tile_id)

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
            if (((search_map[i][j] is not None) and search_map[i][j] == tile_id) or \
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

        # explore the map from every point to classify the unconnected groups
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

        #  while there is more than one group, create a tunnel from group to another different group at random
        if len(group_tiles.keys()) > 1:

            group_a, group_b = random.sample(list(group_tiles.keys()), 2)
            group_a_tile = random.choice(group_tiles[group_a])
            group_b_tile = random.choice(group_tiles[group_b])

            make_tunnel(fix_map, group_a_tile, group_b_tile, group_a, rand_step_chance=tunnel_variablity)
            
            update_screen(fix_map)
            time.sleep(0.5)

        # convert back to T_GROUND for visualization
        for x in range(len(fix_map)):
            for y in range(len(fix_map[x])):
                if isinstance(fix_map[x][y], tuple) and fix_map[x][y] != T_WALL:
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

    # keep tunneling until target tile is reached
    while ((cur_x, cur_y) != to_tile):

        fix_map[cur_x][cur_y] = marker

        # random chance to step away from desired path
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

            # tunnel in x direction towards target
            if cur_x > to_tile[0]:
                cur_x -= 1
            elif cur_x < to_tile[0]:
                cur_x += 1

            # tunnel in y direction towards target
            elif cur_y > to_tile[1]:
                cur_y -= 1
            elif cur_y < to_tile[1]:
                cur_y += 1

        count += 1
        if count % 5 == 0:
            update_screen(fix_map, highlight_tiles=[to_tile, from_tile])

def shortest_path(apply_map):

    start_pos = find_random_tile_with_id(apply_map, T_GROUND)
    end_pos = find_random_tile_with_id(apply_map, T_GROUND)

    bfs(apply_map, start_pos, [end_pos])

    update_screen(apply_map, highlight_tiles=[start_pos, end_pos])

def explore(explore_map, cur_x, cur_y, marker):
    to_explore_stack = []
    explored_tiles = []

    if explore_map[cur_x][cur_y] != T_GROUND:
        return explored_tiles

    to_explore_stack.append((cur_x, cur_y))
    
    steps = 0

    # check to see if any tiles left in the explore stack
    while len(to_explore_stack):
        cur_x, cur_y = to_explore_stack.pop()

        if is_valid_tile(cur_x, cur_y):
            if explore_map[cur_x][cur_y] == T_GROUND:
                # mark explored tiles with the group id
                explore_map[cur_x][cur_y] = marker
                explored_tiles.append((cur_x, cur_y))
                for coords in get_neighbour_coords(cur_x, cur_y):
                    to_explore_stack.append(coords)

                steps += 1
                if steps % 70 == 0:
                    update_screen(explore_map)

    return explored_tiles


def get_neighbour_coords(x, y):
    return [
        (x+1, y),
        (x-1, y),
        (x, y-1),
        (x, y+1),
    ]

def bfs(floor, start_xy, goals_xys, to_draw=True, walls=[None, T_WALL]):
    queue = deque([[start_xy]])
    seen = set([start_xy])
    num_loops = 0

    while queue:
        path = queue.popleft()
        x, y = path[-1]

        if (x, y) in goals_xys:
            path.pop(0) # remove first entry which is current pos
            if to_draw:
                update_screen(floor, highlight_tiles=[start_xy] + goals_xys + path)
                time.sleep(2)
            return path

        # only check cardinal dirs
        for x2, y2 in (
            (x+1,y),
            (x-1,y),
            (x,y+1),
            (x,y-1),
        ):            

            if  0 <= x2 < (len(floor)) and \
                0 <= y2 < (len(floor[0])) and \
                floor[x2][y2] not in walls and \
                (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

        num_loops += 1
        if to_draw and num_loops % 100 == 0:
            update_screen(floor, highlight_tiles=[start_xy] + goals_xys + path, secondary_highlight_tiles=list(seen))
