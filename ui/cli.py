#!/bin/env python
"""
Put module documentation here
"""

from argparse import ArgumentParser

import pandas

import plotting.arguments as arguments
import plotting.factory as plot_factory

__PLOT_TYPES = [
    "line",
]

def create_commandline_parser() -> ArgumentParser:
    """
    Creates a command line parser for the script
    
    :rtype: ArgumentParser
    :return: An argument parser used to collect the inputs to the script
    """
    parser = ArgumentParser("Plot CSV data plainly")
    parser.add_argument(
        "-t",
        metavar="type",
        dest="type",
        type=str,
        choices=__PLOT_TYPES,
        default=__PLOT_TYPES[0],
        help="The type of plot to create"
    )
    parser.add_argument("-T", metavar="title", dest="title", default=None, type=str, help="A title for the plot")
    parser.add_argument("-x", metavar="name", dest="xtitle", default=None, type=str, help="The title on the x axis")
    parser.add_argument("-y", metavar="name", dest="ytitle", default=None, type=str, help="The title on the y axis")
    parser.add_argument("-g", metavar="group", type=str, default=None, dest="group", help="A field to group on")
    parser.add_argument("target", type=str, help="The file to plot")
    parser.add_argument("xaxis", type=str, help="The column to use as the x-axis")
    parser.add_argument("columns", type=str, nargs="+", help="Values to plot on the y-axis")

    return parser


def get_plot_arguments() -> arguments.PlotArguments:
    parameters = create_commandline_parser().parse_args()
    frame = pandas.read_csv(parameters.target)

    is_animated = parameters.group is not None

    if parameters.type in ['line']:
        if is_animated:
            plot_arguments = arguments.AnimatedPlotArguments(
                group=parameters.group,
                data=frame,
                plot_type=parameters.type
            )
        else:
            plot_arguments = arguments.PlotArguments(data=frame, plot_type=parameters.type)
    else:
        raise Exception("This tool cannot plot {} graphs".format(parameters.type))

    plot_arguments.title = parameters.title
    plot_arguments.x_axis = parameters.xaxis
    plot_arguments.trace_columns = parameters.columns
    plot_arguments.y_title = parameters.ytitle
    plot_arguments.x_title = parameters.xtitle
    plot_arguments.group = parameters.group

    return plot_arguments


def main():
    """
    This is the entry point to the script's execution
    """
    plot_arguments = get_plot_arguments()
    graph = plot_factory.get_plot(plot_arguments)
    plot = graph.plot()
    plot.show()


if __name__ == "__main__":
    main() 