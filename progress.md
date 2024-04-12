# Progress Reports

### Week of March 18-22

This week, we started out by slightly revising our proposal to instead
be researching different sorting algorithms in order to determine the range of
westmost/eastmost, and northmost/southmost points, a variant of the 
vertex extremes algorithm. 

We also wrote some boilerplate code that opens a .tmg file,
scans each vertex into arrays that will be later used in
the sorting algorithms.

At the moment there is no serious change to the time table, the goals of this
week were achieved.

* Week of 4/2-4/5 - Write implementations of Bubble Sort, Merge Sort, and Quick Sort. 
Decide what GUI library/package to use, and perform some tech tests with it.
* Week of 4/8-4/12 - Complete tests, collect data, bug testing of algorithm implementation.
* Week of 4/15-4/19 - Begin work on graphical representation of algorithms, GUI's 
* Week of 4/22-4/25 - Finish/bugtest Graphical representations, possibly complete a presentation to display alongside running program.

### Week of April 2-5

This week, we worked on writing the implementations of the sorting algorithms, and began testing on the GUI which will present vertices being sorted in real-time.

There are some known bugs currently with the GUI, however the sorting algorithms 
are complete aside from some comparison and modification counters in the quicksort 
and mergesort algorithms possibly requiring more testing.

Since the GUI was already started today, the focus during the week of 4/15-19 can be
more focused on bug testing the GUI and adding more capability to the GUI such as file selection,
changing time of thread sleeps, etc.

* Week of 4/8-4/12 - Complete tests of sorting algorithms, collect data, bug testing of algorithm implementation.
* Week of 4/15-4/19 - Complete bug testing of GUI implementation, and add more capability to the GUI in general as described above 
* Week of 4/22-4/25 - Finish/bugtest Graphical representations, possibly complete a presentation to display alongside running program.

### Week of April 8-12

This week, we worked on refining the GUI which will present vertices being sorted in real-time. We added sounds
that the GUI produces as it sorts vertices, and a red line that appears over the vertices currently being modified.

Still some bugs regarding the GUI need to be fixed, but all of the basic functionality for the GUI is in place at this point.
We collected some early test data on the sorting algorithms with a few different tmg files. We noticed that larger sized tmg files
with high amounts of vertices seem to break our quicksort algorithm and cause stack overflow exceptions, so our quicksort algorithm
will need to be revised next week.

* Week of 4/15-4/19 - Fix Quicksort algorithm, collect data from tests of sorting algorithms, complete debugging of GUI implementation.
* Week of 4/22-4/25 - Finish/bugtest graphical representations, complete analysis of data, possibly complete a presentations to display alongside running program.
