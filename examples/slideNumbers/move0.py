import sys, pygame, time, random
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()

windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Hello world!')
# Set up the fonts.
basicFont = pygame.font.SysFont(None, 48)

# Set up the text.
text = basicFont.render('Hello world!', True, WHITE, BLACK)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

pygame.draw.rect(windowSurface, WHITE, (textRect.left - 20,
    textRect.top - 20, textRect.width + 40, textRect.height + 40))

while True:
    # Coloring pixels
    pixArray = pygame.PixelArray(windowSurface)
    for i in range(0,500,4):
        for j in range(0,400,25):
            pixArray[i][j] = random.choice([BLACK,WHITE])
    del pixArray
    windowSurface.blit(text, textRect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
