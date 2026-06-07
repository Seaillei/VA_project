import pygame
import os
import json

pygame.mixer.init()

FPS = 60

full_width = 1100
full_height = 740

# sizes
rows = 16
max_collums = 150

# color
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

# tiles
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

# sounds
script_dir = os.path.dirname(os.path.abspath(__file__))
death_sound_path = os.path.join(script_dir, "..", "sounds", "sad_hamster_violin.wav")

death_sound = pygame.mixer.Sound(death_sound_path)

def load_level(level: str, level_type: str = "standard") -> list | None:
    """Handles loading individual levels from either regular or custom folders."""
    global map_data, enemy_data, platform_data

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if level_type == "custom":
        folder = os.path.join(script_dir, "..", "level_editor", "custom_levels")
    else:
        folder = os.path.join(script_dir, "levels")
        
    filename = os.path.join(folder, f"{level}")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            level_data = json.load(f)

        map_data.clear()
        map_data.extend(level_data.get("tiles", []))

        enemy_data.clear()
        enemy_data.extend(level_data.get("enemies", []))

        platform_data.clear()
        platform_data.extend(level_data.get("platforms", []))
    else:
        print(f"Level file does not exist at: {filename}")
        return []
    
class Menu_Button():
    def __init__(self, x: float, y: float, width: int, height: int, color: tuple, action=None, text: str = "", font=None, text_color: tuple = (0, 0, 0)) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action
        self.text = text
        self.text_color = text_color
        self.font = font

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text != "":
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def handle_event(self, event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    return self.action()
        return None

def outputing_text(text: str, font, text_col: tuple, x: float, y: float, screen) -> None:
    write = font.render(text, True, text_col)
    screen.blit(write, (x, y))

def draw_background(screen) -> None:
    screen.fill(gray)

def update_entities() -> None:
    # WALKERS
    for enemy in enemy_data:
        if enemy["type"] == "walker":
            if "moving_to_end" not in enemy:
                enemy["moving_to_end"] = True
                enemy["_start_x"] = enemy["x"]
                enemy["_start_y"] = enemy["y"]

            target_x = enemy["end_x"] if enemy["moving_to_end"] else enemy["_start_x"]
            target_y = enemy["end_y"] if enemy["moving_to_end"] else enemy["_start_y"]
            speed = enemy.get("speed", 1)

            if enemy["x"] != target_x:
                if enemy["x"] < target_x:
                    enemy["x"] = min(target_x, enemy["x"] + speed)
                else:
                    enemy["x"] = max(target_x, enemy["x"] - speed)
            elif enemy["y"] != target_y:
                if enemy["y"] < target_y:
                    enemy["y"] = min(target_y, enemy["y"] + speed)
                else:
                    enemy["y"] = max(target_y, enemy["y"] - speed)

            if enemy["x"] == target_x and enemy["y"] == target_y:
                enemy["moving_to_end"] = not enemy["moving_to_end"]

        # JUMPERS
        if enemy["type"] == "jumper":
            if "jump_timer" not in enemy:
                enemy["jump_timer"] = 0
                enemy["vel_y"] = 0
                enemy["_ground_y"] = enemy["y"]

            enemy["jump_timer"] += 1
            if enemy["jump_timer"] >= enemy.get("jump_delay"):
                enemy["jump_timer"] = 0
                enemy["vel_y"] = -0.27 * enemy.get("jump_height")

            enemy["vel_y"] += 0.1
            enemy["y"] += enemy["vel_y"]

            if enemy["y"] > enemy["_ground_y"]:
                enemy["y"] = enemy["_ground_y"]
                enemy["vel_y"] = 0

    # PLATFORMS
    for platform in platform_data:
        if "moving_to_end" not in platform:
            platform["moving_to_end"] = True
            platform["_start_x"] = platform["x"]
            platform["_start_y"] = platform["y"]

        platform["old_x"] = platform["x"]
        platform["old_y"] = platform["y"]

        target_x = platform["end_x"] if platform["moving_to_end"] else platform["_start_x"]
        target_y = platform["end_y"] if platform["moving_to_end"] else platform["_start_y"]
        speed = platform.get("speed", 1)

        if platform["x"] != target_x:
            if platform["x"] < target_x:
                platform["x"] = min(target_x, platform["x"] + speed)
            else:
                platform["x"] = max(target_x, platform["x"] - speed)
        elif platform["y"] != target_y:
            if platform["y"] < target_y:
                platform["y"] = min(target_y, platform["y"] + speed)
            else:
                platform["y"] = max(target_y, platform["y"] - speed)

        if platform["x"] == target_x and platform["y"] == target_y:
            platform["moving_to_end"] = not platform["moving_to_end"]

def run_level(screen, clock, level: str, level_type: str = "standard") -> str:
    """Unified game runner for both standard and custom player maps."""
    
    load_level(level, level_type)

    exit_menu_state = "custom_levels" if level_type == "custom" else "levels"

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

    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    colliders = []
    danger = []
    end = []
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            world_x = x * tile_size
            world_y = y * tile_size

            if tile == 0:
                rect = pygame.Rect(world_x, world_y, tile_size, tile_size)
                colliders.append(rect)
            elif tile == 1:
                rect = pygame.Rect(world_x, world_y, tile_size, tile_size)
                danger.append(rect)
            elif tile == 2:  
                spawn_x = world_x
                spawn_y = world_y
            elif tile == 3:
                rect = pygame.Rect(world_x, world_y, tile_size, tile_size)
                end.append(rect)

    player = pygame.Rect(
        spawn_x + (tile_size - player_size) // 2, 
        spawn_y + (tile_size - player_size) // 2, 
        player_size, 
        player_size
    )
    player_real_x = float(player.x)

    def draw_and_check_button(btn, mouse_pos, mouse_clicked):
        pygame.draw.rect(screen, btn.color, btn.rect)
        if btn.text and btn.font:
            text_surf = btn.font.render(btn.text, True, btn.text_color)
            text_rect = text_surf.get_rect(center=btn.rect.center)
            screen.blit(text_surf, text_rect)
        if btn.rect.collidepoint(mouse_pos) and mouse_clicked:
            return True
        return False

    def show_menu_overlay(title_text):
        waiting = True
        while waiting:
            current_w = screen.get_width()
            current_h = screen.get_height()

            overlay = pygame.Surface((current_w, current_h), pygame.SRCALPHA)
            overlay.fill((25, 25, 25, 180)) 
            screen.blit(overlay, (0, 0))

            title_surf = nadpisy.render(title_text, True, white)
            title_rect = title_surf.get_rect(center=(current_w / 2, 40))
            screen.blit(title_surf, title_rect)

            btn_restart = Menu_Button(current_w / 2 - 200, 150, 400, 50, white, text="RESTART / RESUME", font=buttons_text, text_color=black)
            
            leave_label = "LEAVE TO CUSTOM LEVELS" if level_type == "custom" else "LEAVE TO LEVELS"
            btn_leave = Menu_Button(current_w / 2 - 200, 150 + 50 + 25, 400, 50, white, text=leave_label, font=buttons_text, text_color=black)

            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE and title_text == "GAME PAUSED":
                        return "resume"

            mouse_pos = pygame.mouse.get_pos()

            if draw_and_check_button(btn_restart, mouse_pos, mouse_clicked):
                return "restart" if (title_text == "GAME OVER" or title_text == "LEVEL WON") else "resume"
            
            if draw_and_check_button(btn_leave, mouse_pos, mouse_clicked):
                return "leave"

            pygame.display.update()
            clock.tick(FPS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    choice = show_menu_overlay("GAME PAUSED")
                    if choice == "leave":
                        return exit_menu_state

        keys = pygame.key.get_pressed()
        vel_x = 0

        if keys[pygame.K_SPACE] and on_ground:
            vel_y = jump_strength
            on_ground = False

        vel_y += gravity
        update_entities()

        camera_x = player.centerx - full_width // 2
        if camera_x < 0:
            camera_x = 0
        if camera_x > world_width - full_width:
            camera_x = world_width - full_width

        on_ground = False
        standing_platform = None

        player.y += vel_y 

        for platform in platform_data:
            platform_rect = pygame.Rect(platform["x"] * tile_size, platform["y"] * tile_size, tile_size, tile_size)
            platform_delta_y = (platform["y"] - platform["old_y"]) * tile_size

            if player.colliderect(platform_rect):
                if player.bottom - vel_y <= platform_rect.top + 2 or (platform_delta_y < 0 and player.top < platform_rect.bottom):
                    if vel_y >= 0:
                        player.bottom = platform_rect.top
                        vel_y = 0
                        on_ground = True
                        standing_platform = platform
                    player.y += platform_delta_y

        for tile in colliders:
            if player.colliderect(tile):
                if vel_y > 0:
                    player.bottom = tile.top
                    vel_y = 0
                    on_ground = True
                elif vel_y < 0:
                    player.top = tile.bottom
                    vel_y = 0

        if standing_platform:
            platform_delta_x = (standing_platform["x"] - standing_platform["old_x"]) * tile_size
        else:
            platform_delta_x = 0

        player_real_x += platform_delta_x

        if keys[pygame.K_d]:
            player_real_x += movement_strength
        elif keys[pygame.K_a]:
            player_real_x -= movement_strength

        future_rect = pygame.Rect(int(player_real_x), player.y, player.width, player.height)
        for tile in colliders:
            if future_rect.colliderect(tile):
                if player_real_x > player.x:
                    future_rect.right = tile.left
                elif player_real_x < player.x:
                    future_rect.left = tile.right
                player_real_x = future_rect.x

        player.x = int(player_real_x)

        is_dead = False
        
        if player.y > full_height:
            is_dead = True
        
        for collider in danger:
            if player.colliderect(collider):
                is_dead = True
                break

        for enemy in enemy_data:
            enemy_world_rect = pygame.Rect(enemy["x"] * tile_size, enemy["y"] * tile_size, tile_size, tile_size)
            if player.colliderect(enemy_world_rect):
                is_dead = True
                break

        if is_dead:
            death_sound.play() 
            
            choice = show_menu_overlay("GAME OVER")
            if choice == "restart":
                return run_level(screen, clock, level, level_type)
            elif choice == "leave":
                return exit_menu_state

        for collider in end:
            if player.colliderect(collider):
                choice = show_menu_overlay("LEVEL WON")
                if choice == "restart":
                    return run_level(screen, clock, level, level_type)
                elif choice == "leave":
                    return exit_menu_state

        draw_background(screen)

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile in tile_colors and tile_colors[tile] is not None:
                    pygame.draw.rect(screen, tile_colors[tile], (x * tile_size - camera_x, y * tile_size, tile_size, tile_size))
        
        for enemy in enemy_data:
            color = blue if enemy["type"] == "walker" else orange
            enemy_screen_rect = pygame.Rect(enemy["x"] * tile_size - camera_x, enemy["y"] * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, enemy_screen_rect)
            
        for platform in platform_data:
            platform_rect = pygame.Rect(platform["x"] * tile_size - camera_x, platform["y"] * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, purple, platform_rect)

        pygame.draw.rect(screen, yellow, (player.x - camera_x, player.y, player.width, player.height))

        level_num = level.replace("_data.json", "").replace("level", "")
        prefix = "CUSTOM " if level_type == "custom" else ""
        text = nadpisy.render(f"{prefix}LEVEL {level_num}", True, white)
        screen.blit(text, (20, 20))

        pause_text = nadpisy.render("Press ESC to pause", True, white)
        screen.blit(pause_text, (20, 50))

        pygame.display.update()
        clock.tick(FPS)