import pygame, sys

# CONSTANTS

DEFAULT_FPS = 60

SCREEN_X = 1280
SCREEN_Y = 1024

TILE_SIZE = 8

MAP_X = SCREEN_X // TILE_SIZE
MAP_Y = SCREEN_Y // TILE_SIZE

T_GROUND = (240, 250, 240)
T_WALL = (110, 110, 110)
BACKGROUND_COLOUR = (10, 10, 10)
HIGHLIGHT_COLOUR = (255,0,0)
HIGHLIGHT2_COLOUR = (244, 199, 0)
PLAYER_COLOUR = (220, 10, 10)

CAMERA_DEFAULT_ZOOM = 1
CAMERA_MOVE_SPEED = 0.8
CAMERA_ZOOM_AMOUNT = 0.05


# PYGAME INIT
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.SCALED | pygame.NOFRAME | pygame.HWACCEL, vsync=1)
map_surface = pygame.Surface((MAP_X*TILE_SIZE, MAP_Y*TILE_SIZE))

pygame.display.set_caption("LoJam2024 ProcGen")

# ===== DRAW SCREEN =====

def update_screen(
    proc_gen_map,
    camera_x=0,
    camera_y=0,
    camera_zoom=CAMERA_DEFAULT_ZOOM,
    camera_follow=False,
    tick=DEFAULT_FPS,
    highlight_tiles=None,
    secondary_highlight_tiles=None,
    ):
        if highlight_tiles is None:
            highlight_tiles = []

        if secondary_highlight_tiles is None:
            secondary_highlight_tiles = []

        screen.fill(BACKGROUND_COLOUR)
        map_surface.fill(BACKGROUND_COLOUR)

        draw_map(map_surface, proc_gen_map, highlight_tiles, secondary_highlight_tiles)

        # calculate the new scaled map surface
        scaled_surface = pygame.transform.scale(
            map_surface,
            (int(map_surface.get_width() * camera_zoom), int(map_surface.get_height() * camera_zoom))
        )
        
        # calculate camera offset for blitting
        blit_x = int(camera_x * camera_zoom)
        blit_y = int(camera_y * camera_zoom)

        # blit the map surface to the main screen at the camera position
        screen.blit(scaled_surface, (-blit_x, -blit_y))

        # draw player if camera follow mode
        if camera_follow:
            pygame.draw.rect(
                screen,
                PLAYER_COLOUR,
                pygame.Rect(SCREEN_X/2, SCREEN_Y/2, 12, 12)
            )

        pygame.display.flip()
        clock.tick(tick)

# draw the map onto the map surface
def draw_map(surface, proc_gen_map, highlight_tiles, secondary_highlight_tiles):
    for row_index, row in enumerate(proc_gen_map):
        for col_index, tile_id in enumerate(row):

            # show highlight colours for visualizations
            if (row_index, col_index) in highlight_tiles:
                colour = HIGHLIGHT_COLOUR
            elif (row_index, col_index) in secondary_highlight_tiles:
                colour = HIGHLIGHT2_COLOUR
            elif isinstance(tile_id, tuple):
                colour = tile_id
            elif tile_id is None:
                continue

            rect_x = row_index * TILE_SIZE
            rect_y = col_index * TILE_SIZE

            # draw the rectangle for the tile
            pygame.draw.rect(
                surface,
                colour,
                pygame.Rect(rect_x, rect_y, TILE_SIZE, TILE_SIZE)
            )


# ===== MAIN LOOP =====

def mainloop():
    import algos.utils
    import algos.bsp
    import algos.lazy_map
    import algos.drunkard
    import algos.diffusion_limited_aggregation    
    import algos.cellular_automata
    import algos.voronoi
    import algos.perlin

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
                    # reset camera zoom
                    if camera_follow:
                        camera_x = 0
                        camera_y = 0
                        camera_zoom = CAMERA_DEFAULT_ZOOM
                    camera_follow = not camera_follow
                if event.key == pygame.K_1:
                    algos.utils.fill_walls(proc_gen_map)
                if event.key == pygame.K_2:
                    algos.utils.fix_connectivitiy(proc_gen_map)
                if event.key == pygame.K_3:
                    algos.utils.fix_connectivitiy(proc_gen_map, tunnel_variablity=85)
                if event.key == pygame.K_4:
                    algos.utils.shortest_path(proc_gen_map)

                if event.key == pygame.K_F1:
                    proc_gen_map = algos.lazy_map.create_lazy_map()
                if event.key == pygame.K_F2:
                    proc_gen_map = algos.bsp.create_bsp_map()
                if event.key == pygame.K_F3:
                    proc_gen_map = algos.lazy_map.create_lazy_map(allow_overlap=True)
                if event.key == pygame.K_F4:
                    proc_gen_map = algos.drunkard.create_drunkard_map()
                if event.key == pygame.K_F5:
                    proc_gen_map = algos.diffusion_limited_aggregation.create_diffusion_limited_aggregation_map()
                if event.key == pygame.K_F6:
                    proc_gen_map = algos.voronoi.create_voronoi_map()
                if event.key == pygame.K_F7:
                    proc_gen_map = algos.cellular_automata.create_cellular_automata_map()
                if event.key == pygame.K_F8:
                    proc_gen_map = algos.perlin.create_perlin_map(terrain_mode=False)
                if event.key == pygame.K_F9:
                    proc_gen_map = algos.perlin.create_perlin_map()
                if event.key == pygame.K_F10:
                    proc_gen_map = algos.perlin.create_perlin_map(two_layer=True)


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
       
        # draw the screen
        update_screen(proc_gen_map, camera_x, camera_y, camera_zoom, camera_follow)


if __name__ == "__main__":
    mainloop()