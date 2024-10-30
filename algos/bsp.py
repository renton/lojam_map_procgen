import random, time
from algos.utils import create_empty_map, gen_random_colour
from main import MAP_X, MAP_Y, update_screen, T_WALL, T_GROUND

MAX_DEPTH = 4
MAX_SPLIT_PERC = 75
MIN_ROOM_SIZE = 20

# class to handle binary tree nodes
class BSPNode:
    def __init__(self, x, y, w, h, parent=None, depth=0, vertical_split=True):
        self.x = x  
        self.y = y
        self.w = w
        self.h = h
        self.left = None
        self.right = None
        self.parent = parent
        self.depth = depth
        self.colour = gen_random_colour()

        if self.depth < MAX_DEPTH:
            self.split(vertical_split)

    def insert_left(self, x, y, w, h, is_vertical_split):
        self.left = BSPNode(x, y, w, h, parent=self, depth=self.depth+1, vertical_split=is_vertical_split)

    def insert_right(self, x, y, w, h, is_vertical_split):
        self.right = BSPNode(x, y, w, h, parent=self, depth=self.depth+1, vertical_split=is_vertical_split)
    
    def get_sibling(self):
        pass

    def split(self, is_vertical_split):      
        ratio = random.randint(100-MAX_SPLIT_PERC, MAX_SPLIT_PERC) * 0.01
        
        if is_vertical_split:

            l_w = int(self.w * ratio)
            r_w = self.w - l_w
            l_x = self.x
            r_x = self.x + l_w

            self.insert_left(l_x, self.y, l_w, self.h, not is_vertical_split)
            self.insert_right(r_x, self.y, r_w, self.h, not is_vertical_split)
        else:

            t_h = int(self.h * ratio)
            b_h = self.h - t_h
            t_y = self.y
            b_y = self.y + t_h

            self.insert_left(self.x, t_y, self.w, t_h, not is_vertical_split)
            self.insert_right(self.x, b_y, self.w, b_h, not is_vertical_split)

    def fill_map(self, fill_map):
        for i in range(self.w):
            for j in range(self.h):
                fill_map[self.x + i][self.y + j] = self.colour

        update_screen(fill_map)
        time.sleep(0.2)

        if self.left:
            self.left.fill_map(fill_map)
        if self.right:
            self.right.fill_map(fill_map)

        update_screen(fill_map)
        time.sleep(0.2)


    def create_room(self, edit_map):
        if self.left:
            self.left.create_room(edit_map)
        if self.right:
            self.right.create_room(edit_map)

        if self.left is None and self.right is None:
            for i in range(self.w):
                for j in range(self.h):
                    edit_map[self.x + i][self.y + j] = None

            update_screen(edit_map)
            time.sleep(0.2)

            room_w = random.randint(
                min(MIN_ROOM_SIZE, (self.w - 2)),
                self.w - 2
            )

            room_h = random.randint(
                min(MIN_ROOM_SIZE, (self.h - 2)),
                self.h - 2
            )

            offset_x = random.randint(1, self.w - room_w - 1)
            offset_y = random.randint(1, self.h - room_h - 1)

            for i in range(room_w):
                for j in range(room_h):
                    edit_map[self.x + i + offset_x][self.y + j + offset_y] = T_GROUND


def create_bsp_map():
    new_map = create_empty_map(None)

    bsp_root = BSPNode(0, 0, MAP_X, MAP_Y, new_map)
    bsp_root.fill_map(new_map)

    time.sleep(1)

    bsp_root.create_room(new_map)

    return new_map
