import random
from algos.utils import find_random_tile_with_id, create_empty_map
from main import update_screen, T_GROUND

DEFAULT_NUM_ROOMS = 20
DEFAULT_ROOM_MAX_SIZE = 32
DEFAULT_ROOM_MIN_SIZE = 8

def create_lazy_map(
        num_rooms=DEFAULT_NUM_ROOMS,
        room_min_size=DEFAULT_ROOM_MIN_SIZE,
        room_max_size=DEFAULT_ROOM_MAX_SIZE,
        allow_overlap=False,
    ):
    new_map = create_empty_map()

    for _ in range(num_rooms):
        room_tiles = gen_room(
            new_map,
            random.randint(room_min_size, room_max_size),
            random.randint(room_min_size, room_max_size),
            allow_overlap=allow_overlap
        )

        update_screen(new_map,tick=10,highlight_tiles=room_tiles)

    return new_map

def gen_room(gen_map, w, h, allow_overlap=False):
    room_tiles = []

    # find a place the room will fit
    room_xy = find_random_tile_with_id(
        gen_map,
        None,
        require_w=w,
        require_h=h,
        allow_overlap=allow_overlap
        )
 
    if room_xy is not None:
        room_x, room_y = room_xy
        for i in range(w):
            for j in range(h):
                gen_map[i+room_x][j+room_y] = T_GROUND
                room_tiles.append((i+room_x, j+room_y))

    return room_tiles
