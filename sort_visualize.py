import time
from random import randint
"""
Author: Sean O'Malley
Edited by: Brenden Talasco

Description:
Various sorting algorithm methods to use for project

Same as sort_tests.py, but edited to add code necessary 
for algorithm visualization

"""

currentPos1 = -1
currentPos2 = -1
comparisons = 0
modifications = 0

delay = 0.01

def resetValues(posLock, statLock):
    global currentPos1
    global currentPos2
    global comparisons
    global modifications

    with posLock:
        with statLock:
            currentPos1 = -1
            currentPos2 = -1
            comparisons = 0
            modifications = 0



def bubbleSort(arr, posLock, statLock, speedLock):
    global currentPos1
    global currentPos2
    global comparisons
    global modifications

    for i in range(0, len(arr) - 1):
        for j in range(0, len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                with statLock:
                    modifications += 2
                with posLock:
                    currentPos1 = j
                    currentPos2 = j + 1
                with speedLock:
                    time.sleep(delay)
                
            with statLock:
                comparisons += 1
    
    return [comparisons, modifications]



def merge(arr, l, m, r, posLock, statLock, speedLock):

    global comparisons
    global modifications
    global currentPos1
    global currentPos2

    tempL = [0] * (m - l + 1)
    tempR = [0] * (r - m)

    for i in range(0, len(tempL)):
        tempL[i] = arr[l + i]

    for i in range(0, len(tempR)):
        tempR[i] = arr[m + 1 + i]

    i = 0
    j = 0
    k = l
    
    while i < len(tempL) and j < len(tempR):
        with statLock:
            comparisons += 1
        if tempL[i] <= tempR[j]:
            arr[k] = tempL[i]
            with posLock:
                currentPos1 = k
            i += 1
            with statLock:
                modifications += 1
            time.sleep(delay)
        else:
            arr[k] = tempR[j]
            with posLock:
                currentPos1 = k
            j += 1
            with statLock:
                modifications += 1
            time.sleep(delay)
        k += 1

    while i < len(tempL):
        with statLock:
            modifications += 1
        arr[k] = tempL[i]
        with posLock:
            currentPos2 = k
        time.sleep(delay)
        i += 1
        k += 1
    
    while j < len(tempR):
        with statLock:
            modifications += 1
        arr[k] = tempR[j]
        with posLock:
            currentPos2 = k
        time.sleep(delay)
        j += 1
        k += 1
    
    return [comparisons, modifications]

def mergeSort(arr, l, r, posLock, statLock, speedLock):
    

    if l < r:
        m = l + (r - l) // 2

        things = mergeSort(arr, l, m, posLock, statLock, speedLock)
        things2 = mergeSort(arr, m + 1, r, posLock, statLock, speedLock)
        things3 = merge(arr, l, m, r, posLock, statLock, speedLock)

        return [things[0] + things2[0] + things3[0], things[1] + things2[1] + things3[1]]
    return [0, 0]




def partition(arr, l, r, posLock, statLock, speedLock):

    global currentPos1
    global currentPos2
    global comparisons
    global modifications
    
    
    p = arr[r]
 
    i = l - 1

    for j in range(l, r):
        with statLock:
            comparisons += 1

        if arr[j] <= p:
 
            i = i + 1
 

            (arr[i], arr[j]) = (arr[j], arr[i])
            with posLock:
                currentPos1 = i
                currentPos2 = j

            with statLock:
                modifications += 2
            time.sleep(delay)
 
    (arr[i + 1], arr[r]) = (arr[r], arr[i + 1])
    with posLock:
        currentPos1 = i + 1
        currentPos2 = r

    with statLock:        
        modifications += 1
    time.sleep(delay)
 

    return [i + 1, comparisons, modifications]
 
 
def quickSort(arr, l, r, posLock, statLock, speedLock):


    if l < r:
        things = partition(arr, l, r, posLock, statLock, speedLock)
 
        things2 = quickSort(arr, l, things[0] - 1, posLock, statLock, speedLock)
 
        things3 = quickSort(arr, things[0] + 1, r, posLock, statLock, speedLock)

        
        return [things[1] + things2[0] + things3[0], things[2] + things2[1] + things3[1]]
    return [0, 0]

