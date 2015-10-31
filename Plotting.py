# Name: Seline, Li, Taylor, Son
# Leap Motion project

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import time

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = Axes3D(fig)
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot(x, y, z, label='parametric curve')
ax.legend()

plt.ion()
plt.show()

for ii in xrange(0,360,1):
    
    ax.view_init(elev=10, azim=ii)
    plt.draw()
    print "drawn? " + str(ii)
    time.sleep(0.01)
