import pygame
import os

FPS = 60
current = "custom_levels"

full_width = 1100
full_height = 740

class Menu_Button():
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

#color
green = (144, 201, 120)
white = (255, 255, 255)
red = (200, 25, 25)
black = (25, 25, 25)
brown = (139, 69, 19)
gray = (120, 120, 120)
yellow = (255, 215, 0)

def get_available_levels():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    if not os.path.exists(folder):
        return []
    return sorted([f for f in os.listdir(folder) if f.startswith("level") and f.endswith("_data.json")])

def to_custom_levels():
    global current
    current = "menu"

def run_custom_menu(screen, clock):
    global current

    #font
    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    levels = get_available_levels()

    buttons = []
    y_start = 50
    for i, level_file in enumerate(levels):
        buttons.append(Menu_Button(full_width/2 - 100, y_start + i * 60, 200, 50, green, action = lambda f=level_file: print(f"Load {f} here"), text=level_file.replace("_data.json","").upper(), font=buttons_text, text_color=(0,0,0)))

    back_button = Menu_Button(60, 75, 120, 50, white, action = to_custom_levels,text="MAIN MENU", font=buttons_text, text_color=black)

    custom_levels_running = True

    while custom_levels_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            for button in buttons:
                button.handle_event(event)
            back_button.handle_event(event)

        screen.fill(gray)
        for button in buttons:
            button.draw(screen)
        back_button.draw(screen)

        if current != "custom_levels":
            return current

        pygame.display.update()
        clock.tick(FPS)