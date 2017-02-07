import snappy
import cmath
import fractions
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np


manifoldList = [
	#cusp area <5.24
	'm125', 'm129', 's596',

	# 's774',	's782',	's785', 'v2124', 'v2355',

	'v3211', 'v3376'
]

# manifoldName = 'm129'
cuspNum = 0
r = 8

def reformatNumber ( snappyNumber ):
	imag = float(snappyNumber.imag())
	real = float(snappyNumber.real())
	return real + imag*1j

def coprimes (s, xTranslation, yTranslation):
	pairs= [[1,0],[0,1]]
	for a in range(1,s+1): 
		for b in range(1,s+1): 
			if fractions.gcd(a,b)==1:
				pairs.append([a,b])
				pairs.append([-a,b])
	return sorted(pairs, key = lambda x: float(abs( x[1]*xTranslation + x[0]*yTranslation)))

def getData (manifoldName, cuspNum):
	points = [[],[],[],[]]
	M = snappy.Manifold(manifoldName)
	C = M.cusp_neighborhood()
	C.set_displacement(100,cuspNum)
	xTranslation = reformatNumber(C.all_translations()[cuspNum][1])
	yTranslation = reformatNumber(C.all_translations()[cuspNum][0])
	for [i,j] in coprimes(r , xTranslation, yTranslation):
		points[3].append(str((i,j)))
		M = snappy.Manifold(manifoldName)
		M.dehn_fill((i,j),cuspNum)
		if M.volume() > 0.9:
			try:
				C = M.cusp_neighborhood()
				C.set_displacement(100)
				xTranslation = reformatNumber(C.all_translations()[0][1])
				yTranslation = reformatNumber(C.all_translations()[0][0])
				points[0].append(abs(xTranslation))
				points[1].append(yTranslation.imag)
				mVolume = abs(reformatNumber(M.volume()))
				cVolume = abs(reformatNumber(C.volume()))
				points[2].append(cVolume/ mVolume)
			except:
				print 'Construction of ' + str(manifoldName) + str((i,j)) + ' cusp failed.'
				pass
	return points

def generateSurface():
	sParam = np.linspace(1.9, 3.8, 100)
	tParam = np.linspace(.35, .9, 100)
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



allThePoints = dict([])
data = []

# data.append(surface)




for manifoldName in manifoldList:
	thisManifold = getData(manifoldName, cuspNum)
	allThePoints.update({manifoldName: thisManifold})


for manifoldName in manifoldList:
	x, y, z, surgery = allThePoints[manifoldName]
	thisManifoldsPoints = go.Scatter3d(
	    x=x,
	    y=y,
	    z=z,
	    text = surgery,
	    name = manifoldName,
	    mode='markers',
	    marker=dict(
	        size=4,
	        line=dict(
	            color='rgba(217, 217, 217, 0.14)',
	            width=0.1
	        ),
	        opacity=0.8
	    )
	)
	data.append(thisManifoldsPoints)

data.append(generateSurface())


layout = go.Layout(
    scene=go.Scene(
        xaxis=go.XAxis(title='m'),
        yaxis=go.YAxis(title='imag(n)'),
        zaxis=go.ZAxis(title='cVol/mVol')
    )
)



fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='manifoldTest2.html')

