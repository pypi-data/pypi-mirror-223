# itutils
This module contains utility functions for debugging and analyzing code.

showit(inp): Prints the names of arguments passed to the calling function and displays the value of inp. sizeit(inp): Calculates and prints the size of the input object inp in human-readable format (bytes, KB, MB, GB, TB, or PB). Returns the size in bytes. timeit(fn): Measures the execution time of the function fn by running it multiple times and provides statistics such as average time, maximum loop time, and minimum loop time. checkit(fn): Executes the function fn, prints its source code, and returns the result.

Note: These functions utilize the inspect module to gather information about the calling context and function source code.

# Documentation
https://openasi.github.io/pymeten/ 