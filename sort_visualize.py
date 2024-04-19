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

sorting = False

def bubbleSort(arr, lock):
    global currentPos1
    global currentPos2


    comparisons = 0
    modifications = 0

    for i in range(0, len(arr) - 1):
        for j in range(0, len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                modifications += 2
                with lock:
                    currentPos1 = j
                    currentPos2 = j + 1
                time.sleep(0.0001)
            comparisons += 1
    
    return [comparisons, modifications]



def merge(arr, l, m, r):

    comps = 0
    mods = 0

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
        comps += 1
        if tempL[i] <= tempR[j]:
            arr[k] = tempL[i]
            i += 1
            mods += 1
        else:
            arr[k] = tempR[j]
            j += 1
            mods += 1
        k += 1

    while i < len(tempL):
        comps += 1
        mods += 1
        arr[k] = tempL[i]
        i += 1
        k += 1
    
    while j < len(tempR):
        comps += 1
        mods += 1
        arr[k] = tempR[j]
        j += 1
        k += 1
    
    return [comps, mods]

def mergeSort(arr, l, r):
    
    if l < r:
        m = l + (r - l) // 2

        things = mergeSort(arr, l, m)
        things2 = mergeSort(arr, m + 1, r)
        things3 = merge(arr, l, m, r)

        return [things[0] + things2[0] + things3[0], things[1] + things2[1] + things3[1]]
    return [0, 0]




def partition(arr, l, r, lock):

    global currentPos1
    global currentPos2

    comps = 0
    mods = 0
    
    p = arr[r]
 
    i = l - 1

    for j in range(l, r):
        comps += 1
        if arr[j] <= p:
 
            i = i + 1
 

            (arr[i], arr[j]) = (arr[j], arr[i])
            with lock:
                currentPos1 = j
                currentPos2 = j + 1

            mods += 2
            # time.sleep(0.001)
 
    (arr[i + 1], arr[r]) = (arr[r], arr[i + 1])
    with lock:
        currentPos1 = j
        currentPos2 = j + 1
    mods += 1
    # time.sleep(0.001)
 

    return [i + 1, comps, mods]
 
 
def quickSort(arr, l, r, lock):
    global sorting
    sorting = True
    if l < r:
        things = partition(arr, l, r, lock)
 
        things2 = quickSort(arr, l, things[0] - 1, lock)
 
        things3 = quickSort(arr, things[0] + 1, r, lock)

        sorting = False
        return [things[1] + things2[0] + things3[0], things[2] + things2[1] + things3[1]]
    sorting = False
    return [0, 0]

