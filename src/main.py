import pygame
from level_editor.level_editor import run_editor
from level_editor.custom_level_menu import run_custom_menu
from level_editor.custom_level import run_custom_level
from main_menu.menu import run_menu
from level.level_menu import run_level_menu
from level.level import run_level

full_width = 1100
full_height = 740

def main():
    global current_state
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('GAME')
    screen = pygame.display.set_mode((full_width, full_height))

    current_state = "menu"

    running = True

    while running:
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
            if level_type == "custom":
                current_state = run_custom_level(screen, clock, level_name)
            elif level_type == "standard":
                current_state = run_level(screen, clock, level_name)

main()
