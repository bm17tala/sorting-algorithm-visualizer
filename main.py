import sys
from gui import runGUI
from sort_tests import runTests
from sort_tests import LATITUDE
from sort_tests import LONGITUDE


"""
Author: Brenden Talasco

Description:
Main execution script. Get a .tmg
file from the user and interpret it.
"""

# const for file type
FILE_TYPE = ".tmg"


# class for holding either latitude or longitude data for a point
# they must hold EITHER latitude or longitude, so they can be sorted by either
# latitude or longitude.
class VertexNode:
    def __init__(self, name, data):
        self.name = name
        self.data = data

# 0. We need a bigger call stack size in order to support recursive sorting algorithms
sys.setrecursionlimit(0x7fffffff)


# 1. Check the file name entered of the user's file


# test out command line input
if len(sys.argv) != 2 or len(sys.argv[1]) < 5 or not sys.argv[1].endswith(FILE_TYPE):
    print("Proper usage: python main.py [File_name].tmg")
    sys.exit(1)

argument = sys.argv[1]


# 2. Attempt to open the file and interpret the data
try:
    with open(argument, 'r') as graph:
        print(f"Success! {argument} opened!\n")
        
        latitude = []
        longitude = []

        #Skip first line, irrelevant
        graph.readline()

        #Edges/vertices count line in second line
        line2 = graph.readline()

        # Get the first element from splitting the line (the number of edges)
        # and convert into an integer, save into vertices
        numVertices = int(line2.split()[0])

        # for each vertex in the file, save their latitudes and longitudes in the
        # lists
        for _ in range(numVertices):
            vertex, lat, long = graph.readline().split()
            latitude.append(VertexNode(vertex, float(lat)))
            longitude.append(VertexNode(vertex, float(long)))

except FileNotFoundError:
    print(f"File not found: {argument}")
    sys.exit(1)


while True:
    print("\nEnter one of the following:")
    print("(1) Visualize")
    print("(2) Run a test")
    userIn = input()
    if userIn == '1':
        while True:
            print("\nEnter one of the following:")
            print("(1) Sort by latitude")
            print("(2) Sort by longitude")
            userIn = input()
            if(userIn == '1'):
                runGUI(latitude)
                break
            if(userIn == '2'):
                runGUI(longitude)
                break
            else:
                print("Try again...")
        break
    elif userIn == '2':
        print(f"\nSorting {numVertices} vertices...\n")
        print("---latitudes---\n")
        runTests(latitude, LATITUDE)
        print("---longitudes---\n")
        runTests(longitude, LONGITUDE)
        break
    else:
        print("Try again...")


