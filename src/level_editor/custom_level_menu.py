import pygame
import os
 
FPS = 60
current = "custom_levels"

full_width = 1100
full_height = 740

class Menu_Button():
    """A reusable UI element representing a clickable screen button.

    Handles positioning, geometric rendering, centering display text, 
    detecting left-clicks on its bounding box, and executing a pre-assigned 
    callback action when clicked.
    """

    def __init__(self, x: float, y: float, width: int, height: int, color: tuple, action=None, text: str = "", font=None, text_color: tuple = (0, 0, 0)) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action
        self.text = text
        self.text_color = text_color
        self.font = font

    def center_horizontally(self, screen) -> None:
        screen_w = screen.get_width()
        self.rect.x = (screen_w - self.rect.width) // 2

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

#color
green = (144, 201, 120)
white = (255, 255, 255)
red = (200, 25, 25)
black = (25, 25, 25)
brown = (139, 69, 19)
gray = (120, 120, 120)
yellow = (255, 215, 0)

def get_available_levels() -> list:
    """Finds and indexes available game levels from local files.

    Scans the designated 'levels' directory for files that strictly follow 
    the format naming rule 'level..._data.json', and returns an alphabetically 
    sorted list of those filenames.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "custom_levels")
    if not os.path.exists(folder):
        return []
    return sorted([f for f in os.listdir(folder) if f.startswith("level") and f.endswith("_data.json")])

def to_menu() -> str:
    return "menu"

def to_level(level_name: str) -> tuple:
    return ("custom", level_name)

def run_custom_menu(screen, clock) -> tuple | str:
    """Handles running and the functionality of the level selection menu.

    Dynamically populates the screen with selectable buttons for every discovered 
    level file. It manages the loop that listens for mouse clicks on buttons, 
    handles background rendering, and forwards navigation states back to the game controller.
    """

    #font
    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    levels = get_available_levels()

    buttons = []
    y_start = 50
    for i, level_file in enumerate(levels):
        clean_text = level_file.replace("_data.json", "").replace("level", "LEVEL ")
        buttons.append(Menu_Button(full_width/2 - 200, y_start + i * 60, 400, 50, green, action = lambda f=level_file: to_level(f), text = clean_text, font = buttons_text, text_color = black))

    back_button = Menu_Button(full_width - 120 - 25, full_height - 75, 120, 50, white, action = to_menu, text = "MAIN MENU", font = buttons_text, text_color = black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            for button in buttons:
                result = button.handle_event(event)
                if result:
                    return result

            result = back_button.handle_event(event)
            if result:
                return result

        screen.fill(gray)
        
        for button in buttons:
            button.center_horizontally(screen)
            button.draw(screen)
            
        back_button.draw(screen)

        pygame.display.update()
        clock.tick(FPS)