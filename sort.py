import time
"""
Author: Sean O'Malley

Description:
Various sorting algorithm methods to use for project
"""


NANOSECOND = 1000000000

def bubbleSort(arr):

    comparisons = 0
    modifications = 0
    startTime = time.time()

    for i in range(0, len(arr) - 1):
        for j in range(0, len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                modifications += 2
            comparisons += 1
    endTime = time.time()
    print(arr)
    print('time: {:f} comparisons: {:d} modifications: {:d}'.format((endTime - startTime), comparisons, modifications))



def merge(arr, l, m, r):

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
        if tempL[i] <= tempR[j]:
            arr[k] = tempL[i]
            i += 1
        else:
            arr[k] = tempR[j]
            j += 1
        k += 1

    while i < len(tempL):
        arr[k] = tempL[i]
        i += 1
        k += 1
    
    while j < len(tempR):
        arr[k] = tempR[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    
    if l < r:
        m = l + (r - l) // 2

        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)



def quickSort(arr, l, r):

    if (l < r):
        p = partition(arr, l, r)
        quickSort(arr, l, p - 1)
        quickSort(arr, p + 1, r)

def partition(arr, l, r):
    p = arr[l]
    i = l
    j = r + 1

    while i < j:
        while arr[i] < p:
            i += 1
        while arr[j] > p:
            j -= 1
        arr[i], arr[j] = arr[j], arr[i]
    arr[i], arr[j] = arr[j], arr[i]
    arr[l], arr[j] = arr[j], arr[l]

    return j


arr = [3, 7, 1, 0, 5, 2, 9, 12, 7, 4, 0]
quickSort(arr, 0, len(arr) - 1)
print(arr)