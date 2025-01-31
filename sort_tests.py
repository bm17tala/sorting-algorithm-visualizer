import time
from copy import deepcopy
from random import randint
"""
Author: Sean O'Malley

Description:
Various sorting algorithm methods to use for project
"""

# consts for whether we're sorting latitude or longitude
LATITUDE = 0
LONGITUDE = 1


def bubbleSort(arr):

    comparisons = 0
    modifications = 0

    for i in range(0, len(arr) - 1):
        for j in range(0, len(arr) - 1 - i):
            if arr[j].data > arr[j + 1].data:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                modifications += 2
                
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
        if tempL[i].data <= tempR[j].data:
            arr[k] = tempL[i]
            i += 1
            mods += 1
        else:
            arr[k] = tempR[j]
            j += 1
            mods += 1
        k += 1

    while i < len(tempL):
        mods += 1
        arr[k] = tempL[i]
        i += 1
        k += 1
    
    while j < len(tempR):
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




def partition(arr, l, r):

    comps = 0
    mods = 0
    
    p = arr[r].data
 
    i = l - 1

    for j in range(l, r):
        comps += 1
        if arr[j].data <= p:
 
            i = i + 1
 

            (arr[i], arr[j]) = (arr[j], arr[i])

            mods += 2
 
    (arr[i + 1], arr[r]) = (arr[r], arr[i + 1])
    mods += 1
 

    return [i + 1, comps, mods]
 
 
def quickSort(arr, l, r):
    if l < r:
        things = partition(arr, l, r)
 
        things2 = quickSort(arr, l, things[0] - 1)
 
        things3 = quickSort(arr, things[0] + 1, r)

        return [things[1] + things2[0] + things3[0], things[2] + things2[1] + things3[1]]
    return [0, 0]


def testBubbleSort(arr, latOrLong):
    startTime = time.time_ns()
    test1 = bubbleSort(arr)
    endTime = time.time_ns()
    duration = (endTime - startTime) / 1000000000
    print('Bubble Sort - time: {:f} seconds, comparisons: {:d}, modifications: {:d}\n'.format(duration, test1[0], test1[1]))
    printResults(arr, latOrLong)

def testMergeSort(arr, latOrLong):
    startTime = time.time_ns()
    test2 = mergeSort(arr, 0, len(arr) - 1)
    endTime = time.time_ns()
    duration = (endTime - startTime) / 1000000000
    print('Merge Sort - time: {:f} seconds, comparisons: {:d} modifications: {:d}\n'.format(duration, test2[0], test2[1]))
    printResults(arr, latOrLong)

def testQuickSort(arr, latOrLong):
    startTime = time.time_ns()
    test3 = quickSort(arr, 0, len(arr) - 1)
    endTime = time.time_ns()
    duration = (endTime - startTime) / 1000000000
    print('Quick Sort - time: {:f} seconds, comparisons: {:d} modifications: {:d}\n'.format(duration, test3[0], test3[1]))
    printResults(arr, latOrLong)

def printResults(arr, latOrLong):
    if latOrLong == LATITUDE:
        print(f'\tNorthmost vertex: {arr[-1].name} : {arr[-1].data}' )
        print(f'\tSouthmost vertex: {arr[0].name} : {arr[0].data}\n' )
    else:
        print(f'\tEastmost vertex: {arr[-1].name} : {arr[-1].data}' )
        print(f'\tWestmost vertex: {arr[0].name} : {arr[0].data}\n' )
    

def runTests(arr, latOrLong):
    
    testBubbleSort(deepcopy(arr), latOrLong)
    testMergeSort(deepcopy(arr), latOrLong)
    testQuickSort(deepcopy(arr), latOrLong)