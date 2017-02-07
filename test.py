import copy
import json
import math
import plotly.offline as py
from plotly import tools
import urllib2

# data related to the ring cyclide is loaded

response = urllib2.urlopen('https://plot.ly/~empet/2381.json')
data_file = response.read()
fig = json.loads(data_file)

# data related to the ring cyclide is loaded


data_original = fig['data'][0]     # this will be trace0

data = copy.deepcopy(fig['data'])[0]        # trace1

lx = len(data['z'])
ly = len(data['z'][0])

out = []


def dist_origin(x, y, z):

    return math.sqrt((1.0 * x)**2 + (1.0 * y)**2 + (1.0 * z)**2)

for i in xrange(lx):
    temp = []
    for j in xrange(ly):
        temp.append(
            dist_origin(data['x'][i][j], data['y'][i][j], data['z'][i][j]))
    out.append(temp)

data['surfacecolor'] = out     # sets surface-color to distance from the origin

# This section deals with the layout of the plot

scene = dict(
    cameraposition=[[0.2, 0.5, 0.5, 0.2], [0, 0, 0], 4.8]
)

fig = tools.make_subplots(rows=1, cols=2,
                          specs=[[{'is_3d': True}, {'is_3d': True}]])

# adding surfaces to subplots.
data_original['scene'] = 'scene1'
data_original['colorbar'] = dict(x=-0.07)

data['scene'] = 'scene2'
fig.append_trace(data_original, 1, 1)
fig.append_trace(data, 1, 2)


fig['layout'].update(title='Ring Cyclide',
                     height=800, width=950)
fig['layout']['scene1'].update(scene)
fig['layout']['scene2'].update(scene)
fig['layout']['annotations'] = [
    dict(
        x=0.1859205,
        y=0.95,       # 0.9395833,
        xref='x',
        yref='y',
        text='4th Dim Prop. to z',
        showarrow=False
    ),
    dict(
        x=0.858,
        y=0.95,
        xref='x',
        yref='y',
        text='4th Dim Prop. to Distance from Origin',
        showarrow=False
    )
]
py.plot(fig, filename='surface-coloring')



