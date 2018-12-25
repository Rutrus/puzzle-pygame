import sys, pygame, time, random
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)

pygame.init()

DISPLAY = pygame.display.set_mode((500, 400), 0, 32)
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

x = 3
y = 3

cuadros = [ [[] for i in range(x)] for j in range(y)]
textos = [ [[] for i in range(x)] for j in range(y)]
for i in range(x):
    for j in range(y):
        if i == 0 and j == 2:
            cuadros[i][j] = pygame.draw.rect(DISPLAY, RED, (0,400//3*2,500//x,400//y))
            textos[i][j] = pygame.font.SysFont(None,48).render("", True, BLACK)
            continue

        if (i+j)%2: choice = WHITE
        else: choice = GREY

        cuadros[i][j] = pygame.draw.rect(DISPLAY, choice, (500//x*i,400//y*j,500//x,400//y))
        textos[i][j] = pygame.font.SysFont(None,48).render(str(3*j+i+1), True, BLACK)

        rectTexto = textos[i][j].get_rect()
        rectTexto.centerx = cuadros[i][j].centerx
        rectTexto.centery = cuadros[i][j].centery
        DISPLAY.blit(textos[i][j],rectTexto)

freeSquare = (0,2)
# cuadros[0][2] =  pygame.draw.rect(DISPLAY, RED, (0,400//3*2,500//x,400//y))

def move(key):
    global freeSquare

    if key == K_LEFT and freeSquare[0] < 2:
        print("tecla left")
        freeSquare = (freeSquare[0]+1,freeSquare[1])
    elif key == K_RIGHT and freeSquare[0]:
        print("tecla right")
        freeSquare = (freeSquare[0]-1,freeSquare[1])
    elif key == K_UP and freeSquare[1] < 2:
        print("tecla up")
        freeSquare = (freeSquare[0],freeSquare[1]+1)
    elif key == K_DOWN and freeSquare[1]:
        print("tecla down")
        freeSquare = (freeSquare[0],freeSquare[1]-1)
    else:
        return
    #freeSquare = (freeSquare[0],freeSquare[1])

while True:
    # Coloring pixels
    # pixArray = pygame.PixelArray(DISPLAY)
    # for i in range(0,500,4):
    #     for j in range(0,400,25):
    #         pixArray[i][j] = random.choice([BLACK,WHITE])
    # del pixArray
    pygame.display.update()
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN:
        if event.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
            move(event.key)

    # pygame.display.update()
    # for event in pygame.event.get():
    #     if event.type == QUIT:
    #         pygame.quit()
    #         sys.exit()
