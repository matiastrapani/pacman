def ghostIA(ghost, mode, pacman, blinky, clyde):
    target = (0,0)
    if   ghost == 'blinky' and mode=='scatter': target = (612,-60)
    elif ghost == 'pinky'  and mode=='scatter': target = (60 ,-60)
    elif ghost == 'inky'   and mode=='scatter': target = (660,780)
    elif ghost == 'clyde'  and mode=='scatter': target = (12 ,780)

    elif ghost == 'blinky' and mode=='chase':   target = (pacman.posX, pacman.posY)
    
    elif ghost == 'pinky'  and mode=='chase':
        if   pacman.direction == 'left':  target = (pacman.posX-96, pacman.posY)
        elif pacman.direction == 'right': target = (pacman.posX+96, pacman.posY)
        elif pacman.direction == 'up':    target = (pacman.posX-96, pacman.posY-96)
        elif pacman.direction == 'down':  target = (pacman.posX, pacman.posY+96)
        else: target = (pacman.posX, pacman.posY)
        
    elif ghost == 'inky'   and mode=='chase':
        if   pacman.direction == 'left':  target = (pacman.posX-48, pacman.posY)
        elif pacman.direction == 'right': target = (pacman.posX+48, pacman.posY)
        elif pacman.direction == 'up':    target = (pacman.posX-48, pacman.posY-48)
        elif pacman.direction == 'down':  target = (pacman.posX, pacman.posY+48)
        else: target = (pacman.posX, pacman.posY)
        target = (2*target[0]-blinky.posX , 2*target[1]-blinky.posY)

    elif ghost == 'clyde'   and mode=='chase':
        target = (12 ,780)
        dist =(pacman.posX-clyde.posX)**2+(pacman.posY-clyde.posY)**2
        if dist > 36864: target = (pacman.posX, pacman.posY)
    
    return (int(target[0]),int(target[1]))
