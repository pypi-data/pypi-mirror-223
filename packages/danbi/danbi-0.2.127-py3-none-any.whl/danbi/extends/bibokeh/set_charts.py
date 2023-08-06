import pandas as pd
import numpy as np
import datetime
from typing import List, Tuple, Any, Union

from bokeh.io import output_notebook
from bokeh.resources import INLINE

from bokeh.models import ColumnDataSource, Range1d, LinearAxis, Span
from bokeh.models import HoverTool,WheelZoomTool, PanTool, ResetTool, CrosshairTool, BoxSelectTool, BoxZoomTool, SaveTool
from bokeh.models.formatters import NumeralTickFormatter, DatetimeTickFormatter
from bokeh.plotting import figure


tools = [PanTool(), WheelZoomTool(), ResetTool(), CrosshairTool(), BoxSelectTool(), BoxZoomTool(), SaveTool()]
COLORSET = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#13005A', '#222831', '#3A1078', '#EA8FEA', '#6A2C70', '#5254a3', '#8ca252', '#bd9e39', '#ad494a', '#a55194', '#6baed6', '#fd8d3c', '#74c476', '#9e9ac8', '#969696', '#9c9ede', '#cedb9c', '#e7cb94', '#e7969c', '#de9ed6', '#c6dbef', '#fdd0a2', '#c7e9c0', '#dadaeb', '#d9d9d9', '#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666', '#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae', '#f1e2cc', '#cccccc', '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f']


def setJupyterEnable():
    output_notebook(resources=INLINE)


def getDataSource(df: pd.DataFrame) -> ColumnDataSource:
    return ColumnDataSource(df)


def getFigure(width: int, height: int, title: str):
    try:
        fig = figure(plot_width=width, plot_height=height, title=title, tools=tools, toolbar_location="above")
    except:
        fig = figure(width=width, height=height, title=title, tools=tools, toolbar_location="above")
    
    return fig


def setBokehFigureStyle(fig: figure, tooltips: List = None, formatters: tuple = None, base_plot: Any = None, mode: str = "vline", **options):
    fig.title.text_font_size = options.get("title_font_size", "12pt")
    fig.grid.grid_line_alpha = options.get("grid_line_alpha", 0.5)
    fig.yaxis.formatter = NumeralTickFormatter(format="0,0[.]00")
    fig.xaxis.formatter = DatetimeTickFormatter(years=["%Y-%m-%d"], months=["%Y-%m-%d"], days=["%Y-%m-%d"])

    fig.legend.border_line_alpha = 0
    fig.legend.background_fill_alpha = 0
    fig.legend.padding = options.get("legend_padding", -5)
    fig.legend.spacing = options.get("legend_spacing", -4)
    fig.legend.click_policy = "mute"
    fig.legend.location = options.get("legend_location", "top_left")
    fig.legend.label_text_font_size = options.get("legend_font_size", "9pt")
    
    if tooltips and formatters and base_plot:
        fig.add_tools(HoverTool(
            tooltips=tooltips,
            formatters=formatters,
            mode="vline",
            renderers=[base_plot]
        ))


def setBokehLine(fig: figure, src: Union[ColumnDataSource, pd.DataFrame], x: str, y: str, color: str, width: int = 1.2, legend_label: str = None, alpha: int = 0.7, muted_alpha: int = 0.05, y_ref: int = None, y_range: tuple = None, extra_y_name: str = None, extra_y_range: tuple = None):
    if isinstance(src, pd.DataFrame):
        src = ColumnDataSource(src)
    
    if legend_label is None:
        legend_label = y
    
    if extra_y_name is not None:
        line = fig.line(source=src, x=x, y=y, color=color, line_width=width, legend_label=legend_label, alpha=alpha, muted_alpha=muted_alpha, y_range_name=extra_y_name)
        fig.circle(x=x, y=y, source=src, radius=0, y_range_name=extra_y_name)
        if extra_y_range is not None:
            fig.extra_y_ranges.update({extra_y_name: Range1d(*extra_y_range)})
            fig.add_layout(LinearAxis(y_range_name=extra_y_name), "right")
        if y_ref is not None:
            fig.renderers.extend([Span(location=y_ref, dimension='width', line_color="slategray", line_width=1, y_range_name=extra_y_name)])
    else:
        line = fig.line(source=src, x=x, y=y, color=color, line_width=width, legend_label=legend_label, alpha=alpha, muted_alpha=muted_alpha)
        fig.circle(x=x, y=y, source=src, radius=0)
        if y_ref is not None:
            fig.renderers.extend([Span(location=y_ref, dimension='width', line_color="slategray", line_width=1)])
    if y_range:
        fig.y_range = Range1d(*y_range)
    
    return line


def setBokehMarke(fig: figure, src: Union[ColumnDataSource, pd.DataFrame], x: str, y: str, color: str, size: int = 10, marker: str = "triangle", legend_label: str = None, alpha: int = 0.5, muted_alpha: int = 0.05):
    if isinstance(src, pd.DataFrame):
        src = ColumnDataSource(src)
    
    if legend_label is None:
        legend_label = y
    
    fig.scatter(x=x, y=y, source=src, size=size, color=color, marker=marker, legend_label=legend_label, alpha=alpha, muted_alpha=muted_alpha)
    
    return fig








