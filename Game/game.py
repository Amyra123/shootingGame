import pygame
import math
import random

from pygame import mixer
# initialize pygame
pygame.init()

#create screen
screen_height = 600
screen_width = 800

screen = pygame.display.set_mode((screen_width,screen_height))

# set caption
pygame.display.set_caption('shoot corona')

# set icon
icon = pygame.image.load('player1.png')
pygame.display.set_icon(icon)

# bg image
bg = pygame.image.load('bg3.jpeg')

flag = 0

# bg music
mixer.music.load('background.wav')

mixer.music.play(-1)
# create enemy
enemy_img=[]
enemyX=[]
enemyY = []
enemyX_change = []
enemyY_change = []
number = 10

for i in range(number):
    
    enemy_img.append(pygame.image.load('virus.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# create player
player_img = pygame.image.load('arrow.png')
playerX = 360
playerY = 536
playerX_change = 0

# create bullet
bullet_img = pygame.image.load('bullet2.png')
bx = 0
by = 536
by_change = 5
bx_change = 0
bullet_state = "ready"

# bullet function
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    
    screen.blit(bullet_img,(x + 26,y - 35))

# player function
def player(x,y):
    screen.blit(player_img,(x,y))
    
# enemy function
def enemy(x,y):
    screen.blit(enemy_img[i],(x,y))
    
# collision detection
def is_collision(ex,ey,bx,by):
    distance = math.sqrt(math.pow(ex-bx , 2) + math.pow(ey -by , 2))
    if(distance < 30):
        return True
    else:
        return False

# score
score=0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY =10

# game over
game_over_text = pygame.font.Font('freesansbold.ttf',64)

def game_over_txt():
        game_overtext = game_over_text.render("GAME OVER",True,(255,255,255))
        screen.blit(game_overtext , (200,250))

def display_score(x,y):
    sc = font.render("score: " + str(score) , True,(255,255,255))
    screen.blit(sc,(x,y))
    
# main game loop

running= True
while(running):
    
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    
    if flag == 1:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bx=playerX
                    fire_bullet(bx,by)
                
        elif event.type == pygame.KEYUP:
            if(event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                playerX_change = 0
                
                
    
    # player
    playerX += playerX_change
    
    if playerX <= 0:
        playerX=0
    if playerX >= 736 :
        playerX=736
    player(playerX,playerY)
    
    # collision detection
    
    for i in range(number):
        collision = is_collision(enemyX[i],enemyY[i],bx,by)
        if collision:
            ex_sound = mixer.Sound('explosion.wav')
            ex_sound.play()
            by = 536
            bullet_state ="ready"
        
            enemyX[i] = random.randint (0,736)
            enemyY[i] = random.randint (50,150)
            score+=1
        
    # enemy movement
    
    for i in range(number):
        if enemyY[i] > 460:
            for j in range(number):
                enemyY[j] = 2000
            game_over_txt()
            flag = 1
            break
       
        
        enemyX[i] +=enemyX_change[i]
    
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        
        if enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        
    # bullet movement
    
    if by <= 0:
        by = 536
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bx, by)
        by -= by_change
    
    for i in range(number):
        enemy(enemyX[i],enemyY[i])
        
    display_score(textX,textY)
    
    pygame.display.update()

while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
if running == False:
    pygame.quit()
