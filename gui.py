import pygame
import pysine
import threading
from random import randint 
import sort_visualize
import os

#Window Properties
WIDTH = 854
HEIGHT = 480
TITLE = "Academic Showcase"

#Some RBG Constants
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


#frequency to be played
frequency = 0


def runGUI(testArray):
    global frequency

    onScreenArr = []

    # we need to represent the testArray input (which has floating point values)
    # all as integers for them to get painted onto the screen properly - so
    # onScreenArr stores each vertex as an integer value, containing the precision
    for i in testArray:
        onScreenArr.append(int(i.data*100000))


    # find the max and min values of the new array to calculate height ratio, this way
    # all verticies are painted on the screen in a decent visible way (this prevents a
    # screen from being filled with mostly bars or mostly nothing)
    max = onScreenArr[0]
    for i in range(1, len(onScreenArr)):
        if onScreenArr[i] > max:
            max = onScreenArr[i]

    min = onScreenArr[0]
    for i in range(1, len(onScreenArr)):
        if onScreenArr[i] < min:
            min = onScreenArr[i]

    heightRatio = (max - min) / HEIGHT 

    # How wide should each bar be?
    barWidth = WIDTH / len(onScreenArr)

    #Once the array to be sorted is configured, then start up the GUI
    pygame.init()
    screen = pygame.display.set_mode( (WIDTH, HEIGHT), pygame.RESIZABLE )
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # start the thread that actually sorts the array
    posLock = threading.Lock()
    t1 = threading.Thread(target=sort_visualize.quickSort, args=[onScreenArr, 0, len(onScreenArr) - 1, posLock])
    t1.start()

    # start the thread that will make the sorting noises
    soundLock = threading.Lock()
    soundThread = threading.Thread(target=playSound, args=[])
    soundThread.start()

    # window loop:
    while True:
        for event in pygame.event.get(): 
            # When the GUI is closed, end all threads/close the entire program is os._exit(0)
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        # get current width/height of screen to determine if a new height ratio needs to be configured
        currentHeight = screen.get_height()
        currentWidth = screen.get_width()

        # If there are more vertices than 
        if len(onScreenArr) > currentWidth:
            newOnScreenArr = average_of_chunks(onScreenArr, int(len(onScreenArr) / currentWidth))
        else:
            newOnScreenArr = onScreenArr

        heightRatio = (max - min) / currentHeight
        if len(onScreenArr) > currentWidth:
            barWidth = 1
        else:
            barWidth = currentWidth / len(newOnScreenArr)

        screen.fill(BLACK)

        for i in range(len(newOnScreenArr)):
            with posLock:
                try:
                    if i == int(sort_visualize.currentPos1  / int(len(onScreenArr) / currentWidth)) or i == int(sort_visualize.currentPos2  / int(len(onScreenArr) / currentWidth)):
                        pygame.draw.rect(screen, RED, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                            
                        with soundLock:
                            frequency = ((newOnScreenArr[i]-min) * 1/heightRatio) + 500
                            
                    else:
                        pygame.draw.rect(screen, GREEN, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                except ZeroDivisionError:
                    if i == int(sort_visualize.currentPos1) or i == int(sort_visualize.currentPos2 ):
        
                        pygame.draw.rect(screen, RED, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                            
                        with soundLock:
                            frequency = ((newOnScreenArr[i]-min) * 1/heightRatio) + 500
                            
                    else:
                        pygame.draw.rect(screen, GREEN, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                    
        pygame.display.update()
        clock.tick(60)

def playSound():
    global frequency

    while sort_visualize.sorting:
        pysine.sine(frequency=frequency, duration=0.05) 

def average_of_chunks(arr, chunk_size):
    averages = []
    for i in range(0, len(arr), chunk_size):
        chunk = arr[i:i+chunk_size]
        average = sum(chunk) / len(chunk)
        averages.append(average)
    return averages
