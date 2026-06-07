import pygame
 
FPS = 60
current = "menu"

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

    # --- ADDED THIS METHOD SO THE CLASS HAS THE ATTRIBUTE ---
    def center_horizontally(self, screen) -> None:
        """Dynamically centers the button horizontally based on the current screen width."""
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

def to_editor() -> str:
    """Returns the routing target state for the level editor suite."""
    return "editor"

def to_custom_levels() -> str:
    """Returns the routing target state for the custom levels selection menu."""
    return "custom_levels"

def to_levels() -> str:
    """Returns the routing target state for the standard built-in levels selection menu."""
    return "levels"

def quit_game() -> None:
    """Gracefully terminates the Pygame engine initialization and kills the runtime process."""
    pygame.quit()
    exit()

#color
green = (144, 201, 120)
white = (255, 255, 255)
red = (200, 25, 25)
black = (25, 25, 25)
brown = (139, 69, 19)
gray = (120, 120, 120)
yellow = (255, 215, 0)

def run_menu(screen, clock) -> str:
    """Handles running and the functionality of the main menu.

    Runs an independent loop that constructs and displays the primary 
    navigation screen. It initializes layout buttons for game modes, listens 
    for mouse interaction events, and returns state-change instructions 
    back to the master game loop when a selection is made.
    """

    #font
    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    level_button = Menu_Button(0, 75, 400, 50, white, action = to_levels, text = "LEVELS", font = buttons_text, text_color = black)
    editor_button = Menu_Button(0, 75 + 50 + 25, 400, 50, white, action = to_editor, text = "LEVEL EDITOR", font = buttons_text, text_color = black)
    custom_levels_button = Menu_Button(0, 75 + 50 + 25 + 50 + 25, 400, 50, white, action = to_custom_levels, text = "CUSTOM LEVELS", font = buttons_text, text_color = black)
    quit_game_button = Menu_Button(0, 75 + 50 + 25 + 50 + 25 + 50 + 25, 400 , 50, white, action = quit_game, text = "QUIT GAME", font = buttons_text, text_color = black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            result = level_button.handle_event(event)
            if result:
                return result
            
            result = editor_button.handle_event(event)
            if result:
                return result

            result = custom_levels_button.handle_event(event)
            if result:
                return result

            result = quit_game_button.handle_event(event)
            if result:
                return result
        
        screen.fill(gray)

        fullscreen_text = nadpisy.render("Press F11 for fullscreen", True, white)
        screen.blit(fullscreen_text, (20, 20))
        
        level_button.center_horizontally(screen)
        editor_button.center_horizontally(screen)
        custom_levels_button.center_horizontally(screen)
        quit_game_button.center_horizontally(screen)
        
        level_button.draw(screen)
        editor_button.draw(screen)
        custom_levels_button.draw(screen)
        quit_game_button.draw(screen)

        pygame.display.update()
        clock.tick(FPS)