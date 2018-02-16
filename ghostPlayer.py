import pygame
class Spr(pygame.sprite.Sprite):
    def __init__(self, position, name, general_sprites):
        self.sheet = general_sprites
        self.name  = name
        nv=0
        self.nVel = 7.5
        self.sVel = 4.0
        if name=='blinky':
            nv = 0
            self.vel = self.nVel
        elif name=='pinky':
            nv = 48
            self.vel = self.nVel
        elif name=='inky':
            nv = 96
            self.vel = self.nVel
        elif name=='clyde':
            nv = 144
            self.vel = self.nVel
        self.sheet.set_clip(pygame.Rect(1464, 192 + nv, 48, 48))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])
        self.frame = 0
        self.direction = 'left'
        self.left_states  = { 0: (1464, 192 + nv, 48, 48), 1: (1512, 192 + nv, 48, 48) }
        self.right_states = { 0: (1368, 192 + nv, 48, 48), 1: (1416, 192 + nv, 48, 48) }
        self.up_states    = { 0: (1560, 192 + nv, 48, 48), 1: (1608, 192 + nv, 48, 48) }
        self.down_states  = { 0: (1656, 192 + nv, 48, 48), 1: (1704, 192 + nv, 48, 48) }
        self.frig_states  = { 0: (1752, 288, 48, 48), 1: (1800, 288, 48, 48) }
        self.trans_states = { 0: (1848, 288, 48, 48), 1: (1896, 288, 48, 48) }
        self.posX = position[0]
        self.posY = position[1]
        self.ghost = False
        self.swapMode = False
        
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
    
    def update(self, Maze, Target, ghost_mode):
        x0=self.posX
        y0=self.posY
        if ghost_mode=='frightened': self.vel = self.sVel
        else: self.vel = self.nVel 
        if   self.direction == 'left':
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

        ic0=int(x0/24)
        jc0=int(y0/24)
        xc0=((ic0*24)+12)
        yc0=((jc0*24)+12)
        x1=self.posX
        y1=self.posY
        ic1=int(x1/24)
        jc1=int(y1/24)
        xc1=((ic1*24)+12)
        yc1=((jc1*24)+12)
    
        isInSameCell = True
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

        #cambia direccion en cambio de ghost mode
        if self.swapMode and not(isInSameCell):
            self.swapMode = False
            self.posX = xc
            self.posY = yc
            if   self.direction == 'left':
                self.direction = 'right'
                self.clip(self.right_states)
                dx = abs(x1-xc)
                self.posX += dx
                
            elif self.direction == 'right':
                self.direction = 'left'
                self.clip(self.left_states)
                dx = abs(x1-xc)
                self.posX -= dx
                
            elif self.direction == 'up':
                self.direction = 'down'
                self.clip(self.down_states)
                dy = abs(y1-yc)
                self.posY += dy
                
            elif self.direction == 'down':
                self.direction = 'up'
                self.clip(self.up_states)
                dy = abs(y1-yc)
                self.posY += dy
                
            x1=self.posX
            y1=self.posY
            ic1=int(x1/24)
            jc1=int(y1/24)
            xc1=((ic1*24)+12)
            yc1=((jc1*24)+12)
            isInSameCell = True

        #decide en interseccion
        if 1<=ic<=26 and 1<=jc<=29:
            if (Maze[jc][ic] & 16)==16 and not(isInSameCell):
                dx = abs(xc-Target[0])
                dy = abs(yc-Target[1])
                dir = ['up','left','down','right']
                if   dx > dy:
                    ind = [0,3,1,2]
                elif dx < dy:
                    ind = [1,2,0,3]
                if  dx == dy:
                    #si el target esta arriba a la izquierda
                    if xc-Target[0]>0 and yc-Target[1]>0: dir = ['up','left','down','right']
                    #si el target esta abajo a la derecha
                    if xc-Target[0]<0 and yc-Target[1]<0: dir = ['down','right','up','left']
                    #si el target esta arriba a la derecha
                    if xc-Target[0]<0 and yc-Target[1]>0: dir = ['up','right','left','down']
                    #si el target esta abajo a la izquierda
                    if xc-Target[0]>0 and yc-Target[1]<0: dir = ['left','down','up','right']
                else:
                    if abs(xc-1-Target[0]) <= abs(xc+1-Target[0]):
                        dir[ind[0]] = 'left'
                        dir[ind[1]] = 'right'
                    else:
                        dir[ind[1]] = 'left'
                        dir[ind[0]] = 'right'
                    if abs(yc-1-Target[1]) <= abs(yc+1-Target[1]):
                        dir[ind[2]] = 'up'
                        dir[ind[3]] = 'down'
                    else:
                        dir[ind[3]] = 'up'
                        dir[ind[2]] = 'down'
                n=int(0)
                priorDir = False
                while priorDir == False:
                    if dir[n]=='up' and (Maze[jc-1][ic] & 1)==1 and self.direction != 'down' and (Maze[jc][ic] & 32)!=32:
                        self.direction = 'up'
                        self.clip(self.up_states)
                        self.posX = xc
                        self.posY -= abs(x1-xc)
                        priorDir = True
                    if dir[n]=='down' and (Maze[jc+1][ic] & 1)==1 and self.direction != 'up':
                        self.direction = 'down'
                        self.clip(self.down_states)
                        self.posX = xc
                        self.posY += abs(x1-xc)
                        priorDir = True
                    if dir[n]=='left' and (Maze[jc][ic-1] & 1)==1 and self.direction != 'right':
                        self.direction = 'left'
                        self.clip(self.left_states)
                        self.posY = yc
                        self.posX -= abs(y1-yc)
                        priorDir = True
                    if dir[n]=='right' and (Maze[jc][ic+1] & 1)==1 and self.direction != 'left':
                        self.direction = 'right'
                        self.clip(self.right_states)
                        self.posY = yc
                        self.posX += abs(y1-yc)
                        priorDir = True
                    n+=1

            #colision con paredes
            if not(isInSameCell):  
                if (self.direction=='left'  and (Maze[jc][ic-1] & 1)!=1) or (self.direction=='right' and (Maze[jc][ic+1] & 1)!=1):
                    self.posX = xc
                    if (Maze[jc-1][ic] & 1)==1:
                        self.direction = 'up'
                        self.clip(self.up_states)
                        self.posY -= abs(x1-xc)
                    elif (Maze[jc+1][ic] & 1)==1:
                        self.direction = 'down'
                        self.clip(self.down_states)
                        self.posY += abs(x1-xc)
                    else:
                        if self.direction == 'left':
                            self.direction = 'right'
                            self.clip(self.right_states)
                            self.posX+=abs(y1-yc)
                        else:
                            self.direction = 'left'
                            self.clip(self.left_states)
                            self.posX-=abs(y1-yc)

                if (self.direction=='up'    and (Maze[jc-1][ic] & 1)!=1) or (self.direction=='down' and (Maze[jc+1][ic] & 1)!=1):
                    self.posY = yc
                    if (Maze[jc][ic-1] & 1)==1:
                        self.direction = 'left'
                        self.clip(self.left_states)
                        self.posX -= abs(y1-yc)
                    elif (Maze[jc][ic+1] & 1)==1:
                        self.direction = 'right'
                        self.clip(self.right_states)
                        self.posX += abs(y1-yc)
                    else:
                        if self.direction == 'up':
                            self.direction = 'down'
                            self.clip(self.down_states)
                            self.posY += abs(x1-xc)
                        else:
                            self.direction = 'up'
                            self.clip(self.up_states)
                            self.posY -= abs(x1-xc)
            #slowway
            if (self.direction=='left'  and (Maze[jc][ic-1] & 8)==8):
                self.posX = x0
                self.posX -= self.sVel
            if (self.direction=='right' and (Maze[jc][ic+1] & 8)==8):
                self.posX = x0
                self.posX += self.sVel
            if (self.direction=='up'    and (Maze[jc-1][ic] & 8)==8):
                self.posY = y0
                self.posY -= self.sVel
            if (self.direction=='down'  and (Maze[jc+1][ic] & 8)==8):
                self.posY = y0
                self.posY += self.sVel

        else:
            #slowway fuera del laberinto
            if self.direction=='left':
                self.posX = x0
                self.posX -= self.sVel
            if self.direction=='right':
                self.posX = x0
                self.posX += self.sVel
            if self.direction=='up':
                self.posY = y0
                self.posY -= self.sVel
            if self.direction=='down':
                self.posY = y0
                self.posY += self.sVel
        if ghost_mode == 'frightened': self.clip(self.frig_states)
        self.rect.center = (self.posX, self.posY)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
    def update_state(self):
        if self.direction == 'left':    self.clip(self.left_states)
        if self.direction == 'right':   self.clip(self.right_states)
        if self.direction == 'up':      self.clip(self.up_states)
        if self.direction == 'down':    self.clip(self.down_states)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
    
    def handle_event(self, event, Maze, Target, ghost_mode):
        if event.type == pygame.QUIT:
            game_over = True

        if self.posX>694 : self.posX-=717
        if self.posX<-23 : self.posX+=717
        if self.posY>767 : self.posY-=790
        if self.posY<-23 : self.posY+=790
        self.update(Maze, Target, ghost_mode)
