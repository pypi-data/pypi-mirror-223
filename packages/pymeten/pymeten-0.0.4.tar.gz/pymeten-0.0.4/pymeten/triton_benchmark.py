#%%
import os
import math

import torch
import triton
#https://triton-lang.org/main/search.html?q=do_bench&check_keywords=yes&area=default
import matplotlib.colors as mcolors

from typing import Callable, Dict

InputFnType = Callable[[int], torch.Tensor]
InputType = Dict[str, InputFnType]
KernelType = Dict[str, Callable]

MeasureFnType = Callable[[int, float], float]


# %%
from enum import Enum
all_line_styles = ('solid', 'dotted', 'dashed', 'dashdot', 'dashdotdotted', 
               'loosely solid', 'loosely dotted', 'loosely dashed', 'loosely dashdot', 'loosely dashdotdotted')

class MetricUnit(Enum):
    GBPS = 'GB/s'
    TBPS = 'TB/s'
    GFLOPS = 'GFLOPS'
    TFLOPS = 'TFLOPS'
    MS = 'MS'

class MetricConfig:
    """
    Configuration class for metric calculations.

    """

    unit = MetricUnit.GBPS
    num_ops = 1
    num_bytes = 12 # A(4)+B(4)=C(4)
    def __init__(self, unit=MetricUnit.MS, num_ops=None, num_bytes=None, calc_measure_fn:MeasureFnType = None):
        """
        Initializes a MetricConfig object.

        Args:
            unit (MetricUnit): The unit of measurement.
            num_ops (int): The number of operations per element.
            num_bytes (int): The number of bytes per element. 
            calc_measure_fn (callable): A function for calculating the measure (ops per millisecond or bytes per millisecond).

        Raises:
            AssertionError: If mandatory arguments are not provided for certain units.
        """
        self.unit = unit
        self.num_ops = num_ops
        self.num_bytes = num_bytes
        if unit.name.endswith('B/s'):
            assert num_bytes is not None or calc_measure_fn is not None, f'Must provide `num_bytes` when using unit {unit}'
        elif unit.name.endswith('FLOPS'):
            assert num_ops is not None or calc_measure_fn is not None, f'Must provide `num_ops` when using unit {unit}'
        self.calc_measure_fn = calc_measure_fn

    def get_metric(self, ms, size):
        """
        Calculates the metric value based on the configuration.

        Args:
            ms (float): The time in milliseconds.
            size (int or tuple/list): The size of the input.

        Returns:
            float: The calculated metric value.
        """
        if self.calc_measure_fn is not None:
            num_ops_pms = self.calc_measure_fn(size, ms) # for FLOPS
            num_bytes_pms = self.calc_measure_fn(size, ms) # for B/s
        else:
            numel = size if not isinstance(size, list) and not isinstance(size, tuple) \
                        else math.prod(size)
            total_num_ops = self.num_ops * numel if self.num_ops is not None else 0
            total_num_bytes = self.num_bytes * numel if self.num_bytes is not None else 0
            num_ops_pms = total_num_bytes / ms
            num_bytes_pms = total_num_bytes / ms

        if self.unit == MetricUnit.MS:
            return int(ms)
        elif self.unit == MetricUnit.GBPS:
            return num_bytes_pms * 1e-6
        elif self.unit == MetricUnit.TBPS:
            return num_bytes_pms * 1e-9
        elif self.unit == MetricUnit.GFLOPS:
            return num_ops_pms * 1e-6
        elif self.unit == MetricUnit.TFLOPS:
            return num_ops_pms * 1e-9
        return 0


# %%
def triton_benchmark_sizes(input_map: InputType, kernel_map: KernelType,
                           sizes=[4096], log_size=True,
                           colors=None, line_styles=None, metric_config=MetricConfig(),
                           print_data=True, show_plots=True, save_path=''):
    """
    Perform benchmarking of Triton kernels with varying input sizes.

    Args:
        input_map (dict): A dictionary mapping input names to functions: size -> torch.Tensor.
        kernel_map (dict): A dictionary mapping kernel names to functions that perform the computation, the input arguments must match input_map keys. Or you can use **kwargs.
        sizes (list, optional): A list of input sizes to be tested. Defaults to [4096].
        log_size (bool, optional): Whether to use a logarithmic scale for the input size axis. Defaults to True.
        colors (list, optional): A list of colors to be used for plotting. Defaults to None.
        line_styles (list, optional): A list of line styles to be used for plotting. Defaults to None.
        metric_config (MetricConfig, optional): Configuration for metrics. Defaults to MetricConfig().
        print_data (bool, optional): Whether to print benchmark results. Defaults to True.
        show_plots (bool, optional): Whether to display the benchmark plots. Defaults to True.
        save_path (str, optional): Path to save the benchmark plot. Defaults to ''.

    Example: 
        Currently `sizes` can only be scalar.

        input_map = {
            'x': lambda size: torch.rand(size, device='cuda', dtype=torch.float32),
            'y': lambda size: torch.rand(size, device='cuda', dtype=torch.float32)
        }

        kernel_map = {
            'torch': lambda x, y: x + y,
            'triton': lambda x, y: add(x, y)
        }
    """
    providers = list(kernel_map.keys())
    assert len(providers) <= 10
    if colors is None:
        colors = list(mcolors.TABLEAU_COLORS.values())[:len(providers)]
    if line_styles is None:
        line_styles = ['-'] * len(providers)
    styles = list(zip(colors, line_styles))

    plot_name = 'test'

    # define the function
    @triton.testing.perf_report(
        triton.testing.Benchmark(
            x_names=['size'],  # Argument names to use as an x-axis for the plot.
            #TODO: x_vals=[math.prod(size) for size in sizes],
            x_vals=sizes,  # Different possible values for `x_name`.
            x_log=log_size,  # x axis is logarithmic.
            line_arg='provider',  # Argument name whose value corresponds to a different line in the plot.
            line_vals=providers,  # Possible values for `line_arg`.
            line_names=providers,  # Label name for the lines.
            styles=styles,  # Line styles.
            ylabel=metric_config.unit.name,  # Label name for the y-axis.
            plot_name=plot_name,  # Name for the plot. Used also as a file name for saving the plot.
            args={},  # Values for function arguments not in `x_names` and `y_name`.
        )
    )
    def benchmark(size, provider):
        # input initialization
        inputs = {}
        for input_name, input_init in input_map.items():
            inputs[input_name] = input_init(size)
    
        quantiles = [0.5, 0.2, 0.8]
        ms, min_ms, max_ms = triton.testing.do_bench(lambda: kernel_map[provider](**inputs), percentiles=quantiles)
        return metric_config.get_metric(ms, size), \
                metric_config.get_metric(max_ms, size), \
                metric_config.get_metric(min_ms, size)

    benchmark.run(print_data=print_data, show_plots=show_plots, save_path=save_path)



# %%
