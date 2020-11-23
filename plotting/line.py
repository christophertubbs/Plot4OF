#!/bin/env python
"""
Put module documentation here
"""
from typing import List

import plotly.graph_objects as go

import plotting.plot as plot
import utilities.general as general


class LinePlot(plot.Plot):
    def plot(self) -> go.Figure:
        figure = go.Figure(
            layout_title_text=self.args.title
        )

        traces = list()

        if self.args.trace_columns is None or len(self.args.trace_columns) == 0:
            traces = [
                self.args.data[column]
                for column in self.args.data.keys()
                if column != self.args.x_axis
            ]
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
    def create_buttons(self) -> go.layout.Updatemenu:
        # Button argument definitions found at
        # https://plotly.com/javascript/plotlyjs-function-reference/

        play_button = go.layout.updatemenu.Button(
            args=[
                # Add a list of appropriate html elements to affect (None)
                None,
                # Define what animation attributes should be affected
                {
                    "frame": {
                        "duration": 500,
                        "redraw": False
                    },
                    "fromcurrent": True,
                    "transition": {
                        "duration": 300,
                        "easing": "quadratic-in-out"
                    }
                }
            ],
            label="Play",
            method="animate"
        )

        pause_button = go.layout.updatemenu.Button(
            args=[
                # Add a list of appropriate html elements to affect (None)
                [None],
                # Define what animation attributes should be affected
                {
                    "frame": {
                        "duration": 0,
                        "redraw": False
                    },
                    "mode": "immediate",
                    "transition": {
                        "duration": 0
                    }
                }

            ],
            label="Pause",
            method="animate"
        )
        return go.layout.Updatemenu(
            buttons=[play_button, pause_button],
            direction="left",
            pad={
                "r": 10,
                "t": 87
            },
            showactive=False,
            type="buttons",
            x=0.1,
            xanchor="right",
            y=0,
            yanchor="top"
        )

    def create_layout(self) -> go.Layout:
        layout = go.Layout(title=self.args.title)
        layout.xaxis.range = (
            self.args.data[self.args.x_axis].min(),
            self.args.data[self.args.x_axis].max()
        )

        if self.args.x_title:
            layout.xaxis.title = self.args.x_title
        else:
            layout.xaxis.title = general.humanize_title(self.args.x_axis)

        if self.args.y_title:
            layout.yaxis.title = self.args.y_title

        layout.hovermode = 'closest'
        layout.updatemenus = (self.create_buttons(),)

        return layout

    def plot(self) -> go.Figure:
        # This data will only be presented on the first load,
        # so we intentionally leave this blank
        data = list()
        frames = list()
        layout = self.create_layout()

        slider_steps: List[go.layout.slider.Step] = list()
        traces: List[str] = list()

        if self.args.trace_columns is None or len(self.args.trace_columns) == 0:
            traces = [
                column
                for column in self.args.data.keys()
                if column != self.args.x_axis
            ]
        elif isinstance(self.args.trace_columns, str):
            traces.append(self.args.trace_columns)
        else:
            traces = [name for name in self.args.trace_columns]

        first_frame = True

        y_max = None
        y_min = None

        for key, group_data in self.args.data.groupby(by=self.args.group):
            print("Creating a trace for " + str(key))
            slider_steps.append(
                go.layout.slider.Step(
                    args=[
                        [str(key)],
                        {
                            "frame": {
                                "duration": 300,
                                "redraw": False
                            },
                            "mode": "immediate",
                            "transition": {
                                "duration": 300
                            }
                        }
                    ],
                    label=str(key).title(),
                    method="animate"
                )
            )

            frame_plots: List[go.Scatter] = list()

            for trace in traces:
                y_values = group_data[trace]

                if y_min is None or y_values.min() < y_min:
                    y_min = y_values.min()

                if y_max is None or y_values.max() > y_max:
                    y_max = y_values.max()

                frame_plots.append(
                    go.Scatter(
                        text=trace,
                        x=group_data[self.args.x_axis],
                        y=group_data[trace]
                    )
                )

            if first_frame:
                first_frame = False
                data = frame_plots

            frame = go.Frame(
                data=frame_plots,
                group=key,
                name=key
            )

            frames.append(frame)

            print("Creating a trace for " + str(key))

        if y_min is not None and y_max is not None:
            layout.yaxis.range = (y_min, y_max)

        print("Creating slider")
        layout.sliders = [
            go.layout.Slider(
                active=0,
                yanchor="top",
                xanchor="left",
                currentvalue=go.layout.slider.Currentvalue(
                    font=go.layout.slider.currentvalue.Font(
                        size=20
                    ),
                    prefix=None,
                    visible=True,
                    xanchor="right"
                ),
                pad={
                    "b": 10,
                    "t": 50
                },
                transition=go.layout.slider.Transition(
                    duration=300,
                    easing='cubic-in-out'
                ),
                len=0.9,
                x=0.1,
                y=0,
                steps=slider_steps
            )
        ]

        print("Creating plot...")
        return go.Figure(
            data=data,
            layout=layout,
            frames=frames
        )
