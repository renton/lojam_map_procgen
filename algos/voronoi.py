import time
from algos.utils import find_random_tile_with_id, create_empty_map, fill_walls, is_valid_tile, gen_random_colour, bfs
from main import MAP_X, MAP_Y, update_screen, T_GROUND


DEFAULT_POINTS = 18

def create_voronoi_map(
        num_points=DEFAULT_POINTS,
    ):

    new_map = create_empty_map()

    group_points = {}

    # draw random group points to map
    for _ in range(num_points):
        pos = find_random_tile_with_id(new_map, None)
        group_id = gen_random_colour()
        group_points[pos] = group_id
        new_map[pos[0]][pos[1]] = group_id

    update_screen(new_map)
    count = 0

    # for each tile in grid, find which group point is closest
    for i in range(MAP_X):
        for j in range(MAP_Y):

            if new_map[i][j] is None:

                closest_group_path = bfs(new_map, (i, j), list(group_points.keys()), to_draw=False, walls=[])

                if closest_group_path is not None:
                    new_map[i][j] = group_points[closest_group_path[-1]]
                    for path_step in closest_group_path:
                        new_map[path_step[0]][path_step[1]] = group_points[closest_group_path[-1]]

                count += 1

                if count % 30 == 0:
                    update_screen(new_map)

    update_screen(new_map)
    time.sleep(2)

    # convert edges to walkable tile type for visualization
    for i in range(MAP_X):
        for j in range(MAP_Y):
            if new_map[i][j] is not T_GROUND:
                if is_valid_tile(i+1, j) and new_map[i][j] != new_map[i+1][j]:
                    new_map[i][j] = T_GROUND

                if is_valid_tile(i+1, j+1) and new_map[i][j] != new_map[i+1][j+1]:
                    new_map[i][j] = T_GROUND

                if is_valid_tile(i, j+1) and new_map[i][j] != new_map[i][j+1]:
                    new_map[i][j] = T_GROUND                

    update_screen(new_map)
    time.sleep(2)

    # convert walled tiles to emplty tiles for visualization
    for i in range(MAP_X):
        for j in range(MAP_Y):
            if new_map[i][j] != T_GROUND:
                new_map[i][j] = None

    return new_map