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

class Tiles:
    def __init__(self):
        self.buttons = []

        self.buttons.append(Button(full_width + 50, 50, white, 0))
        self.buttons.append(Button(full_width + 125, 50, brown, 1))
        self.buttons.append(Button(full_width + 200, 50, gray, 2))
        self.buttons.append(Button(full_width + 50, 125, yellow, 3))

        self.selected_tile = 0

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

        pygame.draw.rect(
            screen,
            (0,0,0),
            self.buttons[self.selected_tile].rect,
            3
        )

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.selected_tile = button.tile_id

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

palette = Tiles()

running = True

while running:

    draw_background()
    draw_grid()  

    #tile panel
    pygame.draw.rect(screen, green, (full_width, 0, side_margin, full_height + 1))  

    palette.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        palette.handle_event(event)
        
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
        
    
    if scroll_left == True and scroll > 0:
        scroll -= 5 
    if scroll_right == True:
        scroll += 5 

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
