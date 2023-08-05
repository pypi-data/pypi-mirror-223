# coding=utf-8

"""
"""

__author__ = "Morten Lind"
__copyright__ = "Morten Lind, SINTEF Manufacturing 2020"
__credits__ = ["Morten Lind"]
__license__ = "LGPLv3"
__maintainer__ = "Morten Lind"
__email__ = "morten@lind.fairuse.org, morten.lind@sintef.no"
__status__ = "Development"


import numpy as np
import math2d.geometry as m2dg
import matplotlib.pyplot as plt


# Test the dist function

l = m2dg.LineSegment([1, 1], [2, 1])
s = m2dg.LineSegment([0, 1], [1, 3])
print(l.dist(s))

ax = plt.axes()
ax.set_aspect('equal')
ax.plot(*np.transpose((l.start.array, l.end.array)), color='blue', label='l')
ax.plot(*l.start.array, color='blue', marker='o')
ax.plot(*np.transpose((s.start.array, s.end.array)), color='red', label='s')
ax.plot(*s.start.array, color='red', marker='o')
ax.legend()
plt.show(block=False)
