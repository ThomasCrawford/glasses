#Depricated

import snappy
import cmath
import fractions
import plotly.plotly as py
import plotly.graph_objs as go


manifoldList = [
	#cusp area <5.24
	'm125', 'm129', 's596',		's774',	's782',	's785',
	'v2124', 'v2355', 'v3211', 'v3376'
]

# manifoldName = 'm129'
cuspNum = 0
r = 6

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
	points = [[],[],[]]
	M = snappy.Manifold(manifoldName)
	C = M.cusp_neighborhood()
	C.set_displacement(100,cuspNum)
	xTranslation = reformatNumber(C.all_translations()[cuspNum][1])
	yTranslation = reformatNumber(C.all_translations()[cuspNum][0])
	for [i,j] in coprimes(r , xTranslation, yTranslation):
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
				if len(C.horoballs(.9)) == 2:
					gDistance = C.horoballs(.9)[0]['center'] - C.horoballs(.9)[1]['center']
					points[2].append(abs(gDistance))
				elif len(C.horoballs(.9)) == 4:
					#Still need to address this case
					gDistance = C.horoballs(.9)[0]['center'] - C.horoballs(.9)[1]['center']
					points[2].append(0)
				else: 
					print str((i,j)) + ' has ' + str(len(C.horoballs(.9))) + ' full sized horoballs ?!?!'
					points[2].append(0)
			except:
				print 'Construction of ' + str(manifoldName) + str((i,j)) + ' cusp failed.'
				pass
	return points


allThePoints = dict([])
data = []

for manifoldName in manifoldList:
	thisManifold = getData(manifoldName, cuspNum)
	allThePoints.update({manifoldName: thisManifold})


for manifoldName in manifoldList:
	x, y, z = allThePoints[manifoldName]
	alpha = go.Scatter3d(
	    x=x,
	    y=y,
	    z=z,
	    mode='markers',
	    marker=dict(
	        size=6,
	        line=dict(
	            color='rgba(217, 217, 217, 0.14)',
	            width=0.5
	        ),
	        opacity=0.8
	    )
	)
	data.append(alpha)

# trace1 = go.Scatter3d(
#     x=x,
#     y=y,
#     z=z,
#     mode='markers',
#     marker=dict(
#         size=6,
#         line=dict(
#             color='rgba(217, 217, 217, 0.14)',
#             width=0.5
#         ),
#         opacity=0.8
#     )
# )





layout = go.Layout(
    scene=go.Scene(
        xaxis=go.XAxis(title='m'),
        yaxis=go.YAxis(title='imag(n)'),
        zaxis=go.ZAxis(title='abs(g)')
    )
)


fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='manifoldTest1')

