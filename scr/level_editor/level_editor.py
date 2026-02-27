import pygame
import json
import os

pygame.init()

clock = pygame.time.Clock()
FPS = 60

full_width = 800
full_height = 640

lower_margin = 100
side_margin = 300

screen = pygame.display.set_mode((full_width + side_margin, full_height + lower_margin))
pygame.display.set_caption('Level Editor')

#EVERYTHING TO DEFY FOR THE GAME

class Tile_button():
    def __init__(self, x, y, background, tile_id):
        self.background = background
        self.tile_id = tile_id
        # self.rect = self.background.get_rect()
        # self.rect.topleft = (x, y)
        self.rect = pygame.Rect(x, y, 64, 64)

    def draw(self, screen):
        # screen.blit(self.background, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.background, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                if self.rect.collidepoint(event.pos):
                    return True
        return False

class UI_Button():
    def __init__(self, x, y, width, height, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Tiles:
    def __init__(self):
        self.buttons = []

        self.buttons.append(Tile_button(full_width + 50, 50, white, 0))
        self.buttons.append(Tile_button(full_width + 125, 50, red, 1))
        self.buttons.append(Tile_button(full_width + 200, 50, green, 2))
        self.buttons.append(Tile_button(full_width + 50, 125, yellow, 3))

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
black = (0, 0, 0)
brown = (139, 69, 19)
gray = (120, 120, 120)
yellow = (255, 215, 0)

#font
nadpisy = pygame.font.SysFont("Futura", 30)

#tiles
tile_size = full_height // rows
tile_types = 12
current_tile = 0

tile_colors = {
    -1: None,
    0: white, 
    1: red,
    2: green,
    3: yellow
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
def outputing_text(text, font, text_col, x, y):
    write = font.render(text, True, text_col)
    screen.blit(write, (x, y))

def draw_background():
    screen.fill(gray)

def draw_grid():
    #verticaly
    for c in range(max_collums + 1):
        pygame.draw.line(screen, white, (c * tile_size - scroll, 0), (c * tile_size - scroll, full_height))

    #horizontaly
    for c in range(rows + 1):
        pygame.draw.line(screen, white, (0, c * tile_size), (full_width, c * tile_size))

def draw_world_tiles():
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
    global map_data  # IMPORTANT — we are modifying it

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

save_button = UI_Button(50, full_height + lower_margin - 75, 120, 50, green, action = save_level)
load_button = UI_Button(50 + 120 + 25, full_height + lower_margin - 75, 120, 50, white, action = load_level)

palette = Tiles()

running = True

while running:

    draw_background()
    draw_grid()  
    draw_world_tiles()
    outputing_text(f'Custom level: {level}', nadpisy, white, 50 + (120 + 25) * 2, full_height + lower_margin - 75)
    outputing_text(f'Press UP or DOWN to change level', nadpisy, white, 50 + (120 + 25) * 2, full_height + lower_margin - 45)

    #tile panel
    pygame.draw.rect(screen, gray, (full_width, 0, side_margin, full_height + 1))  

    palette.draw(screen)

    save_button.draw(screen)
    load_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

            if mouse_buttons[0]:  # left adds
                map_data[grid_y][grid_x] = palette.selected_tile

            if mouse_buttons[2]:  # right deletes
                map_data[grid_y][grid_x] = -1


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
