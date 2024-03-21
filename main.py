import sys


"""
Author: Brenden Talasco

Description:
Main execution script. Get a .tmg
file from the user and interpret it.
"""


# test out command line input
if len(sys.argv) != 2:
    print(f"Proper usage: python main.py [File name]")
    exit()

argument = sys.argv[1]


print(argument)
