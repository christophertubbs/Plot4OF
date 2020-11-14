#!/bin/env python

import plotting.arguments as arguments
import plotting.line as line_graphs
import plotting.plot as plots


def get_plot(plot_arguments: arguments.PlotArguments) -> plots.Plot:
    if plot_arguments.plot_type.lower() == 'line':
        if plot_arguments.group is None:
            return line_graphs.LinePlot(plot_arguments)
        return line_graphs.AnimatedLinePlot(plot_arguments)
    raise Exception("{} is not a valid plot type".format(plot_arguments.plot_type))
