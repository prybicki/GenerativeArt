import math
import sys

import dearpygui.dearpygui as dpg
from itertools import islice


def logistic(r: float, x: float = 0.5):
    i = 0
    seen = set()
    while True:
        yield i, x, x not in seen
        seen.add(x)
        x = r * x * (1 - x)
        i += 1


def make_plot_theme(plot_type, color, marker_type, marker_size):
    """
    :param plot_type: e.g. mvScatterSeries
    :param color: 3-tuple
    :param marker_type: e.g. mvPlotMarker_Asterisk
    :return: tag
    """
    with dpg.theme() as theme:
        with dpg.theme_component(plot_type):
            # This does not work with legend...
            # dpg.add_theme_color(dpg.mvPlotCol_Line, color, category=dpg.mvThemeCat_Plots)
            # dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, marker_type, category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, marker_size, category=dpg.mvThemeCat_Plots)
    return theme


def update(tag):
    r = dpg.get_value(r_slider)
    i = dpg.get_value(i_slider)
    ys = list(islice(logistic(r), 0, i))
    ys_repeating = []
    xs_repeating = []
    ys_unique = []
    xs_unique = []
    for x, y, u in ys:
        xs_unique.append(x) if u else xs_repeating.append(x)
        ys_unique.append(y) if u else ys_repeating.append(y)
    dpg.set_value(unique, [xs_unique, ys_unique])
    dpg.set_value(repeating, [xs_repeating, ys_repeating])
    dpg.set_axis_limits(x_axis, 0, len(ys))


dpg.create_context()
dpg.create_viewport(title='Iteration of the logistic equation - interactive chart')
dpg.setup_dearpygui()

with dpg.window(tag='main_window') as window:
    i_slider = dpg.add_slider_int(default_value=1000, min_value=1, max_value=10000, width=-100, label='Iterations', callback=update)
    r_slider = dpg.add_slider_double(format='%.15f', default_value=3.80102, min_value=0, max_value=4.0 - sys.float_info.epsilon, width=-100, label='R parameter', callback=update)

    with dpg.plot(width=-1, height=-1) as plot:
        dpg.add_plot_legend()
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label='Index')
        with dpg.plot_axis(dpg.mvXAxis, label='Value') as y_axis:
            unique = dpg.add_scatter_series(label='Unique values', x=[], y=[])
            repeating = dpg.add_scatter_series(label='Repeating values', x=[], y=[])
        dpg.set_axis_limits(y_axis, 0, 1)
        dpg.bind_item_theme(plot, make_plot_theme(dpg.mvScatterSeries, (224, 224, 0), dpg.mvPlotMarker_Asterisk, 3))
        dpg.bind_item_theme(plot, make_plot_theme(dpg.mvScatterSeries, (0, 0, 224), dpg.mvPlotMarker_Asterisk, 3))


update(None)
dpg.set_primary_window('main_window', True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
