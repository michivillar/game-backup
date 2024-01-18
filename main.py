import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battles")

# stuff for ball
dx, dy = 1, -1

# Colours
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 10)

# Important stuff
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
bullet_radius = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 

# Yellow spaceship stuff
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Red spaceship stuff
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


#Background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spacebg.webp')), (WIDTH, HEIGHT))
# Checks what key is being pressed

# wasd, yellow
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y-VEL>0: # Up
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL +yellow.height<HEIGHT: # Down
            yellow.y += VEL
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0: # Left
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL + yellow.width<WIDTH: # Right
            yellow.x += VEL

# udlr, red
def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y-VEL>0: # Up
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y+VEL +red.height<HEIGHT: # Down
            red.y += VEL
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>0: # Left
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL + red.width<WIDTH: # Right
            red.x += VEL

#function to handle bullets

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullets in yellow_bullets:
        bullets.x += BULLET_VEL
        if red.colliderect(bullets):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullets)
            if bullets.centerY < bullet_radius:
                dy = -dy
            if bullets.centerX < bullet_radius or bullets.centerX > WIDTH - bullet_radius:
                dx = -dx

    for bullets in red_bullets:
        bullets.x -= BULLET_VEL
        if yellow.colliderect(bullets):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullets)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0 ))

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    

    #to draw bullets on screen
    for bullets in red_bullets:
         pygame.draw.circle(WIN, RED, bullets)

    for bullets in yellow_bullets:
         pygame.draw.circle(WIN, YELLOW, bullets) 

    pygame.display.update()


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    #list for bullets
    red_bullets = []
    yellow_bullets = []

    #lists for health
    red_health = 5
    yellow_health = 5

    bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

# BULLETS AND KEYS TO SHOOT!!!!!!!!!!!!!!!!!!
            if event.type == pygame.KEYDOWN:
                #bullet for yellow, wasd
                if event.key == pygame.K_q and len(yellow_bullets)< MAX_BULLETS:
                    bullets = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullets)
                #bullet for red, udlr
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullets = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullets)

            if event.type == RED_HIT:
                red_health -= 1
             
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
           pass # SOMEONE WON
                    
        
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

         

    pygame.quit()

if __name__ == "__main__":
    main()

