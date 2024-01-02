import pygame
import random
import time
pygame.font.init()

#create a window
WIDTH, HEIGHT = 800, 650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Say No To Drugs")

#load images
BG = pygame.transform.scale(pygame.image.load("bg.png"),(WIDTH,HEIGHT))
BIN = pygame.transform.scale2x(pygame.image.load("bin.png"))
PILL = pygame.transform.scale2x(pygame.image.load("pill.png"))

#player
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 120
PLAYER_VEL = 10

#font
FONT = pygame.font.SysFont("comicsans",30)

#pill
PILL_WIDTH = 100
PILL_HEIGHT = 30
PILL_VEL = 4

def draw(player,elapsed_time,pills,count):
    WIN.blit(BG,(0,0))
    WIN.blit(BIN,player)
    time_text = FONT.render(f"Time: {round(elapsed_time)}s",1,"white")
    WIN.blit(time_text,(10,10))
    for pill in pills:
        WIN.blit(PILL,pill)
    count_text = FONT.render(f"Pills Destroyed: {count}",1,"white")
    WIN.blit(count_text,(WIDTH-280,10))

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,
                         PLAYER_WIDTH,PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    pill_inc = 400
    pill_count = 0

    pills = []
    hit = True

    count = 0

    while run:
        pill_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if pill_count > pill_inc:
            pill_x = random.randint(0,WIDTH-PILL_WIDTH)
            pill = pygame.Rect(pill_x,-PILL_HEIGHT,PILL_WIDTH,PILL_HEIGHT)
            pills.append(pill)

            pill_inc = min(700,pill_count+50)
            pill_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x-PLAYER_VEL>=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x+PLAYER_WIDTH+PLAYER_VEL<=WIDTH:
            player.x += PLAYER_VEL
        
        for pill in pills[:]:
            pill.y += PILL_VEL
            if pill.y + pill.height >= player.height and pill.colliderect(player):
                count += 1
                pills.remove(pill)
            elif pill.y > HEIGHT:
                pills.remove(pill)
                hit = False
                break
        
        if not hit:
            lost_text = FONT.render(f"YOU DESTROYED {count} PILLS",1,"white")
            WIN.blit(lost_text,(WIDTH/2-lost_text.get_width()/2, HEIGHT/2-lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player,elapsed_time,pills,count)

    pygame.quit()

if __name__ == "__main__":
    main()
