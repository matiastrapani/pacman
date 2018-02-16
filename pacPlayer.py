import pygame
class Spr(pygame.sprite.Sprite):
    cornering_init = 0
    game_over = False
    def __init__(self, position, general_sprites):
        self.sheet = general_sprites
        self.sheet.set_clip(pygame.Rect(1464, 0, 45, 45))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])
        self.frame = 0
        self.left_states  = { 0: (1368,  48, 45, 45), 1: (1416,  48, 45, 45), 2: (1464, 0, 45, 45), 3: (1416,  48, 45, 45) }
        self.right_states = { 0: (1368,   0, 45, 45), 1: (1416,   0, 45, 45), 2: (1464, 0, 45, 45), 3: (1416,   0, 45, 45) }
        self.up_states    = { 0: (1368,  96, 45, 45), 1: (1416,  96, 45, 45), 2: (1464, 0, 45, 45), 3: (1416,  96, 45, 45) }
        self.down_states  = { 0: (1368, 144, 45, 45), 1: (1416, 144, 45, 45), 2: (1464, 0, 45, 45), 3: (1416, 144, 45, 45) }
        self.dead_seq     = { 0: (1464,   0, 45, 45), 1: (1512,   0, 45, 45), 2: (1560, 0, 45, 45), 3: (1608, 0, 45, 45), 4: (1656, 0, 45, 45), 5: (1704, 0, 45, 45), 6: (1752, 0, 45, 45), 7: (1800, 0, 45, 45), 8: (1848, 0, 45, 45), 9: (1896, 0, 45, 45), 10: (1944, 0, 45, 45), 11: (1992, 1, 45, 45), 12: (1992, 48, 45, 45)}
        self.direction = 'stand'
        self.posX = position[0]
        self.posY = position[1]
        self.sVel = 7.0
        self.nVel = 8.0
        self.vel  = self.nVel
        self.nextDirection = ''
        self.pills = 0
        self.pillCenter = (0,0)
        self.eaten = 'nothing'
        self.lives = 0
        self.n = 0
        self.cornering_timer = []
        
    def get_frame(self, frame_set):
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    
    def dead_clip(self):
        self.clip(self.dead_seq)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
    
    def update(self, Maze):
        x0 = self.posX
        y0 = self.posY
        
        if self.nextDirection!='':
            if self.direction == 'stand'\
                    or (self.direction=='right' and self.nextDirection=='left')\
                    or (self.direction=='left' and self.nextDirection=='right')\
                    or (self.direction=='up' and self.nextDirection=='down')\
                    or (self.direction=='down' and self.nextDirection=='up'):
                self.direction=self.nextDirection
                self.nextDirection=''
     
        if self.direction == 'stand':
            self.frame = 2
            self.clip(self.left_states)

        elif self.direction == 'left':
            self.clip(self.left_states)
            self.posX -= self.vel
            
        elif self.direction == 'right':
            self.clip(self.right_states)
            self.posX += self.vel

        elif self.direction == 'up':
            self.clip(self.up_states)
            self.posY -= self.vel
            
        elif self.direction == 'down':
            self.clip(self.down_states)
            self.posY += self.vel
        
        ic0 = int(x0/24)
        jc0 = int(y0/24)
        xc0 = ((ic0*24)+12)
        yc0 = ((jc0*24)+12)
        x1  = self.posX
        y1  = self.posY
        ic1 = int(x1/24)
        jc1 = int(y1/24)
        xc1 = ((ic1*24)+12)
        yc1 = ((jc1*24)+12)

        #ahora se detecta si tendria que haber cambiado la direccion o haberse detenido
        #entonces si se movio
        isInSameCell = True
        if self.direction != 'stand' and (x1!=x0 or y1!=y0):
            if  x0>=xc0>x1 or x0<=xc0<x1:
                xc=xc0
                ic=ic0
                isInSameCell = False
            elif x0>=xc1>x1 or x0<xc1<x1:
                xc=xc1
                ic=ic1
                isInSameCell = False
            else:
                xc=xc0
                ic=ic0
            if  y0>=yc0>y1 or y0<=yc0<y1:
                yc=yc0
                jc=jc0
                isInSameCell = False
            elif y0>=yc1>y1 or y0<=yc1<y1:
                yc=yc1
                jc=jc1
                isInSameCell = False
            else:
                yc=yc0
                jc=jc0

            #y queria cambiar de direccion y hubo cambio de celda
            if self.nextDirection != '' and not(isInSameCell): 
                #hacia una direccion vertical
                cornering_timer = pygame.time.get_ticks()
                cornering_timer -= self.cornering_init
                delta = 0
                if self.nextDirection == 'up' or self.nextDirection == 'down':
                    #detecta si las celdas en vertical estan en el laberinto
                    if 0<=ic<=27:
                        if self.nextDirection=='up'   and (Maze[jc-1][ic] & 1)==1:
                            delta = abs(x1-xc) 
                            self.posY -= delta
                            self.clip(self.up_states)
                            self.posX = xc
                            self.direction = self.nextDirection
                            self.nextDirection = ''
                            if cornering_timer < 80: self.posY -= 8-delta
                        if self.nextDirection == 'down' and (Maze[jc+1][ic] & 1)==1:
                            delta = abs(x1-xc)
                            self.posY += delta
                            self.clip(self.down_states)
                            self.posX=xc
                            self.direction = self.nextDirection
                            self.nextDirection = ''
                            if cornering_timer < 80: self.posY += 8-delta
                        
                #o hacia una direccion horizontal
                elif self.nextDirection=='right' or self.nextDirection=='left':

                    #aca hay un error si esta en el tunel
                    if 0<=jc<=30:
                        if self.nextDirection == 'right' and (Maze[jc][ic+1] & 1)==1:
                            delta = abs(y1-yc)
                            self.posX += delta
                            self.clip(self.right_states)
                            self.posY = yc
                            self.direction = self.nextDirection
                            self.nextDirection = ''
                            if cornering_timer < 80: self.posX += 8-delta
                        if self.nextDirection == 'left'  and (Maze[jc][ic-1] & 1)==1:
                            delta = abs(y1-yc)
                            self.posX -= delta
                            self.clip(self.left_states)
                            self.posY = yc
                            self.direction = self.nextDirection
                            self.nextDirection  = ''
                            if cornering_timer < 80: self.posX -= 8-delta
                #if cornering_timer < 80: print 8-delta
                            
            #detecta la colision con una pared
            if 1<=ic<=26 and 1<=jc<=29 and not(isInSameCell):
                if self.direction == 'left'  and (Maze[jc][ic-1] & 1)!=1: self.posX=xc
                if self.direction == 'right' and (Maze[jc][ic+1] & 1)!=1: self.posX=xc
                if self.direction == 'up'    and (Maze[jc-1][ic] & 1)!=1: self.posY=yc
                if self.direction == 'down'  and (Maze[jc+1][ic] & 1)!=1: self.posY=yc

                #si hay pill comerla y aumentar el score
                if (Maze[jc][ic] & 2)==2:
                    self.vel = self.sVel
                    self.pills+=1
                    Maze[jc][ic] = Maze[jc][ic] & 125
                    self.pillCenter = (xc,yc)
                    self.eaten = 'pill'
                elif (Maze[jc][ic] & 4)==4:
                    self.vel = self.sVel
                    self.pills+=1
                    Maze[jc][ic] = Maze[jc][ic] & 123
                    self.pillCenter = (xc,yc)
                    self.eaten = 'powerpill'
                else:
                    self.vel = self.nVel

        

        self.rect.center = (self.posX, self.posY)
        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_event(self, event, Maze):
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            sys.exit()
            
        if self.posX > 694 : self.posX -= 717
        if self.posX < -23 : self.posX += 717
        if self.posY > 767 : self.posY -= 790
        if self.posY < -23 : self.posY += 790
        self.update(Maze)
        
        # Creo una lista vacia 
        pressed_key_text = []

        # Obtengo las teclas que el usuario presiona
        pressed_keys = pygame.key.get_pressed()
        # recorro la lista con un loop for 
        for key_constant, pressed in enumerate(pressed_keys):
    
            # Si la tecla esta presionada 
            if pressed:
                # Obtengo el nombre de la tecla presionada
                key_name = pygame.key.name(key_constant)
                if key_name == 'left'  or key_name == '[4]':
                    self.nextDirection='left'
                    self.cornering_init = pygame.time.get_ticks()
                if key_name == 'right' or key_name == '[6]':
                    self.nextDirection='right'
                    self.cornering_init = pygame.time.get_ticks()
                if key_name == 'up'    or key_name == '[8]':
                    self.nextDirection='up'
                    self.cornering_init = pygame.time.get_ticks()
                if key_name == 'down'  or key_name == '[2]':
                    self.nextDirection='down'
                    self.cornering_init = pygame.time.get_ticks()
                if key_name == 'escape':
                    self.game_over = True

                    
                if self.nextDirection == self.direction:
                    self.nextDirection = ''
