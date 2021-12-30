# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 11:38:54 2021

@author: jnwag
"""

import matplotlib.pyplot as plt

year = [1950, 1970, 1990, 2010]
pop = [2.519, 3.692, 5.263, 6.972]
plt.plot(year,pop)
plt.show()

plt.scatter(year,pop)
plt.show()