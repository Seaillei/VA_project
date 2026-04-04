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
blue = (0, 0, 255)
black = (25, 25, 25)
brown = (139, 69, 19)
gray = (120, 120, 120)
purple = (128, 0, 128)
yellow = (255, 215, 0)
orange = (255, 165, 0)

#tiles
tile_size = full_height // rows
tile_types = 4
current_tile = 0

tile_colors = {
    -1: None,
    0: white, 
    1: red,
    2: green,
    3: black,
    4: blue,      # walker start
    5: orange,    # jumper
    6: purple 
}

map_data = []
enemy_data = []
platform_data = []

def load_level(level):
    global map_data, enemy_data, platform_data

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    filename = os.path.join(folder, f"{level}")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            level_data =  json.load(f)

        map_data.clear()
        map_data.extend(level_data.get("tiles", []))

        enemy_data.clear()
        enemy_data.extend(level_data.get("enemies", []))

        platform_data.clear()
        platform_data.extend(level_data.get("platforms", []))
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

def update_entities():
    #WALKERS
    for enemy in enemy_data:
        if enemy["type"] == "walker":
            if "dir" not in enemy:
                enemy["dir"] = 1  #end first
                enemy["_start_x"] = enemy["x"]  #runtime start x
                enemy["_start_y"] = enemy["y"]  #runtime start y

            target_x = enemy["end_x"] if enemy["dir"] == 1 else enemy["_start_x"]
            target_y = enemy["end_y"] if enemy["dir"] == 1 else enemy["_start_y"]

            #horizontal first
            if enemy["x"] != target_x:
                step = enemy.get("speed") * enemy["dir"]
                enemy["x"] += step
                if (enemy["dir"] == 1 and enemy["x"] >= target_x) or (enemy["dir"] == -1 and enemy["x"] <= target_x):
                    enemy["x"] = target_x

            #vertical
            elif enemy["y"] != target_y:
                step = enemy.get("speed") * enemy["dir"]
                enemy["y"] += step
                if (enemy["dir"] == 1 and enemy["y"] >= target_y) or (enemy["dir"] == -1 and enemy["y"] <= target_y):
                    enemy["y"] = target_y

            #switch
            if enemy["x"] == target_x and enemy["y"] == target_y:
                enemy["dir"] *= -1

        if enemy["type"] == "jumper":
            if "jump_timer" not in enemy:
                enemy["jump_timer"] = 0
                enemy["vel_y"] = 0
                enemy["_ground_y"] = enemy["y"]

            #timer
            enemy["jump_timer"] += 1
            if enemy["jump_timer"] >= enemy.get("jump_delay"):
                enemy["jump_timer"] = 0
                enemy["vel_y"] = - 0.27 * enemy.get("jump_height")

            #gravity
            enemy["vel_y"] += 0.1
            enemy["y"] += enemy["vel_y"]

            #land
            if enemy["y"] > enemy["_ground_y"]:
                enemy["y"] = enemy["_ground_y"]
                enemy["vel_y"] = 0

    #PLATFORMS
    for platform in platform_data:
        if "dir" not in platform:
            platform["dir"] = 1 #end first
            platform["_start_x"] = platform["x"]  #runtime start x
            platform["_start_y"] = platform["y"]  #runtime start y

        target_x = platform["end_x"] if platform["dir"] == 1 else platform["_start_x"]
        target_y = platform["end_y"] if platform["dir"] == 1 else platform["_start_y"]

        #horizontal first
        if platform["x"] != target_x:
            step = platform.get("speed") * platform["dir"]
            platform["x"] += step
            if (platform["dir"] == 1 and platform["x"] >= target_x) or (platform["dir"] == -1 and platform["x"] <= target_x):
                platform["x"] = target_x

        #vertical
        elif platform["y"] != target_y:
            step = platform.get("speed") * platform["dir"]
            platform["y"] += step
            if (platform["dir"] == 1 and platform["y"] >= target_y) or (platform["dir"] == -1 and platform["y"] <= target_y):
                platform["y"] = target_y

        #switch
        if platform["x"] == target_x and platform["y"] == target_y:
            platform["dir"] *= -1

def run_custom_level(screen, clock, level):

    load_level(level)

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
            
        # for platform in platform_data:
        #     platform_rect = pygame.Rect(platform["x"] * tile_size, platform["y"] * tile_size, tile_size, tile_size)
        
        # world shall obey me
        camera_x = player.centerx - full_width // 2

        if camera_x < 0:
            camera_x = 0
        if camera_x > world_width - full_width:
            camera_x = world_width - full_width


        draw_background(screen)
        update_entities()

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
        
        for enemy in enemy_data:
            if enemy["type"] == "walker":
                color = blue 
            elif enemy["type"] == "jumper":
                color = orange 

            enemy_rect = pygame.Rect(enemy["x"] * tile_size - camera_x, enemy["y"] * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, enemy_rect)
            
            if player.colliderect(enemy_rect):
                print("WHY ARE YOU DAD?")
                return "custom_levels"
            

        for platform in platform_data:
            platform_rect = pygame.Rect(platform["x"] * tile_size - camera_x, platform["y"] * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, purple, platform_rect)
            # colliders.append(platform_rect)

        # Weeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        pygame.draw.rect(screen,yellow,( player.x - camera_x, player.y, player.width, player.height))

        text = nadpisy.render(f"Custom level: {level}", True, white)
        screen.blit(text, (20, 20))

        pygame.display.update()
        clock.tick(FPS)
