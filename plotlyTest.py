import plotly.offline as py
import plotly.graph_objs as go

import numpy as np

s = np.linspace(0, 1, 100)
t = np.linspace(0, 1, 100)
tGrid, sGrid = np.meshgrid(s, t)
x = tGrid
y = 5.24/tGrid
z = sGrid
surface = go.Surface(x=x, y=y, z = z, 
    opacity = 0.9, 
    # colorscale= [[0, 'rgb(0, 0, 80)'],[1, 'rgb(0, 0, 80)']],
    showscale = False
)
data = [surface]



fig = go.Figure(data=data, layout = layout)



py.plot(
    fig, 
    filename = 'Parametric_plot.html'
    )

# py.iplot(fig, filename='Parametric_plot')
