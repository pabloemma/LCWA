import matplotlib.pyplot as plt
import numpy as np

nFigures = 4
nRows = 2
nCols = 2

xaxis = np.linspace(0, 10, num=50)

figarr = [None for i in range(nFigures)]
for i in range(nFigures):
  figarr[i] = plt.figure(i+1)
  

  for j in range(nRows*nCols):
    ax = figarr[i].add_subplot(nRows, nCols, j+1)
    ax.plot(xaxis, np.random.rand(50), '.')
    ax.set_title('%d_%d' % (i, j))

plt.show()
