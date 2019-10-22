This project converts a GeoDB file containing polygons and their public transport grades into a csv file containing s2cells and their grade. For more information about s2cells see : https://github.com/google/s2geometry or http://s2geometry.io/. The cellIDs, which are the first value, can be inserted into https://s2.sidewalklabs.com/regioncoverer/ in order to show them on a map. Be sure to insert hex values since the website does not work for dec or bin numbers.

The python-program was run in the venv folder so it should contain all required libraries.

The Final_OeVGK_2018.gdb.zip contains all the data needed. For now only one of six layers was used.

The program itself is in the challengeproject.py file.

The output of the program is saved in the oev-grades.csv file.
