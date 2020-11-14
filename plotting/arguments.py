#!/bin/env python
"""
Put module documentation here
"""

import pandas


class PlotArguments(object):
    def __init__(
            self,
            data: pandas.DataFrame,
            plot_type: str,
            title: str = None,
            x_title: str = None,
            y_title: str = None,
            x_axis: str = None,
            group: str = None,
            trace_columns: [list, tuple, str] = None,
            **kwargs
    ):
        self.data = data
        self.plot_type = plot_type
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.x_axis = x_axis
        self.group = group
        self.trace_columns = trace_columns

    def validate(self) -> list:
        invalid_arguments = list()

        if self.data is None:
            invalid_arguments.append("data")
        elif isinstance(self.data.index, pandas.RangeIndex) and self.x_axis is None:
            invalid_arguments.append("x_axis")

        return invalid_arguments


class AnimatedPlotArguments(PlotArguments):
    def __int__(self, animation_column: str, **kwargs):
        super().__init__(**kwargs)
        self.animation_column = animation_column

    def validate(self) -> list:
        invalid_arguments = super().validate()

        if self.animation_column is None:
            invalid_arguments.append("animation_column")

        return invalid_arguments


class MapArguments(PlotArguments):
    def __init__(self, basemap: str, **kwargs):
        super().__init__(**kwargs)
        self.basemap = basemap

    def validate(self) -> list:
        invalid_arguments = super().validate()

        if self.basemap is None:
            invalid_arguments.append("basemap")

        return invalid_arguments


class AnimatedMapArguments(PlotArguments):
    def __init__(self, basemap: str, animation_column: str, **kwargs):
        super().__init__(**kwargs)
        self.animation_column = animation_column
        self.basemap = basemap

    def validate(self) -> list:
        invalid_arguments = super().validate()

        if self.basemap is None:
            invalid_arguments.append("basemap")

        if self.animation_column is None:
            invalid_arguments.append("animation_column")

        return invalid_arguments
