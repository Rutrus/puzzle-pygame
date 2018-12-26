import sys, pygame, time, random, os
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

x = BOARD_X_AXIS = 4
y = BOARD_y_AXIS = 4
sq_x = sq_y = None # Initialized depends on image()

freeSquare = (BOARD_X_AXIS-1,BOARD_y_AXIS-1)

def setImage():
    from PIL import Image
    from io import BytesIO
    global sq_x, sq_y

    location = os.path.abspath("examples/slideNumbers/img")+"/"
    _,_,img = next(os.walk(location))
    wallpaper = random.choice(img)

    image = [ [[] for i in range(x)] for j in range(y)]
    im = Image.open(location+wallpaper).convert("RGB")
    im.thumbnail((1000,im.size[1]*1000//im.size[0]),Image.ANTIALIAS)
    sq_x, sq_y =  im.size[0]//x, im.size[1]//y
    for i in range(x):
        for j in range(y):
            imCrop = im.crop((sq_x*i,sq_y*j,sq_x*(i+1),sq_y*(j+1)))
            byte_io = BytesIO()
            imCrop.save(byte_io,"PNG")
            image[i][j] = pygame.image.fromstring(imCrop.tobytes(),imCrop.size,imCrop.mode)
    return image

def getColor(x,y):
    if (x+y)%2: return WHITE
    else: return GREY

def createBoard():
    global cuadros
    global numbers

    numbers = [ [[] for i in range(x)] for j in range(y)]
    cuadros = [ [[] for i in range(x)] for j in range(y)]

    pygame.init()
    for i in range(x):
        for j in range(y):
            cuadros[i][j] = pygame.Rect(sq_x*i,sq_y*j,sq_x,sq_y)
            if (i,j) == freeSquare:
                numbers[i][j] = 0
            numbers[i][j] = y*j+i+1
            DISPLAY.blit(image[i][j],cuadros[i][j])
            pygame.display.flip()

def move(key):
    move = freeSquare
    if key == K_LEFT and freeSquare[0] < x-1:
        print("Key: left")
        move = (move[0]+1,move[1])
    elif key == K_RIGHT and freeSquare[0]:
        print("Key: right")
        move = (move[0]-1,move[1])
    elif key == K_UP and freeSquare[1] < y-1:
        print("Key: up")
        move = (move[0],move[1]+1)
    elif key == K_DOWN and freeSquare[1]:
        print("Key: down")
        move = (move[0],move[1]-1)
    return move

def change(from_, to_ ):
    global cuadros
    # Because pieces move in reverse way
    # Free space is from_ -> to_
    # Piece is to_ -> from_
    x0,y0 = to_
    x1,y1 = from_

    cuadro0 = cuadros[x0][y0]
    cuadro1 = cuadros[x1][y1]

    rectCuadro = cuadro0.copy()
    if cuadro0.centerx != cuadro1.centerx:
        a = cuadro0.centerx
        b = cuadro1.centerx
        exp = 1
        if a > b: exp = -1
        for i in range(a,b,8*exp):
            rectCuadro.centerx = i
            pygame.draw.rect(DISPLAY,WHITE,cuadro0)
            redraw(x0,y0,rectCuadro)
            #redraw(x1,y1,rectCuadro)
            
    else:
        a = cuadro0.centery
        b = cuadro1.centery
        exp = 1
        if a > b: exp = -1
        for i in range(a,b,8*exp):
            rectCuadro.centery = i
            pygame.draw.rect(DISPLAY,WHITE,cuadro0)
            redraw(x0,y0,rectCuadro)

    numbers[x0][y0], numbers[x1][y1] =  numbers[x1][y1], numbers[x0][y0]
    image[x0][y0], image[x1][y1] =  image[x1][y1], image[x0][y0]
    if numbers[x1][y1] == y*y1+x1+1:
        pass
    else:
        pass
    DISPLAY.blit(image[x1][y1],cuadros[x1][y1])
    pygame.display.flip()

def redraw(i,j,rect = None):
    if rect is None:
        rect = cuadros[i][j]
    if (i,j) == freeSquare:
        pygame.draw.rect(DISPLAY,WHITE,rect)
        return
    DISPLAY.blit(image[i][j],rect)
    pygame.display.update()

def redrawBoard():
    for i in range(x):
        for j in range(y):
            redraw(i,j)

def moveRandom(times = 1):
    global freeSquare
    last = None
    while times:
        i,j = freeSquare
        add = random.choice([1,-1])
        moveX = random.choice([0,1])
        if moveX and last != "x":
            i = i+add if add > 0 and i < x-1 or add < 0 and i > 0 else i-add
            newPosition = (i, j)
            change(freeSquare, newPosition)
            freeSquare = newPosition
            last = "x"
            times -= 1
        elif not moveX and last != "y":
            j = j+add if add > 0 and j < y-1 or add < 0 and j > 0 else j-add
            newPosition = (i, j)
            change(freeSquare, newPosition)
            freeSquare = newPosition
            last = "y"
            times -= 1

def isFinish():
    for i in range(x):
        for j in range(y):
            if numbers[i][j] and numbers[i][j] != y*j+i+1:
                print("DISTINTOS",numbers[i][j], y*j+i+1)
                return False
    return True

image = setImage()
DISPLAY = pygame.display.set_mode((sq_x*x, sq_y*y), 0, 32)
clock = pygame.time.Clock()

# Create board and remix
createBoard()
pygame.time.wait(3000)
moveRandom(150)

continuar = True
while True:
    pygame.display.update()
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN:
        if event.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
            newPosition = move(event.key)
            if newPosition != freeSquare:
                change(freeSquare, newPosition)
                freeSquare = newPosition
        elif event.key == K_KP_ENTER:
            moveRandom()
        elif event.key == K_RETURN:
            if continuar: moveRandom(100)
            else: break
        redraw(*freeSquare)
        if isFinish():
            basicFont = pygame.font.SysFont(None, 56)
            text = basicFont.render('You Win!!', True, WHITE)
            rect = text.get_rect()
            rect.centerx = DISPLAY.get_rect().centerx
            rect.centery = DISPLAY.get_rect().centery
            pygame.draw.rect(DISPLAY, RED, (rect.left - 20,
                rect.top - 20, rect.width + 40, rect.height + 40))
            DISPLAY.blit(text, rect)
            continuar = False
            pygame.display.update()
    clock.tick(30)
pygame.time.wait(15*1000)
