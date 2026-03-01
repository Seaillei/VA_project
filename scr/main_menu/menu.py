import pygame
 
FPS = 60
current = "menu"

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
                    return self.action()
        return None

def to_editor():
    return "editor"

def to_custom_levels():
    return "custom_levels"

def quit_game():
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

def run_menu(screen, clock):
    #font
    nadpisy = pygame.font.SysFont("Futura", 28)
    buttons_text = pygame.font.SysFont("Futura", 15)

    editor_button = Menu_Button(full_width/2 - 60, 75, 120, 50, white, action = to_editor, text = "LEVEL EDITOR", font = buttons_text, text_color = black)
    custom_levels_button = Menu_Button(full_width/2 - 60, 75 + 50 + 25, 120, 50, white, action = to_custom_levels, text = "CUSTOM LEVELS", font = buttons_text, text_color = black)
    quit_game_button = Menu_Button(full_width/2 - 60, 75 + 50 + 25 + 50 + 25, 120, 50, white, action = quit_game, text = "QUIT GAME", font = buttons_text, text_color = black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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

        editor_button.draw(screen)
        custom_levels_button.draw(screen)
        quit_game_button.draw(screen)

        pygame.display.update()
        clock.tick(FPS)
