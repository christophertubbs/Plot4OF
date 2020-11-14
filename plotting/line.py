#!/bin/env python
"""
Put module documentation here
"""

import plotly.graph_objects as go

import plotting.plot as plot


class LinePlot(plot.Plot):
    def plot(self) -> go.Figure:
        figure = go.Figure(
            layout_title_text=self.args.title
        )

        traces = list()

        if self.args.trace_columns is None or len(self.args.trace_columns) == 0:
            traces = [self.args.data[column] for column in self.args.data.keys() if column != self.args.x_axis]
        elif isinstance(self.args.trace_columns, str):
            traces.append(self.args.data[self.args.trace_columns])
        else:
            traces = [self.args.data[name] for name in self.args.trace_columns]

        for trace in traces:
            figure.add_trace(
                go.Scatter(
                    x=self.args.data[self.args.x_axis],
                    y=trace
                )
            )

        return figure


class AnimatedLinePlot(plot.Plot):
    def plot(self) -> go.Figure:
        figure = go.Figure()

        return figure
