"""
Author: zhangzn710@gmail.com

This module contains utility functions for debugging and analyzing code.

showit(inp): Prints the names of arguments passed to the calling function and displays the value of inp.
sizeit(inp): Calculates and prints the size of the input object inp in human-readable format (bytes, KB, MB, GB, TB, or PB). Returns the size in bytes.
timeit(fn): Measures the execution time of the function fn by running it multiple times and provides statistics such as average time, maximum loop time, and minimum loop time.
checkit(fn): Executes the function fn, prints its source code, and returns the result.

Note: These functions utilize the inspect module to gather information about the calling context and function source code.
"""

from time import time
import inspect

def showit(inp):
    """
    Calculates and prints the size of 'inp' in bytes, kilobytes (KB), megabytes (MB), gigabytes (GB), or terabytes (TB).
    
    Parameters:
        inp (ndarray): The input array or object to calculate the size of.
        
    Returns:
        int: The size of 'inp' in bytes.
    """
    print('\nxxxxxxxx')
    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)[1]
    string = inspect.getframeinfo(frame[0]).code_context[0].strip()
    args = string[string.find('(') + 1:-1].split(',')
    
    names = []
    for i in args:
        if i.find('=') != -1:
            names.append(i.split('=')[1].strip())
        
        else:
            names.append(i)
    
    print(names)

    print(inp)

    print('xxxxxxxx\n')

def sizeit(inp):
    """
    Calculates and prints the size of 'inp' in bytes, kilobytes (KB), megabytes (MB), gigabytes (GB),
    or terabytes (TB). Returns the size in bytes.

    Parameters:
    inp (ndarray): The input array or object to calculate the size of.

    Returns:
    int: The size of 'inp' in bytes.
    """
    
    print('\n--------')
    frame = inspect.currentframe()
    frame = inspect.getouterframes(frame)[1]
    string = inspect.getframeinfo(frame[0]).code_context[0].strip()
    args = string[string.find('(') + 1:-1].split(',')
    
    names = []
    for i in args:
        if i.find('=') != -1:
            names.append(i.split('=')[1].strip())
        
        else:
            names.append(i)
    
    print(names)

    bytes = inp.nbytes
    size = bytes

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            print("%3.1f %s" % (size, x))
            break
        size /= 1024.0
    else:
        print("%3.1f PB" % (size))

    print('--------\n')
    return bytes

def timeit(fn):
    """
    Measures the execution time of the provided function 'fn' over multiple runs, displaying the average,
    maximum, and minimum time taken.

    Parameters:
        fn (function): The function to be executed and timed.

    Returns:
        object: The return value of the provided function 'fn'.
    """

    print('\n========')
    print(inspect.getsource(fn))
    maxl = 0
    minl = 1e6
    total = 0

    for i in range(5):
        start = time()
        x = fn()
        #print(f'time: {time()-start}')

        taken = time()-start
        total += taken

        if taken > maxl:
            maxl = taken
        elif taken < minl:
            minl = taken

    print(f'avg: {total/5}, max loop: {maxl}, min loop: {minl}')

    print('========\n')
    return x

def checkit(fn):
    """
    Executes the provided function 'fn' and displays its source code and return value.

    Parameters:
        fn (function): The function to be executed and checked.

    Returns:
        object: The return value of the provided function 'fn'.
    """
    print('\n????????')
    print(inspect.getsource(fn))
    res = fn()
    print(res)
    print('????????\n')
    return res