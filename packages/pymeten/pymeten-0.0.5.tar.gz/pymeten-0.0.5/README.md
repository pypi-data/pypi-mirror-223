# Documentation
https://openasi.github.io/pymeten/ 

# itutils
This module contains utility functions for debugging and analyzing code.

showit(inp): Prints the names of arguments passed to the calling function and displays the value of inp. sizeit(inp): Calculates and prints the size of the input object inp in human-readable format (bytes, KB, MB, GB, TB, or PB). Returns the size in bytes. timeit(fn): Measures the execution time of the function fn by running it multiple times and provides statistics such as average time, maximum loop time, and minimum loop time. checkit(fn): Executes the function fn, prints its source code, and returns the result.

Note: These functions utilize the inspect module to gather information about the calling context and function source code.

# Triton Benchmark Sizes

The `triton_benchmark_sizes` function is used to benchmark the performance of different kernel providers on input sizes. It takes the following parameters:

- `input_map`: A dictionary that maps input names to functions generating input tensors.
- `kernel_map`: A dictionary that maps kernel provider names to kernel functions.
- `sizes` (optional): A list of input sizes to be tested. Default is `[4096]`.
- `log_size` (optional): A boolean indicating whether the x-axis for plot should be logarithmic. Default is `True`.
- `colors` (optional): A list of colors for plotting. If not provided, default colors will be used.
- `line_styles` (optional): A list of line styles for plotting. If not provided, solid lines will be used.
- `metric_config` (optional): An object specifying the configuration for metrics. Default is an empty configuration.
- `print_data` (optional): A boolean indicating whether to print benchmark data. Default is `True`.
- `show_plots` (optional): A boolean indicating whether to display the benchmark plots. Default is `True`.
- `save_path` (optional): A string representing the path to save the benchmark plots. Default is an empty string.

Example usage:

```python
# Define input_map
input_map = {
    'x': lambda size: torch.rand(size, device='cuda', dtype=torch.float32),
    'y': lambda size: torch.rand(size, device='cuda', dtype=torch.float32)
}

# Define kernel_map
kernel_map = {
    'torch': lambda x, y: x + y,
    'triton': lambda x, y: add(x, y)
}

# Perform benchmarking
triton_benchmark_sizes(input_map, kernel_map)
```

Please note that the current implementation only supports scalar values for `sizes`. The benchmarking results are displayed in plots, and optional data printing and saving features can be enabled by setting the corresponding parameters.

Remeber to install python-dev.