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
    def __init__(self, x, y, background, tile_id, font, text="", text_color=(0,0,0)):
        self.background = background
        self.tile_id = tile_id
        # self.rect = self.background.get_rect()
        # self.rect.topleft = (x, y)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, 64, 64)

    def draw(self, screen):
        # screen.blit(self.background, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.background, self.rect)

        if self.text != "":
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)

            screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                if self.rect.collidepoint(event.pos):
                    return True
        return False

class UI_Button():
    def __init__(self, x, y, width, height, color, action=None, text="", font=None, text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action
        self.text = text
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        if self.text != "":
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)

            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Tiles:
    def __init__(self, font):
        self.buttons = []

        self.buttons.append(Tile_button(full_width + 50, 50, white, 0, font, "TILE", black))
        self.buttons.append(Tile_button(full_width + 125, 50, red, 1, font, "DAMAGE", black))
        self.buttons.append(Tile_button(full_width + 200, 50, green, 2, font, "START-flag", black))
        self.buttons.append(Tile_button(full_width + 50, 125, black, 3, font, "FINISH-flag", white))

        self.selected_tile = 0

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

        pygame.draw.rect(screen,(0,0,0),self.buttons[self.selected_tile].rect,3)

    def handle_event(self, event):
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
black = (25, 25, 25)
brown = (139, 69, 19)
gray = (120, 120, 120)
yellow = (255, 215, 0)

#tiles
tile_size = full_height // rows
tile_types = 12
current_tile = 0

tile_colors = {
    -1: None,
    0: white, 
    1: red,
    2: green,
    3: black
}

# tile_images = {
#     1: grass_image,
#     2: stone_image,
#     3: coin_image
# }
# screen.blit(tile_images[tile], position)

#empty tile list

map_data = []
for row in range(rows):
    all_rows = [-1] * max_collums
    map_data.append(all_rows)   

#functions
def outputing_text(text, font, text_col, x, y, screen):
    write = font.render(text, True, text_col)
    screen.blit(write, (x, y))

def draw_background(screen):
    screen.fill(gray)

def draw_grid(screen):
    #verticaly
    for c in range(max_collums + 1):
        pygame.draw.line(screen, white, (c * tile_size - scroll, 0), (c * tile_size - scroll, full_height))

    #horizontaly
    for c in range(rows + 1):
        pygame.draw.line(screen, white, (0, c * tile_size), (full_width, c * tile_size))

def draw_world_tiles(screen):
     for y, row in enumerate(map_data):
         for x, tile in enumerate(row):
            if tile != -1:
                color = tile_colors[tile]

                pygame.draw.rect(screen, color, (x * tile_size - scroll,y * tile_size, tile_size, tile_size))

def save_level():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"level{level}_data.json")

    with open(filename, "w") as f:
        json.dump(map_data, f)

def load_level():
    scroll = 0
    global map_data  #modifying

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    filename = os.path.join(folder, f"level{level}_data.json")

    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                map_data = json.load(f)
            print(f"Loaded level from: {filename}")
        except Exception as e:
            print("Failed to load level:", e)
    else:
        print("Level file does not exist!")


def run_editor(screen, clock):

    global scroll_left, scroll_right, scroll
    global level

    scroll_left = False
    scroll_right = False
    scroll = 0

    #font
    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    palette = Tiles(buttons_text)
    save_button = UI_Button(50, full_height + lower_margin - 75, 120, 50, white, action = save_level, text = "SAVE LEVEL", font = buttons_text, text_color = black)
    load_button = UI_Button(50 + 120 + 25, full_height + lower_margin - 75, 120, 50, white, action = load_level, text = "LOAD LEVEL", font = buttons_text, text_color = black)

    editor_running = True
    while editor_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

            palette.handle_event(event)
            save_button.handle_event(event)
            load_button.handle_event(event)
            
            #scrollovani
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    scroll_left = True
                if event.key == pygame.K_d:
                    scroll_right = True
            
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

        draw_background(screen)
        draw_grid(screen)  
        draw_world_tiles(screen)
        #tile panel
        pygame.draw.rect(screen, gray, (full_width, 0, side_margin, full_height + 1))  

        palette.draw(screen)
        
        outputing_text(f'Custom level: {level}', nadpisy, white, 50 + (120 + 25) * 2, full_height + lower_margin - 80, screen)
        outputing_text(f'Press UP or DOWN to change level', nadpisy, white, 50 + (120 + 25) * 2, full_height + lower_margin - 60, screen)
        outputing_text(f'Press ESC to return to the menu', nadpisy, white, 50 + (120 + 25) * 2, full_height + lower_margin - 40, screen)

        save_button.draw(screen)
        load_button.draw(screen)
            

        if scroll_left == True and scroll > 0:
            scroll -= 5 
        if scroll_right == True and scroll < (max_collums * tile_size) - full_width:
            scroll += 5 

        #placing blox in the grid
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_x < full_width and mouse_y < full_height:

            grid_x = (mouse_x + scroll) // tile_size
            grid_y = mouse_y // tile_size

            if 0 <= grid_y < rows and 0 <= grid_x < max_collums:

                if mouse_buttons[0]:  #left adds
                    tile = palette.selected_tile

                    if tile in (2, 3):  #start and finish

                        #Remove old start and finih
                        for y, row in enumerate(map_data):
                            for x, value in enumerate(row):
                                if value == tile:
                                    map_data[y][x] = -1

                    map_data[grid_y][grid_x] = tile

                if mouse_buttons[2]:  #right deletes
                    map_data[grid_y][grid_x] = -1


        pygame.display.update()
        clock.tick(FPS)
