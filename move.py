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
pygame.display.set_caption('Hello world!')
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
for i in range(x):
    for j in range(y):
        if i == 0 and j == 2:
            cuadros[i][j] = pygame.Rect(0,400//3*2,500//x,400//y)
            textos[i][j] = pygame.font.SysFont(None,48).render("", True, BLACK)
            continue

        cuadros[i][j] = pygame.draw.rect(DISPLAY, getColor(i,j), (500//x*i,400//y*j,500//x,400//y))
        if i == 0 and j == 2:
            textos[i][j] = pygame.font.SysFont(None,48).render("", True, BLACK)
            continue
        textos[i][j] = pygame.font.SysFont(None,48).render(str(3*j+i+1), True, BLACK)
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
            redrawBoard(x0,y0)
            redrawBoard(x1,y1)
            DISPLAY.blit(texto0,rectTexto)
            pygame.display.flip()
    else:
        a = cuadro0.centery
        b = cuadro1.centery
        exp = 1
        if a > b: exp = -1
        for i in range(a,b,5*exp):
            rectTexto.centery = i
            rectCuadro.centery = i
            redrawBoard(x0,y0)
            redrawBoard(x1,y1)
            DISPLAY.blit(texto0,rectTexto)
            pygame.display.flip()

    textos[x0][y0], textos[x1][y1] = texto1, texto0

def redrawBoard(i = None, j = None):
    if i is None and j is None:
        for i in range(x):
            for j in range(y):
                rectTexto = textos[i][j].get_rect()
                rectTexto.centery = cuadros[i][j].centery
                rectTexto.centerx = cuadros[i][j].centerx
                pygame.draw.rect(DISPLAY, getColor(i,j), cuadros[i][j])
                DISPLAY.blit(textos[i][j], rectTexto)
    else:
        assert x is not None or y is not None, "Bad coordinates"
        rectTexto = textos[i][j].get_rect()
        rectTexto.centery = cuadros[i][j].centery
        rectTexto.centerx = cuadros[i][j].centerx
        pygame.draw.rect(DISPLAY, getColor(i,j), cuadros[i][j])
        DISPLAY.blit(textos[i][j], rectTexto)

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
