import pygame

pygame.init()
pygame.font.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player = pygame.Rect(50, 50, 50, 50)

platform1 = pygame.Rect(0, height - 50, width // 2, 50)
platform2 = pygame.Rect(300, height - 200, 200, 30)
platform3 = pygame.Rect(650, height - 350, 200, 30)
platform4 = pygame.Rect(950, height - 500, 200, 30)
platform5 = pygame.Rect(150, height - 400, 150, 30)

nono_block = pygame.Rect(1050, height - 550, 100, 50)

danger = [nono_block]
colliders = [platform1, platform2, platform3, platform4, platform5]

vel_y = 0
vel_x = 0

gravity = 1
jump_strength = -20
movement_strength = 10
on_ground = False

running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # horizontal reset
    vel_x = 0

    if keys[pygame.K_d]:
        vel_x = movement_strength
    if keys[pygame.K_a]:
        vel_x = -movement_strength

    # uppies
    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_strength
        on_ground = False

    # gravity
    vel_y += gravity

    #COLIDERS
    # horizontal bs
    player.x += vel_x

    for collider in colliders:
        if player.colliderect(collider):
            if vel_x > 0:
                player.right = collider.left
            elif vel_x < 0:
                player.left = collider.right

    # vertical bs
    player.y += vel_y
    on_ground = False

    for collider in colliders:
        if player.colliderect(collider):
            if vel_y > 0:
                player.bottom = collider.top
                vel_y = 0
                on_ground = True
            elif vel_y < 0:
                player.top = collider.bottom
                vel_y = 0

    # bro went too low
    if player.y > height:
        running = False

    # hitting blockdanger
    for collider in danger:
        if player.colliderect(collider):
            running = False


    # drawing
    screen.fill((0, 0, 106))
    pygame.draw.rect(screen, (255, 255, 255), player)

    pygame.draw.rect(screen, (0, 150, 150), platform1)
    pygame.draw.rect(screen, (0, 150, 150), platform2)
    pygame.draw.rect(screen, (0, 150, 150), platform3)
    pygame.draw.rect(screen, (0, 150, 150), platform4)
    pygame.draw.rect(screen, (0, 150, 150), platform5)

    pygame.draw.rect(screen, (150, 0, 0), nono_block)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
