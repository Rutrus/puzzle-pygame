import sys, pygame, time, random
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

x = 3
y = 3

pygame.init()

DISPLAY = pygame.display.set_mode((166*x, 133*y), 0, 32)
clock = pygame.time.Clock()
DISPLAY.fill(RED)

# Set up the fonts.
basicFont = pygame.font.SysFont(None, 48)

# Set up the text.
text = basicFont.render('Hello world!', True, WHITE, BLACK)
textRect = text.get_rect()
textRect.centerx = DISPLAY.get_rect().centerx
textRect.centery = DISPLAY.get_rect().centery

# pygame.draw.rect(DISPLAY, RED, (textRect.left - 20,
#     textRect.top - 20, textRect.width + 40, textRect.height + 40))

def getColor(x,y):
    if (x+y)%2: return WHITE
    else: return GREY

cuadros = [ [[] for i in range(x)] for j in range(y)]
textos = [ [[] for i in range(x)] for j in range(y)]
numbers = [ [[] for i in range(x)] for j in range(y)]
for i in range(x):
    for j in range(y):
        cuadros[i][j] = pygame.draw.rect(DISPLAY, getColor(i,j), (500//x*i,400//y*j,500//x,400//y))
        if i == 0 and j == 2:
            textos[i][j] = pygame.font.SysFont(None,48).render("", True, BLACK)
            numbers[i][j] = 0
            continue
        numbers[i][j] = 3*j+i+1
        textos[i][j] = pygame.font.SysFont(None,48).render(str(numbers[i][j]), True, BLACK)
        rectTexto = textos[i][j].get_rect()
        rectTexto.centerx = cuadros[i][j].centerx
        rectTexto.centery = cuadros[i][j].centery
        DISPLAY.blit(textos[i][j],rectTexto)

freeSquare = (0,2)

def move(key):
    move = freeSquare
    if key == K_LEFT and freeSquare[0] < 2:
        print("Key: left")
        move = (move[0]+1,move[1])
    elif key == K_RIGHT and freeSquare[0]:
        print("Key: right")
        move = (move[0]-1,move[1])
    elif key == K_UP and freeSquare[1] < 2:
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
    print(numbers[x1][y1],3*y1+x1+1)
    if numbers[x1][y1] == 3*y1+x1+1:
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

def moveRandom():
    pass

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
        redrawBoard()
    clock.tick(30)
