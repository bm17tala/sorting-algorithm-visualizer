import pygame
import pysine
import threading
from random import randint 
import sort_visualize
import os
from math import ceil
from copy import deepcopy
from time import sleep

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

#countdown until next shuffle for when algorithm completes
countdown = 15

pygame.init()


def runGUI(testArray, algorithm, argument):
    global frequency
    global t1
    global countdownTicking
    global countdown
    global onScreenArr
    global soundThread

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
    screen = pygame.display.set_mode( (WIDTH, HEIGHT), pygame.RESIZABLE )
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    # start the thread that actually sorts the array - begin with bubble sort, then we go to merge sort and quicksort later
    # posLock - locks on integer positions of values being modified
    # statLock - locks on integer values of number of comparisons and modifications
    # speedLock - lock for the time in seconds that the sorting algorithm should wait after each array modification
    posLock = threading.Lock()
    statLock = threading.Lock()
    speedLock = threading.Lock()

    t1 = None
    algName = None
    if algorithm == '1':
        t1 = threading.Thread(target=sort_visualize.bubbleSort, args=[onScreenArr, posLock, statLock, speedLock])
        algName = "BubbleSort"
    elif algorithm == '2':
        t1 = threading.Thread(target=sort_visualize.mergeSort, args=[onScreenArr, 0, len(onScreenArr)-1, posLock, statLock, speedLock])
        algName = "MergeSort"
    elif algorithm == '3':
        t1 = threading.Thread(target=sort_visualize.quickSort, args=[onScreenArr, 0, len(onScreenArr)-1, posLock, statLock, speedLock])
        algName = "QuickSort"

    t1.start()

    # start the thread that will make the sorting noises
    soundLock = threading.Lock()
    soundThread = threading.Thread(target=playSound, args=[])
    soundThread.start()

    # is the reset countdown ticking?
    countdownTicking = False

    # newOnScreenArr is what will actually get used to display vertices - we differentiate this from onScreenArr
    # in the case that there are more bars to display than pixels on screen to fit them (so we have to get average
    # values of a few vertices and just display them in one bar)
    newOnScreenArr = onScreenArr
    # window loop:

    fullScreen = False

    while True:
        for event in pygame.event.get(): 
            # When the GUI is closed, end all threads/close the entire program is os._exit(0)
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    with speedLock:
                        sort_visualize.delay /= 2
                elif event.key == pygame.K_s:
                    with speedLock:
                        sort_visualize.delay *= 2
                elif event.key == pygame.K_0:
                    with speedLock:
                        if sort_visualize.delay != 0:
                            sort_visualize.delay = 0
                            sort_visualize.sleeping = False
                        else:
                            sort_visualize.delay = 0.01
                            sort_visualize.sleeping = True

                        




        # get current width/height of screen to determine if a new height ratio needs to be configured
        currentHeight = screen.get_height()
        currentWidth = screen.get_width()

        # If there are more vertices than pixels on the screen to render them, we have to take the average
        # of some calculated few of them and show that average in each bar instead - be sure to calculate
        # new min/max values since averages could change as the array is being sorted!
        if len(onScreenArr) > currentWidth:
            newOnScreenArr = average_of_chunks(onScreenArr, ceil(len(onScreenArr) / currentWidth))
        else:
            newOnScreenArr = deepcopy(onScreenArr)

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
        # if len(onScreenArr) > currentWidth:
        #     barWidth = 1
        # # otherwise, we can just divide up our width by how many vertices we have to represent
        # else:
        barWidth = currentWidth / len(newOnScreenArr)

        screen.fill(BLACK)

        if not countdownTicking and not t1.is_alive():
                countdownThread = threading.Thread(target=shuffleCountdown, args=[testArray, algorithm, posLock, statLock, speedLock])
                countdownThread.start()

        for i in range(len(newOnScreenArr)):
            # The sorting algorithm has a thread lock in order to prevent race conditions
            # on currentPos1/2, along with comparison/modification counts

            

            with posLock:
                try:
                    if i == int(sort_visualize.currentPos1  / ceil(len(onScreenArr) / currentWidth)) or i == int(sort_visualize.currentPos2  / ceil(len(onScreenArr) / currentWidth)):
                        pygame.draw.rect(screen, RED, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                            
                        with soundLock:
                            frequency = ((newOnScreenArr[i]-min) * 1/heightRatio) + 100
                            
                    else:
                        pygame.draw.rect(screen, GREEN, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                #Should get thrown if we aren't averaging out anything AKA there are more pixels on screen that vertices - this works like an effective if statement
                except ZeroDivisionError:
                    if i == int(sort_visualize.currentPos1) or i == int(sort_visualize.currentPos2 ):
        
                        pygame.draw.rect(screen, RED, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)
                            
                        with soundLock:
                            frequency = ((newOnScreenArr[i]-min) * 1/heightRatio) + 100
                            
                    else:
                        pygame.draw.rect(screen, GREEN, [ i*barWidth, currentHeight - (newOnScreenArr[i]-min) * 1/heightRatio,
                                                            barWidth, ( (newOnScreenArr[i]-min) * 1/heightRatio)],0)

        drawText(f"{algName}", 10, 10, screen)
        with statLock:
            drawText(f"Comparisons: {"{:,}".format(sort_visualize.comparisons)}", 10, 50, screen)
            drawText(f"Modifications: {"{:,}".format(sort_visualize.modifications)}", 10, 90, screen)
        with speedLock:
            drawText(f"Swap delay: {sort_visualize.delay} seconds", 10, 130, screen)
        drawText(f"{argument}", 10, 170, screen) 

        if not t1.is_alive():
            drawText(f"Sorting completed! Resetting in {countdown} seconds...", currentWidth / 2 - 200, currentHeight / 2, screen)

        pygame.display.update()
        clock.tick(60)




def shuffleCountdown(testArray, algorithm, posLock, statLock, speedLock):
    global countdown
    global countdownTicking
    global t1
    global onScreenArr
    global soundThread

    #count down 15 seconds

    countdownTicking = True

    while countdown != 0:
        sleep(1)
        countdown -= 1

    countdown = 15
    
    #then shuffle the array and begin sorting again

    onScreenArr = []
    for i in testArray:
        onScreenArr.append(int(i.data*100000))

    sort_visualize.resetValues(posLock, statLock)

    if algorithm == '1':
        t1 = threading.Thread(target=sort_visualize.bubbleSort, args=[onScreenArr, posLock, statLock, speedLock])
    elif algorithm == '2':
        t1 = threading.Thread(target=sort_visualize.mergeSort, args=[onScreenArr, 0, len(onScreenArr)-1, posLock, statLock, speedLock])
    elif algorithm == '3':
        t1 = threading.Thread(target=sort_visualize.quickSort, args=[onScreenArr, 0, len(onScreenArr)-1, posLock, statLock, speedLock])

    t1.start()

    soundThread = threading.Thread(target=playSound, args=[])
    soundThread.start()

    countdownTicking = False






def playSound():
    global frequency

    while t1.is_alive():
        pysine.sine(frequency=frequency, duration=0.05) 

def average_of_chunks(arr, chunk_size):
    averages = []
    for i in range(0, len(arr), chunk_size):
        chunk = arr[i:i+chunk_size]
        average = sum(chunk) / len(chunk)
        averages.append(average)
    return averages

def drawText(string, x, y, screen):
    font = pygame.font.SysFont('Comic Sans MS', 21)
    text_surface = font.render(string, True, (0x0,0x0,0x0))
    screen.blit(text_surface, (x-1,y+1))
    text_surface = font.render(string, True, (0xff,0xff,0xff))
    screen.blit(text_surface, (x,y))
    


