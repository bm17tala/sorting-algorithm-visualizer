import pygame
import sort

WIDTH = 854
HEIGHT = 480
TITLE = "Academic Showcase"

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


testArray = [ i for i in range(1000) ]


max = testArray[0]
for i in range(1, len(testArray)):
    if testArray[i] > max:
        max = testArray[i]

heightRatio = max / HEIGHT 


barWidth = WIDTH / len(testArray)

pygame.init()

screen = pygame.display.set_mode( (WIDTH, HEIGHT), pygame.RESIZABLE )
pygame.display.set_caption(TITLE)

running = True

clock = pygame.time.Clock()

while running:
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
              running = False 
              continue
            
        currentHeight = screen.get_height()
        currentWidth = screen.get_width()

        heightRatio = max / currentHeight
        barWidth = currentWidth / len(testArray)

        screen.fill(BLACK)
        
        for i in range(len(testArray)):
            pygame.draw.rect(screen, GREEN, [ i*barWidth, currentHeight - testArray[i] * 1/heightRatio,
                                              barWidth, (testArray[i] * 1/heightRatio)],0)
        
        pygame.display.flip()
        
        
        clock.tick(60)

pygame.quit()
