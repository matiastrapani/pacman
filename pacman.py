import pygame, sys
from pygame.locals import *
import pacPlayer
import ghostPlayer
import renderNumber
from ghostIA import *
    
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

def intro_seq():
    intro.play()
    screen.blit(fondo, (0, 0))
    screen.blit(pacman.image, pacman.rect)
    if blinky.ghost: screen.blit (blinky.image, blinky.rect)
    if  pinky.ghost: screen.blit ( pinky.image, pinky.rect)
    if   inky.ghost: screen.blit (  inky.image, inky.rect)
    if  clyde.ghost: screen.blit ( clyde.image, clyde.rect)
    screen.blit (ready_text,(264,396))
    clock.tick(clktcks)
    pygame.display.flip()
    while pygame.mixer.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.stop()
                game_over = True
                pygame.quit()
                sys.exit()

#secuencia de muerte de pacman
def dead_seq():
    pygame.mixer.stop()
    for n in range (0,20):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.stop()
                game_over = True
                pygame.quit()
                sys.exit()
                
            #cambia el frame de cada sprite por interrupcion
            elif event.type == USEREVENT + 1:
                blinky.frame += 1
                pinky.frame  += 1
                inky.frame   += 1
                clyde.frame  += 1
                
        screen.blit(fondo, (0, 0))
        screen.blit(pacman.image, pacman.rect)
        if blinky.ghost:
            blinky.update_state()
            screen.blit (blinky.image, blinky.rect)
        if  pinky.ghost:
            pinky.update_state()
            screen.blit ( pinky.image, pinky.rect)
        if   inky.ghost:
            inky.update_state()
            screen.blit (  inky.image, inky.rect)
        if  clyde.ghost:
            clyde.update_state()
            screen.blit ( clyde.image, clyde.rect)
        pygame.display.flip()
        clock.tick(clktcks)

    life_lost.play()
    for frame in range(0, 13):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    game_over = True
                    pygame.quit()
                    sys.exit()
        pacman.frame = frame
        screen.blit(fondo, (0, 0))
        pacman.dead_clip()
        screen.blit(pacman.image, pacman.rect)
        pygame.display.flip()
        pygame.time.wait(100)
        
    if pacman.lives > 0:
        pacman.nextDirection = ''
        pacman.direction = 'stand'
        position = (336, 564)
        pacman.rect.center = position
        pacman.posX = position[0]
        pacman.posY = position[1]
        pacman.frame = 2
        pacman.vel = pacman.nVel 
        pacman.clip(pacman.left_states)

        position = (336, 276)
        blinky.rect.center = position
        blinky.posX = position[0]
        blinky.posY = position[1]
        blinky.rect.center = position
        blinky.clip(blinky.left_states)

        pinky.rect.center = position
        pinky.posX = position[0]
        pinky.posY = position[1]
        pinky.rect.center = position
        pinky.clip(pinky.left_states)

        inky.rect.center = position
        inky.posX = position[0]
        inky.posY = position[1]
        inky.rect.center = position
        inky.clip(inky.left_states)

        clyde.rect.center = position
        clyde.posX = position[0]
        clyde.posY = position[1]
        clyde.rect.center = position
        clyde.clip(clyde.left_states)

        blinky.direction = 'left'
        pinky.direction  = 'left'
        inky.direction   = 'left'
        clyde.direction  = 'left'
        blinky.ghost = False
        pinky.ghost  = False
        inky.ghost   = False
        clyde.ghost  = False

class blinkSprite(pygame.sprite.Sprite):
    def __init__(self, sprRect, general_sprites):
        self.sheet = general_sprites
        self.sheet.set_clip(pygame.Rect(sprRect))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.frame = 0
        
#maze array
# b1(01):way            b2(02):pill             b3(04):powerpill             b4(08):slowway
# b5(16):intersection   b6(32):specialintersec  b7(64):fruit
myArray = [
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  
    [0,  3,  3,  3,  3,  3, 19,  3,  3,  3,  3,  3,  3,  0,  0,  3,  3,  3,  3,  3,  3, 19,  3,  3,  3,  3,  3,  0],  
    [0,  3,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  3,  0],  
    [0,  5,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  5,  0],  
    [0,  3,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  3,  0],  
    [0, 19,  3,  3,  3,  3, 19,  3,  3, 19,  3,  3, 19,  3,  3, 19,  3,  3, 19,  3,  3, 19,  3,  3,  3,  3, 19,  0],  
    [0,  3,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  3,  0],  
    [0,  3,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  3,  0],  
    [0,  3,  3,  3,  3,  3, 19,  0,  0,  3,  3,  3,  3,  0,  0,  3,  3,  3,  3,  0,  0, 19,  3,  3,  3,  3,  3,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  1,  0,  0,  1,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  1,  0,  0,  1,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  1,  1, 49,  1,  1, 49,  1,  1,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [9,  9,  9,  9,  9,  9, 19,  1,  1, 17,  0,  0,  0,  0,  0,  0,  0,  0, 17,  1,  1, 19,  9,  9,  9,  9,  9,  9],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0, 17,  1,  1,  1,  1,  1,  1,  1,  1, 17,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  0,  0,  0,  0,  0,  3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0],  
    [0,  3,  3,  3,  3,  3, 19,  3,  3, 19,  3,  3,  3,  0,  0,  3,  3,  3, 19,  3,  3, 19,  3,  3,  3,  3,  3,  0],  
    [0,  3,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  3,  0],  
    [0,  3,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  3,  0],  
    [0,  5,  3,  3,  0,  0, 19,  3,  3, 19,  3,  3, 51,  1,  1, 51,  3,  3, 19,  3,  3, 19,  0,  0,  3,  3,  5,  0],  
    [0,  0,  0,  3,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  3,  0,  0,  0],  
    [0,  0,  0,  3,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  3,  0,  0,  0],  
    [0,  3,  3, 19,  3,  3,  3,  0,  0,  3,  3,  3,  3,  0,  0,  3,  3,  3,  3,  0,  0,  3,  3,  3, 19,  3,  3,  0],  
    [0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0],  
    [0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0],  
    [0,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3, 19,  3,  3, 19,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  0],  
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

screen = pygame.display.set_mode((1032, 744))
font = pygame.font.SysFont('arial', 30)
pygame.display.set_caption('pacman')

#carga imagenes del laberinto
Sprites = pygame.image.load('imagenes\General-Sprites.png')
fondo = Sprites.subsurface(0, 0, 672, 744)
ready_text = Sprites.subsurface(1656, 432, 144, 48)
game_over_text = Sprites.subsurface(1656, 384, 240, 48)
life = Sprites.subsurface(1752, 48, 48, 48)
high_score_text = Sprites.subsurface(1659, 490, 237, 30)

#carga sprites
pacman = pacPlayer.Spr((336, 564), Sprites)
blinky = ghostPlayer.Spr((336, 276),'blinky', Sprites)
pinky  = ghostPlayer.Spr((336, 276),'pinky', Sprites)
inky   = ghostPlayer.Spr((336, 276),'inky', Sprites)
clyde  = ghostPlayer.Spr((336, 276),'clyde', Sprites)
num    = renderNumber.Txt(Sprites)
hinum  = renderNumber.Txt(Sprites)
player2up = Sprites.subsurface(1827, 454, 72, 30)
player1up = blinkSprite((1827, 427, 72, 30), Sprites)
player2up = blinkSprite((1827, 454, 72, 30), Sprites)
powerpill = blinkSprite((1656, 528, 48, 48), Sprites)
fruit     = Sprites.subsurface(1656, 576, 48, 48)

#init game vars
timer0       = 0.0
timer_mode   = 0.0
timer_frig   = 0.0
game_over    = False
score        = int(0)
hiscore      = int(0)
level        = int(1)
pacman.lives = int(3)
ghost_mode   = 'scatter'
ppill_lst    = []
clktcks      = 25

#ubicacion de powerpills
for j in range(0,len(myArray)):
    for i in range(0,len(myArray[0])):
        if myArray[j][i] & 4 == 4: ppill_lst.append((i*24-12,j*24-12))

#carga sonidos
pygame.mixer.init()
intro          = pygame.mixer.Sound('sounds fx\intro.wav')
ambient        = pygame.mixer.Sound('sounds fx\siren medium 3.wav')
wakaA          = pygame.mixer.Sound('sounds fx\munch A.wav')
wakaB          = pygame.mixer.Sound('sounds fx\munch B.wav')
life_lost      = pygame.mixer.Sound('sounds fx\death 1.wav')
ppill_snd      = pygame.mixer.Sound('sounds fx\power_pellet_eaten.wav')
ppill_snd_loop = pygame.mixer.Sound('sounds fx\large pellet loop.wav')
wak = True

clock = pygame.time.Clock()

#interrupcion cada 100ms para cambiar el frame de cada sprite
pygame.time.set_timer(USEREVENT + 1, 100)

intro_seq()

pygame.time.wait(100)
ambient.play(-1)

#main loop
timer0 = pygame.time.get_ticks()
timer_mode = pygame.time.get_ticks()

while game_over == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit()
                
        #cambia el frame de cada sprite por interrupcion
        elif event.type == USEREVENT + 1:
            pacman.frame     += 1
            blinky.frame     += 1
            pinky.frame      += 1
            inky.frame       += 1
            clyde.frame      += 1
            player1up.frame  += 1
            powerpill.frame  += 1
            if player1up.frame > 7: player1up.frame = 0
            if powerpill.frame > 5: powerpill.frame = 0
            
    #cuando aparece cada fantasma            
    clk = pygame.time.get_ticks()
    if clk-timer0 > 0      : blinky.ghost = True
    if clk-timer0 > 5000   : pinky.ghost  = True
    if clk-timer0 > 10000  : inky.ghost   = True
    if clk-timer0 > 15000  : clyde.ghost  = True

    
    if ghost_mode != 'frightened':
        prev_mode = ghost_mode
        if             (clk-timer_mode) <=   7000: ghost_mode  = 'scatter'
        elif   7000  < (clk-timer_mode) <=  27000: ghost_mode  = 'chase'
        elif  27000  < (clk-timer_mode) <=  34000: ghost_mode  = 'scatter'
        elif  34000  < (clk-timer_mode) <=  54000: ghost_mode  = 'chase'
        elif  54000  < (clk-timer_mode) <=  59000: ghost_mode  = 'scatter'
        elif  59000  < (clk-timer_mode) <=  79000: ghost_mode  = 'chase'
        elif  79000  < (clk-timer_mode) <=  84000: ghost_mode  = 'scatter'
        elif  84000  < (clk-timer_mode)          : ghost_mode  = 'chase'
        if prev_mode != ghost_mode:
            if blinky.ghost : blinky.swapMode = True
            if pinky.ghost  : pinky.swapMode  = True
            if inky.ghost   : inky.swapMode   = True
            if clyde.ghost  : clyde.swapMode  = True
    else:
        if timer_frig != 0 and pygame.time.get_ticks()-timer_frig > 10000:
            ghost_mode = prev_mode 
            ppill_snd_loop.stop()
            ambient.play(-1)
            timer_frig = 0

    #calcula la posicion de cada sprite
    pacman.handle_event(event, myArray)
    game_over = pacman.game_over
    if blinky.ghost: blinky.handle_event (event, myArray, ghostIA('blinky', ghost_mode, pacman, blinky, clyde), ghost_mode)
    if  pinky.ghost:  pinky.handle_event (event, myArray, ghostIA('pinky' , ghost_mode, pacman, blinky, clyde), ghost_mode)
    if   inky.ghost:   inky.handle_event (event, myArray, ghostIA('inky'  , ghost_mode, pacman, blinky, clyde), ghost_mode)
    if  clyde.ghost:  clyde.handle_event (event, myArray, ghostIA('clyde' , ghost_mode, pacman, blinky, clyde), ghost_mode)

    
    #verifica si come
    if pacman.eaten != 'nothing':
        if pacman.eaten == 'pill':
            score += 10
            pygame.draw.rect(fondo,(0,0,0),(pacman.pillCenter[0]-3,pacman.pillCenter[1]-3,6,6))
            if wak:
                wak = False
                wakaA.play()
            else:
                wak = True
                wakaB.play()
        if pacman.eaten == 'powerpill':
            score += 50
            ppill_snd.play()
            for n in range(0,len(ppill_lst)):
                if (ppill_lst[n][0]+24,ppill_lst[n][1]+24) == pacman.pillCenter:
                    ghost_mode  = 'frightened'
                    if blinky.ghost : blinky.swapMode = True
                    if pinky.ghost  : pinky.swapMode  = True
                    if inky.ghost   : inky.swapMode   = True
                    if clyde.ghost  : clyde.swapMode  = True
                    pygame.mixer.stop()
                    ppill_snd_loop.play(-1)
                    timer_frig = pygame.time.get_ticks()
                    del ppill_lst[n]
                    break
                
        pacman.eaten = 'nothing'
        pacman.pillCenter = (0,0)
        if pacman.pills>=244: game_over = True
        
    #verifica si los fantasmas atrapan a pacman
    if ghost_mode != 'frightened':
        if     (((blinky.posX-12) <= pacman.posX <= (blinky.posX+12)) and ((blinky.posY-12) <= pacman.posY <= (blinky.posY+12)) and blinky.ghost)\
            or ((( pinky.posX-12) <= pacman.posX <= ( pinky.posX+12)) and (( pinky.posY-12) <= pacman.posY <= ( pinky.posY+12)) and pinky.ghost)\
            or (((  inky.posX-12) <= pacman.posX <= (  inky.posX+12)) and ((  inky.posY-12) <= pacman.posY <= (  inky.posY+12)) and inky.ghost)\
            or ((( clyde.posX-12) <= pacman.posX <= ( clyde.posX+12)) and (( clyde.posY-12) <= pacman.posY <= ( clyde.posY+12)) and clyde.ghost):
            pacman.lives-=1
            dead_seq()
            if ghost_mode == 'frightened':
                ghost_mode = prev_mode
            timer_frig = 0
            timer0 = pygame.time.get_ticks()
            if pacman.lives > 0: ambient.play(-1)

    #verifica si se acabaron las vidas
    if pacman.lives <= 0:
        game_over = True

    #calcula el puntaje
    num.handle_event   (event, score,(852,159))
    if score == 0: hinum.handle_event (event, hiscore, (852,363))
    if hiscore < score:
        hiscore = score
        hinum.handle_event (event, hiscore, (852,363))
        
    #imprime todos los sprites en pantalla
    screen.blit(fondo, (0, 0))
    if powerpill.frame <3:
        for n in range(0,len(ppill_lst)):
            screen.blit (powerpill.image, (ppill_lst[n]))
            
    screen.blit(pacman.image, pacman.rect)
    if blinky.ghost: screen.blit (blinky.image, blinky.rect)
    if  pinky.ghost: screen.blit ( pinky.image, pinky.rect)
    if   inky.ghost: screen.blit (  inky.image, inky.rect)
    if  clyde.ghost: screen.blit ( clyde.image, clyde.rect)
    screen.fill((0,0,0),(672,0,1032,744))
    screen.blit (num.image, num.rect)
    if hiscore>0: screen.blit (hinum.image, hinum.rect)
    
    #text_pacX = font.render('x: '+str(clk), True, (255,255,255))
    #text_pacX = font.render('Lives: '+str(pacman.lives), True, (255,255,255))
    #screen.blit(text_pacX, (684, 12))
    
    #text_pacY = font.render('Score: '+str(clk-timer_mode), True, (255,255,255))
    #screen.blit(text_pacY, (684, 42))

    if player1up.frame <4: screen.blit (player1up.image, (820,111))

    screen.blit (high_score_text,(735,315))
    screen.blit (fruit,(828,666))
    #screen.blit (player2up,(678+100 , 48))
    nx =  855 - (pacman.lives-1) * 24
    for n in range (0, pacman.lives-1):
        screen.blit (life,(nx + 48 * n, 192))
        
    pygame.display.flip()
    clock.tick(clktcks)

#game over sequence
pygame.mixer.stop()
#ppill_snd_loop.stop()
while True:
    for event in pygame.event.get():
        #if event.type == pygame.KEYDOWN:
            #if event.key != '':
                #pygame.quit()
                #sys.exit()
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        #cambia el frame de cada sprite por interrupcion
        elif event.type == USEREVENT + 1:
            blinky.frame += 1
            pinky.frame  += 1
            inky.frame   += 1
            clyde.frame  += 1
            player1up.frame  += 1
            
    screen.blit(fondo, (0, 0))
    screen.blit(pacman.image, pacman.rect)
    
    if blinky.ghost:
        blinky.handle_event (event,myArray,(pacman.posX,pacman.posY),'chase')
        screen.blit (blinky.image, blinky.rect)
    if  pinky.ghost:
        pinky.handle_event (event,myArray,(60 ,-60),'chase')
        screen.blit ( pinky.image, pinky.rect)
    if   inky.ghost:
        inky.handle_event (event,myArray,(660,780),'chase')
        screen.blit (  inky.image, inky.rect)
    if  clyde.ghost:
        clyde.handle_event (event,myArray,(12 ,780),'chase')
        screen.blit ( clyde.image, clyde.rect)
    screen.blit (game_over_text,(216,396))
    pygame.display.flip()
    clock.tick(clktcks)
