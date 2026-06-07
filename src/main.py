import pygame
from level_editor.level_editor import run_editor
from level_editor.custom_level_menu import run_custom_menu
from main_menu.menu import run_menu
from level.level_menu import run_level_menu
from level.level import run_level

full_width = 1100
full_height = 740

def main() -> None:
    """Handles loading different parts of the game.
    
    Initializes the Pygame modules, sets up the display window, and manages 
    the core game loop. It acts as a state controller, continuously switching 
    between menus, the level editor, and active gameplay based on the value 
    of the global game state.
    """

    global current_state
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('GAME')
    screen = pygame.display.set_mode((full_width, full_height))

    current_state = "menu"

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

        if current_state == "menu":
            current_state = run_menu(screen, clock)

        elif current_state == "editor":
            current_state = run_editor(screen, clock)
        
        elif current_state == "custom_levels":
            current_state = run_custom_menu(screen, clock)

        elif current_state == "levels":
            current_state = run_level_menu(screen, clock)

        elif isinstance(current_state, tuple):
            level_type, level_name = current_state
            current_state = run_level(screen, clock, level_name, level_type = level_type)
            
    pygame.quit()

if __name__ == "__main__":
    main()
