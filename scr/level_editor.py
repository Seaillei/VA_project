import pygame

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

class Button():
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

#tiles
tile_size = full_height // rows
tile_types = 12
current_tile = 0

#functions
def draw_background():
    screen.fill(green)

def draw_grid():
    #verticaly
    for c in range(max_collums + 1):
        pygame.draw.line(screen, white, (c * tile_size - scroll, 0), (c * tile_size - scroll, full_height))

    #horizontaly
    for c in range(rows + 1):
        pygame.draw.line(screen, white, (0, c * tile_size), (full_width, c * tile_size))

#buttons
button_list = []
button_col = 0
button_row = 0
for i in range(tile_types):
    tile_button = Button(full_width + (75* button_col) + 50, 75 * button_row + 50, red, 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

running = True

while running:

    draw_background()
    draw_grid()  

    #tile panel
    pygame.draw.rect(screen, green, (full_width, 0, side_margin, full_height + 1))

    #choose a tile
    for button in button_list:
        button.draw(screen)

    # highlight selected tile
    pygame.draw.rect(screen, black, button_list[current_tile].rect, 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
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
        
        for index, button in enumerate(button_list):
            if button.is_clicked(event):
                current_tile = index
    
    if scroll_left == True and scroll > 0:
        scroll -= 5 
    if scroll_right == True:
        scroll += 5 

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()