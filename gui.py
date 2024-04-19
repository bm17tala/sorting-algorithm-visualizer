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
    
    
    

    # start the thread that actually sorts the array - begin with bubble sort, then we go to merge sort and quicksort later
    # posLock - locks on integer positions of values being modified
    # statLock - locks on integer values of number of comparisons and modifications
    posLock = threading.Lock()
    statLock = threading.Lock()
    t1 = threading.Thread(target=sort_visualize.bubbleSort, args=[onScreenArr, posLock, statLock])
    t1.start()

    # start the thread that will make the sorting noises
    soundLock = threading.Lock()
    soundThread = threading.Thread(target=playSound, args=[])
    soundThread.start()

    # has the 'sorting complete' message printed yet?
    msgSortingComplete = False

    # newOnScreenArr is what will actually get used to display vertices - we differentiate this from onScreenArr
    # in the case that there are more bars to display than pixels on screen to fit them (so we have to get average
    # values of a few vertices and just display them in one bar)
    newOnScreenArr = onScreenArr
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

        # If there are more vertices than pixels on the screen to render them, we have to take the average
        # of some calculated few of them and show that average in each bar instead - be sure to calculate
        # new min/max values since averages could change as the array is being sorted!
        if len(onScreenArr) > currentWidth:
            newOnScreenArr = average_of_chunks(onScreenArr, int(len(onScreenArr) / currentWidth))

            max = newOnScreenArr[0]
            for i in range(1, len(newOnScreenArr)):
                if newOnScreenArr[i] > max:
                    max = newOnScreenArr[i]

            min = newOnScreenArr[0]
            for i in range(1, len(newOnScreenArr)):
                if newOnScreenArr[i] < min:
                    min = newOnScreenArr[i]

        heightRatio = (max - min) / currentHeight

        # if there were originally more vertices than there are current pixels available, each bar is 1px wide
        if len(onScreenArr) > currentWidth:
            barWidth = 1
        # otherwise, we get the length of each bar based on how many chunks of 'averages' we have
        else:
            barWidth = currentWidth / len(newOnScreenArr)

        screen.fill(BLACK)

        for i in range(len(newOnScreenArr)):
            # The sorting algorithm has a thread lock in order to prevent race conditions
            # on currentPos1/2

            if (not msgSortingComplete) and (not t1.is_alive()):
                print("Sorting complete!")
                msgSortingComplete = True

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

        with statLock:
            drawText(f"Comparisons: {sort_visualize.comparisons} | Modifications: {sort_visualize.modifications}", 10, 10, screen)
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

def drawText(string, x, y, screen):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = font.render(string, True, (0xff,0xff,0xff))
    screen.blit(text_surface, (x,y))


