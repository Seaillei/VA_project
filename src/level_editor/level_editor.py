import pygame
import json
import os
 

FPS = 60

full_width = 800
full_height = 640

lower_margin = 100
side_margin = 300

#EVERYTHING TO DEFY FOR THE GAME

class Tile_button():
    """A specialized button component representing an item in the editor palette.

    Manages fixed-size squares (64x64 pixels) containing tile types, hazards, 
    or entity definitions. It handles rendering its assigned identification text 
    and checks if the mouse left-clicked its boundaries.
    """

    def __init__(self, x: float, y: float, background: tuple, tile_id: int, font, text: str = "", text_color: tuple = (0, 0, 0)) -> None:
        self.background = background
        self.tile_id = tile_id
        # self.rect = self.background.get_rect()
        # self.rect.topleft = (x, y)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, 64, 64)

    def draw(self, screen) -> None:
        # screen.blit(self.background, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.background, self.rect)

        if self.text != "":
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)

            screen.blit(text_surface, text_rect)

    def is_clicked(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                if self.rect.collidepoint(event.pos):
                    return True
        return False

class UI_Button():
    """A general-purpose button component for application controls.

    Manages layout execution tasks for the tool interface, rendering background 
    shapes and text prompts. It evaluates event clicks to fire action callback triggers.
    """

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

class Tiles:
    """Manages the editor's item selection layout panel.

    Constructs a structural panel array of selectable game elements on the sidebar. 
    It tracks which entity or environmental block index is active for painting 
    actions and highlights the active selection with a clean border outline.
    """

    def __init__(self, font) -> None:
        self.buttons = []

        self.buttons.append(Tile_button(full_width + 50, 50, white, 0, font, "TILE", black))
        self.buttons.append(Tile_button(full_width + 125, 50, red, 1, font, "DAMAGE", black))
        self.buttons.append(Tile_button(full_width + 200, 50, green, 2, font, "START-flag", black))
        self.buttons.append(Tile_button(full_width + 50, 125, black, 3, font, "FINISH-flag", white))
        self.buttons.append(Tile_button(full_width + 125, 125, blue, 4, font, "WALKER", white))
        self.buttons.append(Tile_button(full_width + 200, 125, orange, 5, font, "JUMPER", black))
        self.buttons.append(Tile_button(full_width + 50, 200, purple, 6, font, "PLATFORM", white))

        self.selected_tile = 0

    def draw(self, screen) -> None:
        for button in self.buttons:
            button.draw(screen)

        pygame.draw.rect(screen,(0,0,0),self.buttons[self.selected_tile].rect,3)

    def handle_event(self, event) -> None:
        for button in self.buttons:
            if button.is_clicked(event):
                self.selected_tile = button.tile_id
#level
level = 0

#sizes
rows = 16
max_collums = 150

#scrolling
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

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

# tile_images = {
#     1: grass_image,
#     2: stone_image,
#     3: coin_image
# }
# screen.blit(tile_images[tile], position)

#empty tile list

map_data = []
enemy_data = []
platform_data = []

for row in range(rows):
    all_rows = [-1] * max_collums
    map_data.append(all_rows)   

#functions
def outputing_text(text: str, font, text_col: tuple, x: float, y: float, screen) -> None:
    write = font.render(text, True, text_col)
    screen.blit(write, (x, y))

def draw_background(screen) -> None:
    screen.fill(gray)

def draw_grid(screen) -> None:
    for c in range(max_collums + 1):
        line_x = c * tile_size - scroll
        if 0 <= line_x <= full_width:
            pygame.draw.line(screen, white, (line_x, 0), (line_x, full_height))

    for c in range(rows + 1):
        pygame.draw.line(screen, white, (0, c * tile_size), (full_width, c * tile_size))

def draw_world_tiles(screen, placing_object: dict | None = None) -> None:
    """Handles rendering the map grid tiles and placement previews.

    Loops through the 2D map array to draw static environmental blocks adjusted 
    for camera scroll. If a user is currently plotting a two-stage path object 
    (like a walker or moving platform), it overlays a temporary ghost tile 
    at the designated start coordinates.
    """

    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile != -1:
                color = tile_colors[tile]
                pygame.draw.rect(screen, color, (x * tile_size - scroll, y * tile_size, tile_size, tile_size))

    # Draw the temporary start for walker/platform
    if placing_object is not None:
        px = placing_object["start_x"] * tile_size - scroll
        py = placing_object["start_y"] * tile_size
        color = blue if placing_object["type"] == "walker" else purple
        pygame.draw.rect(screen, color, (px, py, tile_size, tile_size))

def draw_enemies(screen) -> None:
    """Handles rendering all active enemy types onto the screen.

    Iterates through the enemy database to determine whether a placement 
    represents a 'walker' or a 'jumper'. It scales their coordinate values into 
    pixel screen spaces and offsets them based on horizontal camera panning.
    """

    for enemy in enemy_data:
        x = enemy["x"] * tile_size - scroll
        y = enemy["y"] * tile_size

        if enemy["type"] == "walker":
            pygame.draw.rect(screen, blue, (x, y, tile_size, tile_size))

        if enemy["type"] == "jumper":
            pygame.draw.rect(screen, orange, (x, y, tile_size, tile_size))

def draw_platforms(screen) -> None:
    """Handles rendering moving platforms onto the screen layout.

    Processes positions tracked inside the platform configuration array, 
    drawing color-coded rectangles adjusted to align properly with active 
    world camera scrolling coordinates.
    """

    for platform in platform_data:
        x = platform["x"] * tile_size - scroll
        y = platform["y"] * tile_size

        pygame.draw.rect(screen, purple, (x, y, tile_size, tile_size))

def draw_paths(screen) -> None:
    """Handles rendering the movement paths of patrols and platforms.

    Calculates geometric center coordinates for path points, drawing explicit 
    connecting lines from an entity's initial placement point to its final destination 
    boundaries to visually chart movement ranges inside the layout workspace.
    """

    #walker paths
    for enemy in enemy_data:
        if enemy["type"] == "walker" and "end_x" in enemy and "end_y" in enemy:
            start_x = enemy["x"]
            start_y = enemy["y"]
            end_x = enemy["end_x"]
            end_y = enemy["end_y"]

            start_pos = (start_x * tile_size - scroll + tile_size // 2,start_y * tile_size + tile_size // 2)
            middle_pos = (end_x * tile_size - scroll + tile_size // 2,start_y * tile_size + tile_size // 2)
            end_pos = (end_x * tile_size - scroll + tile_size // 2,end_y * tile_size + tile_size // 2)

            pygame.draw.line(screen, white, start_pos, middle_pos, 3)
            pygame.draw.line(screen, white, middle_pos, end_pos, 3)

    #platform paths
    for platform in platform_data:
        if "end_x" in platform and "end_y" in platform:
            start_x = platform["x"]
            start_y = platform["y"]
            end_x = platform["end_x"]
            end_y = platform["end_y"]

            start_pos = (start_x * tile_size - scroll + tile_size // 2,start_y * tile_size + tile_size // 2)
            middle_pos = (end_x * tile_size - scroll + tile_size // 2,start_y * tile_size + tile_size // 2)
            end_pos = (end_x * tile_size - scroll + tile_size // 2,end_y * tile_size + tile_size // 2)

            pygame.draw.line(screen, white, start_pos, middle_pos, 3)
            pygame.draw.line(screen, white, middle_pos, end_pos, 3)

def save_level() -> None:
    """Serializes the current grid setup into an external file.

    Packages the existing map structure matrix, enemy dictionary configurations, 
    and path tracking platforms into a clean nested file layout, saving it inside 
    the 'custom_levels' folder using a JSON naming pattern.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"level{level}_data.json")

    level_data = {
        "tiles": map_data,
        "enemies": enemy_data,
        "platforms": platform_data
    }

    with open(filename, "w") as f:
        json.dump(level_data, f)
    print("Level saved")

def load_level() -> None:
    """Loads a saved file composition back into memory.

    Attempts to locate and parse a level file matching the targeted global index. 
    If found, it safely resets any active geometry arrays, updating the editor 
    grid state back to the historical save point.
    """

    scroll = 0
    global map_data  #modifying
    global enemy_data
    global platform_data

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    filename = os.path.join(folder, f"level{level}_data.json")

    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                level_data = json.load(f)

                map_data.clear()
                map_data.extend(level_data.get("tiles", []))

                enemy_data.clear()
                enemy_data.extend(level_data.get("enemies", []))

                platform_data.clear()
                platform_data.extend(level_data.get("platforms", []))
                
                print("Level loaded")
        except Exception as e:
            print("Failed to load level:", e)
    else:
        print("Level file does not exist!")

def to_menu() -> str:
    return "menu"

def run_editor(screen, clock) -> str:
    """Manages the full loop system for the map composition suite.

    Runs the level editor mode. It continuously tracks mouse coordinate grid snaps, 
    interprets keyboard scroll speeds, processes placement patterns for two-stage 
    path variables (Walkers and Platforms), updates live layer view screens, and 
    cleans deleted coordinates upon right-click actions.
    """

    global scroll_left, scroll_right, scroll
    global level

    placing_object = None

    scroll_left = False
    scroll_right = False
    scroll = 0

    #font
    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    palette = Tiles(buttons_text)
    save_button = UI_Button(50, full_height + lower_margin - 75, 120, 50, white, action = save_level, text = "SAVE LEVEL", font = buttons_text, text_color = black)
    load_button = UI_Button(50 + 120 + 25, full_height + lower_margin - 75, 120, 50, white, action = load_level, text = "LOAD LEVEL", font = buttons_text, text_color = black)
    back_button = UI_Button(side_margin + full_width - 120 - 25, full_height + lower_margin - 75, 120, 50, white, action = to_menu, text = "MAIN MENU", font = buttons_text, text_color = black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            palette.handle_event(event)
            save_button.handle_event(event)
            load_button.handle_event(event)

            result = back_button.handle_event(event)
            if result:
                return result
            
            #scrollovani
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    scroll_left = True
                if event.key == pygame.K_d:
                    scroll_right = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:         
                    pygame.display.toggle_fullscreen()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    scroll_left = False
                if event.key == pygame.K_d:
                    scroll_right = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    level += 1
                if event.key == pygame.K_DOWN:
                    level -= 1

            #placing blox in the grid
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if mouse_x < full_width and mouse_y < full_height:

                    grid_x = (mouse_x + scroll) // tile_size
                    grid_y = mouse_y // tile_size

                    if 0 <= grid_y < rows and 0 <= grid_x < max_collums:

                        if event.button == 1:  #left adds
                            tile = palette.selected_tile

                            if tile == 5:
                                enemy_data.append({
                                    "type": "jumper",
                                    "x": grid_x,
                                    "y": grid_y,
                                    "jump_height": 3,
                                    "jump_delay": 180
                                })

                            if tile == 4:
                                if placing_object is None:
                                    placing_object = {
                                        "type": "walker",
                                        "start_x": grid_x,
                                        "start_y": grid_y
                                    }
                                else:
                                    enemy_data.append({
                                        "type": "walker",
                                        "x": placing_object["start_x"],
                                        "y": placing_object["start_y"],
                                        "end_x": grid_x,
                                        "end_y": grid_y,
                                        "speed": 0.1
                                    })
                                    placing_object = None

                            if tile == 6:
                                if placing_object is None:
                                    placing_object = {
                                        "type": "platform",
                                        "start_x": grid_x,
                                        "start_y": grid_y
                                    }
                                else:
                                    platform_data.append({
                                        "x": placing_object["start_x"],
                                        "y": placing_object["start_y"],
                                        "end_x": grid_x,
                                        "end_y": grid_y,
                                        "speed": 0.1
                                    })
                                    placing_object = None

        draw_background(screen)
        draw_grid(screen)  
        draw_world_tiles(screen, placing_object)
        draw_enemies(screen)
        draw_platforms(screen)
        draw_paths(screen)

        #tile panel
        pygame.draw.rect(screen, gray, (full_width, 0, side_margin, full_height + 1))  

        palette.draw(screen)
        
        outputing_text(f'Custom level: {level}', nadpisy, white, 50 + (120 + 25) * 2, full_height + lower_margin - 72, screen)
        outputing_text(f'Press UP or DOWN to change level', nadpisy, white, 50 + (120 + 25) * 2, full_height + lower_margin - 48, screen)

        save_button.draw(screen)
        load_button.draw(screen)
        back_button.draw(screen)
            

        if scroll_left == True and scroll > 0:
            scroll -= 5 
        if scroll_right == True and scroll < (max_collums * tile_size) - full_width:
            scroll += 5 

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_x < full_width and mouse_y < full_height:
            grid_x = (mouse_x + scroll) // tile_size
            grid_y = mouse_y // tile_size

            if 0 <= grid_y < rows and 0 <= grid_x < max_collums:
                #left draw
                if mouse_buttons[0]:
                    tile = palette.selected_tile
                    if tile <= 3:  #tiles
                        map_data[grid_y][grid_x] = tile

                #right delete
                if mouse_buttons[2]:
                    map_data[grid_y][grid_x] = -1

                    enemy_data[:] = [
                        enemy for enemy in enemy_data
                        if not (
                            (enemy["x"] == grid_x and enemy["y"] == grid_y)  #start
                            or
                            (enemy.get("end_x") == grid_x and enemy.get("end_y") == grid_y)  #end
                        )
                    ]

                    #Remove platform 
                    platform_data[:] = [
                        platform for platform in platform_data
                        if not (
                            (platform["x"] == grid_x and platform["y"] == grid_y)  #start
                            or
                            (platform.get("end_x") == grid_x and platform.get("end_y") == grid_y)  #end
                        )
                    ]

                    # user placing new entity cancel it if start is deleted
                    if placing_object is not None:
                        if placing_object["start_x"] == grid_x and placing_object["start_y"] == grid_y:
                            placing_object = None

        pygame.display.update()
        clock.tick(FPS)