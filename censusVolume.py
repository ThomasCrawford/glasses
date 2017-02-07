import snappy
import cmath
import fractions
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
import time
start_time = time.time()


howMany = 4815
# howMany = 200

cuspNum = 0

points = [[],[],[],[]]


def reformatNumber ( snappyNumber ):
	imag = float(snappyNumber.imag())
	real = float(snappyNumber.real())
	return real + imag*1j

def getData():
	for M in snappy.OrientableCuspedCensus[0:howMany]:
		C=M.cusp_neighborhood()
		C.set_displacement(100)
		xTranslation = reformatNumber(C.all_translations()[cuspNum][1])
		yTranslation = reformatNumber(C.all_translations()[cuspNum][0])
		volume = abs(reformatNumber(M.volume()))
		name = M.identify()[0]
		points[0].append(abs(xTranslation))
		points[1].append(yTranslation.imag)
		points[2].append(volume)
		points[3].append(str(name))

def generateSurface():
	#x values
	sParam = np.linspace(1.9, 3.8, 100)
	#z values
	tParam = np.linspace(2.2, 5, 100)
	tGrid, sGrid = np.meshgrid(sParam, tParam)
	# rParam = np.linspace(2, 4.5, 100)
	# qParam = np.linspace(2, 4.5, 100)
	x = tGrid
	y = 5.24/tGrid
	z = sGrid

	surface = go.Surface(x=x, y=y, z=z, 
	    opacity = .999999999999999, 
	    # colorscale = 'rgb(0, 0, 100)',
	    colorscale= [[0, 'rgb(0, 0, 255)'],[1, 'rgb(0, 0, 255)']],
	    showscale = False
	)
	return surface

getData()


data = []


x, y, z, name = points
scatterData = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    text = name,
    mode='markers',
    marker=dict(
        color=range(len(x)),                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
		colorbar=go.ColorBar(title='index'),
        size=4,
        line=dict(
            color='rgba(217, 217, 217, 0.14)',
            width=0.02
        ),
        opacity=0.3
    )
)

data.append(scatterData)
data.append(generateSurface())

layout = go.Layout(
    scene=go.Scene(
        xaxis=go.XAxis(title='m'),
        yaxis=go.YAxis(title='imag(n)'),
        zaxis=go.ZAxis(title='mVolume')
    )
)



print("--- %s seconds ---" % (time.time() - start_time))


fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='censusMVolume.html')


