#!/bin/env python
"""
Put module documentation here
"""

from abc import abstractmethod

import plotly.graph_objects as go

import plotting.exceptions as exceptions
import plotting.arguments as arguments


class Plot(object):
    def __init__(self, args: arguments.PlotArguments):
        self.args = args
        self.validate()
        self.args.data.reset_index(inplace=True)

    @abstractmethod
    def plot(self) -> go.Figure:
        pass

    def validate(self):
        invalid_arguments = self.args.validate()

        if len(invalid_arguments) > 0:
            raise exceptions.MissingArgumentException(invalid_arguments)
