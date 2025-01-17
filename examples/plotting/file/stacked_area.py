''' A stacked area plot using data from a pandas DataFrame.

.. bokeh-example-metadata::
    :apis: bokeh.plotting.Figure.varea_stack
    :refs: :ref:`userguide_plotting` > :ref:`userguide_plotting_directed_areas`
    :keywords: area, pandas, stacked

'''
import numpy as np
import pandas as pd

from bokeh.palettes import brewer
from bokeh.plotting import figure, show

N = 10
df = pd.DataFrame(np.random.randint(10, 100, size=(15, N))).add_prefix('y')

p = figure(x_range=(0, len(df)-1), y_range=(0, 800))
p.grid.minor_grid_line_color = '#eeeeee'

names = [f"y{i}" for i in range(N)]
p.varea_stack(stackers=names, x='index', color=brewer['Spectral'][N], legend_label=names, source=df)

# reverse the legend entries to match the stacked order
p.legend.items.reverse()

show(p)
