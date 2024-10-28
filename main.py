import algos.utils
import pygame, sys

from tile_data import TILE_DATA

SCREEN_X = 1280
SCREEN_Y = 1024

DEFAULT_FPS = 60

BACKGROUND_COLOUR = (10, 10, 10)
HIGHLIGHT_COLOUR = (200,200,0)
PLAYER_COLOUR = (220, 10, 10)

TILE_SIZE = 8

CAMERA_DEFAULT_ZOOM = 1
CAMERA_MOVE_SPEED = 0.8
CAMERA_ZOOM_AMOUNT = 0.05

MAP_X = SCREEN_X // TILE_SIZE
MAP_Y = SCREEN_Y // TILE_SIZE

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.SCALED | pygame.NOFRAME | pygame.HWACCEL, vsync=1)
map_surface = pygame.Surface((MAP_X*TILE_SIZE, MAP_Y*TILE_SIZE))

pygame.display.set_caption("LoJam2024 ProcGen")


# ===== MAIN LOOP =====

def update_screen(
    proc_gen_map,
    camera_x=0,
    camera_y=0,
    camera_zoom=CAMERA_DEFAULT_ZOOM,
    camera_follow=False,
    tick=DEFAULT_FPS,
    highlight_tiles=None
    ):

        if highlight_tiles is None:
            highlight_tiles = []

        screen.fill(BACKGROUND_COLOUR)
        map_surface.fill(BACKGROUND_COLOUR)

        draw_map(map_surface, proc_gen_map, highlight_tiles)

        # Calculate the new scaled surface
        scaled_surface = pygame.transform.scale(
            map_surface,
            (int(map_surface.get_width() * camera_zoom), int(map_surface.get_height() * camera_zoom))
        )
        
        # Calculate camera offset for blitting
        blit_x = int(camera_x * camera_zoom)
        blit_y = int(camera_y * camera_zoom)

        # Blit the map surface to the main screen at the camera position
        screen.blit(scaled_surface, (-blit_x, -blit_y))

        if camera_follow:
            pygame.draw.rect(
                screen,
                PLAYER_COLOUR,
                pygame.Rect(SCREEN_X/2, SCREEN_Y/2, 12, 12)
            )

        pygame.display.flip()
        clock.tick(tick)

def mainloop():
    import algos.utils
    import algos.lazy_map
    import algos.drunkard
    import algos.cellular_automata

    proc_gen_map = algos.utils.create_empty_map()

    camera_x = 0
    camera_y = 0
    camera_zoom = CAMERA_DEFAULT_ZOOM
    camera_follow = False

    while True:
        
        # === HANDLE INPUT ===
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                # q to exit
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_f:
                    camera_follow = not camera_follow
                if event.key == pygame.K_1:
                    algos.utils.fill_walls(proc_gen_map)
                if event.key == pygame.K_2:
                    algos.utils.fix_connectivitiy(proc_gen_map)
                if event.key == pygame.K_3:
                    algos.utils.fix_connectivitiy(proc_gen_map, tunnel_variablity=40)
                if event.key == pygame.K_4:
                    algos.utils.fix_connectivitiy(proc_gen_map, tunnel_variablity=90)

                if event.key == pygame.K_F1:
                    proc_gen_map = algos.lazy_map.create_lazy_map()
                if event.key == pygame.K_F2:
                    proc_gen_map = algos.lazy_map.create_lazy_map(bsp=True)
                if event.key == pygame.K_F3:
                    proc_gen_map = algos.lazy_map.create_lazy_map(allow_overlap=True)
                if event.key == pygame.K_F4:
                    proc_gen_map = algos.drunkard.create_drunkard_map()
                if event.key == pygame.K_F5:
                    proc_gen_map = algos.cellular_automata.create_cellular_automata_map()                    


        keys = pygame.key.get_pressed()

        # move camera
        if keys[pygame.K_LEFT]:
            camera_x -= CAMERA_MOVE_SPEED * camera_zoom
        if keys[pygame.K_RIGHT]:
            camera_x += CAMERA_MOVE_SPEED * camera_zoom
        if keys[pygame.K_DOWN]:
            camera_y += CAMERA_MOVE_SPEED * camera_zoom
        if keys[pygame.K_UP]:
            camera_y -= CAMERA_MOVE_SPEED * camera_zoom
        if keys[pygame.K_z]:
            camera_zoom += CAMERA_ZOOM_AMOUNT
        if keys[pygame.K_x]:
            camera_zoom = max(1, camera_zoom - CAMERA_ZOOM_AMOUNT)
       
        # === DRAW SCREEN === 
        update_screen(proc_gen_map, camera_x, camera_y, camera_zoom, camera_follow)


def draw_map(surface, proc_gen_map, highlight_tiles):
    for row_index, row in enumerate(proc_gen_map):
        for col_index, tile_id in enumerate(row):

            if tile_id is not None:
                if (row_index, col_index) in highlight_tiles:
                    colour = HIGHLIGHT_COLOUR
                elif isinstance(tile_id, tuple):
                    colour = tile_id
                else:
                    colour = TILE_DATA[tile_id]['colour']

                rect_x = row_index * TILE_SIZE
                rect_y = col_index * TILE_SIZE

                # Draw the rectangle
                pygame.draw.rect(
                    surface,
                    colour,
                    pygame.Rect(rect_x, rect_y, TILE_SIZE, TILE_SIZE)
                )


if __name__ == "__main__":
    mainloop()