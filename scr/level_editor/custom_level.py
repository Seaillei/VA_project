import pygame
import os
import json

FPS = 60

full_width = 1100
full_height = 740

#sizes
rows = 16
max_collums = 150

#color
green = (144, 201, 120)
white = (255, 255, 255)
red = (200, 25, 25)
black = (25, 25, 25)
brown = (139, 69, 19)
gray = (120, 120, 120)
yellow = (255, 215, 0)

#tiles
tile_size = full_height // rows
tile_types = 4
current_tile = 0

tile_colors = {
    -1: None,
    0: white, 
    1: red,
    2: green,
    3: black
}

def load_level(level):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    filename = os.path.join(folder, f"{level}")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        print("Level file does not exist!")
        return []

#functions
def outputing_text(text, font, text_col, x, y, screen):
    write = font.render(text, True, text_col)
    screen.blit(write, (x, y))

def draw_background(screen):
    screen.fill(gray)

# def draw_grid(screen):
#     #verticaly
#     for c in range(max_collums + 1):
#         pygame.draw.line(screen, white, (c * tile_size - scroll, 0), (c * tile_size - scroll, full_height))

#     #horizontaly
#     for c in range(rows + 1):
#         pygame.draw.line(screen, white, (0, c * tile_size), (full_width, c * tile_size))

# def draw_world_tiles(screen):
#      for y, row in enumerate(load_level()):
#          for x, tile in enumerate(row):
#             if tile != -1:
#                 color = tile_colors[tile]

#                 pygame.draw.rect(screen, color, (x * tile_size - scroll,y * tile_size, tile_size, tile_size))

def run_custom_level(screen, clock, level):

    map_data = load_level(level)

    spawn_x = 100 
    spawn_y = 100
     
    vel_x = 0
    vel_y = 0

    gravity = 1
    jump_strength = -15
    movement_strength = 7
    on_ground = False

    player_size = int(tile_size / 1.5)

    world_width = len(map_data[0]) * tile_size

    #font
    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    #COLIDERS
    colliders = []
    danger = []
    end = []
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            world_x = x * tile_size
            world_y = y * tile_size

            if tile == 0:  # WHITE
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                colliders.append(rect)
            if tile == 1:  # RED
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                danger.append(rect)
            if tile == 2:  # GREEN
                spawn_x = world_x
                spawn_y = world_y
            if tile == 3:  # BLACK
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                end.append(rect)

    player = pygame.Rect(spawn_x + (tile_size - player_size) // 2 , spawn_y + (tile_size - player_size) // 2, player_size, player_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        # horizontal reset
        vel_x = 0

        if keys[pygame.K_d]:
            vel_x = movement_strength
        if keys[pygame.K_a]:
            vel_x = -movement_strength

        # uppies
        if keys[pygame.K_SPACE] and on_ground:
            vel_y = jump_strength
            on_ground = False

        # gravity
        vel_y += gravity

      # horizontal bs
        player.x += vel_x
        for tile in colliders:
            if player.colliderect(tile):
                if vel_x > 0:
                    player.right = tile.left
                elif vel_x < 0:
                    player.left = tile.right

        # vertical bs
        player.y += vel_y
        on_ground = False

        for tile in colliders:
            if player.colliderect(tile):
                if vel_y > 0:
                    player.bottom = tile.top
                    vel_y = 0
                    on_ground = True
                elif vel_y < 0:
                    player.top = tile.bottom
                    vel_y = 0

        if player.y > full_height:
            return "custom_levels"
        
        # hitting blockdanger
        for collider in danger:
            if player.colliderect(collider):
                print("WHY ARE YOU DAD?")
                return "custom_levels"
            
        # hitting end
        for collider in end:
            if player.colliderect(collider):
                print("YOU WON")
                return "custom_levels"
        
        # world shall obey me

        camera_x = player.centerx - full_width // 2

        if camera_x < 0:
            camera_x = 0
        if camera_x > world_width - full_width:
            camera_x = world_width - full_width


        draw_background(screen)

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile == 0:
                    pygame.draw.rect(screen, tile_colors[0],( x * tile_size - camera_x, y * tile_size, tile_size, tile_size))
                if tile == 1:
                    pygame.draw.rect(screen, tile_colors[1],( x * tile_size - camera_x, y * tile_size, tile_size, tile_size))
                if tile == 2:
                    pygame.draw.rect(screen, tile_colors[2],( x * tile_size - camera_x, y * tile_size, tile_size, tile_size))
                if tile == 3:
                    pygame.draw.rect(screen, tile_colors[3],( x * tile_size - camera_x, y * tile_size, tile_size, tile_size))

        # Weeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        pygame.draw.rect(screen,white,( player.x - camera_x, player.y, player.width, player.height))

        text = nadpisy.render(f"Custom level: {level}", True, white)
        screen.blit(text, (20, 20))

        pygame.display.update()
        clock.tick(FPS)