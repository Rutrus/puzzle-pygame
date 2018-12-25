import sys, pygame, time, random
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

x = BOARD_X_AXIS = 4
y = BOARD_y_AXIS = 4
freeSquare = (BOARD_X_AXIS-1,BOARD_y_AXIS-1)
pygame.init()

DISPLAY = pygame.display.set_mode((166*x, 133*y), 0, 32)
clock = pygame.time.Clock()

def getColor(x,y):
    if (x+y)%2: return WHITE
    else: return GREY

cuadros = [ [[] for i in range(x)] for j in range(y)]
textos = [ [[] for i in range(x)] for j in range(y)]
numbers = [ [[] for i in range(x)] for j in range(y)]
for i in range(x):
    for j in range(y):
        cuadros[i][j] = pygame.draw.rect(DISPLAY, getColor(i,j), (166*i,133*j,166,133))
        if (i,j) == (x-1,y-1):
            textos[i][j] = pygame.font.SysFont(None,48).render("", True, BLACK)
            numbers[i][j] = 0
            continue
        numbers[i][j] = y*j+i+1
        textos[i][j] = pygame.font.SysFont(None,48).render(str(numbers[i][j]), True, BLACK)
        rectTexto = textos[i][j].get_rect()
        rectTexto.centerx = cuadros[i][j].centerx
        rectTexto.centery = cuadros[i][j].centery
        DISPLAY.blit(textos[i][j],rectTexto)

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
    global textos
    # Because pieces move in reverse way
    # Free space is from_ -> to_
    # Piece is to_ -> from_
    x0,y0 = to_
    x1,y1 = from_
    texto0 = textos[x0][y0] # Piece
    texto1 = textos[x1][y1] # Free space
    cuadro0 = cuadros[x0][y0]
    cuadro1 = cuadros[x1][y1]

    rectTexto = texto0.get_rect()
    rectCuadro = cuadro0.copy()
    rectTexto.centerx = cuadro0.centerx
    rectTexto.centery = cuadro0.centery

    if cuadro0.centerx != cuadro1.centerx:
        a = cuadro0.centerx
        b = cuadro1.centerx
        exp = 1
        if a > b: exp = -1
        for i in range(a,b,5*exp):
            rectTexto.centerx = i
            rectCuadro.centerx = i
            redraw(x0,y0)
            redraw(x1,y1)
            DISPLAY.blit(texto0,rectTexto)
    else:
        a = cuadro0.centery
        b = cuadro1.centery
        exp = 1
        if a > b: exp = -1
        for i in range(a,b,5*exp):
            rectTexto.centery = i
            rectCuadro.centery = i
            redraw(x0,y0)
            redraw(x1,y1)
            DISPLAY.blit(texto0,rectTexto)

    textos[x0][y0], textos[x1][y1] = texto1, texto0
    numbers[x0][y0], numbers[x1][y1] =  numbers[x1][y1], numbers[x0][y0]
    print(numbers[x1][y1],y*y1+x1+1)
    if numbers[x1][y1] == y*y1+x1+1:
        textos[x1][y1] = pygame.font.SysFont(None,48)
        textos[x1][y1] = textos[x1][y1].render(str(numbers[x1][y1]), True, BLUE)
    else:
        textos[x1][y1] = pygame.font.SysFont(None,48)
        textos[x1][y1] = textos[x1][y1].render(str(numbers[x1][y1]), True, BLACK)
    DISPLAY.blit(textos[x1][y1], rectTexto)

def redraw(i,j):
    rectTexto = textos[i][j].get_rect()
    rectTexto.centery = cuadros[i][j].centery
    rectTexto.centerx = cuadros[i][j].centerx
    pygame.draw.rect(DISPLAY, getColor(i,j), cuadros[i][j])
    DISPLAY.blit(textos[i][j], rectTexto)

def redrawBoard():
    for i in range(x):
        for j in range(y):
            redraw(i,j)

def moveRandom(num = 1):
    global freeSquare
    while num:
        i,j = freeSquare
        add = random.choice([1,-1])
        if random.choice([0,1]):
            i = i+add if add > 0 and i < x-1 or add < 0 and i > 0 else i-add
            newPosition = (i, j)
            change(freeSquare, newPosition)
            freeSquare = newPosition
        else:
            j = j+add if add > 0 and j < y-1 or add < 0 and j > 0 else j-add
            newPosition = (i, j)
            change(freeSquare, newPosition)
            freeSquare = newPosition
        num -= 1

def isFinish():
    for i in range(x):
        for j in range(y):
            if numbers[i][j] and numbers[i][j] != y*j+i+1:
                print("DISTINTOS",numbers[i][j], y*j+i+1)
                return False
    return True

#moveRandom(500)
redrawBoard()
continuar = True
while continuar:
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
            for i in range(100):
                moveRandom()
        redraw(freeSquare[0],freeSquare[1])
        if isFinish():
            # Set up the fonts.
            basicFont = pygame.font.SysFont(None, 56)
            # Set up the text.
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

time.sleep(15)
