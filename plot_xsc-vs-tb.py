#!/bin/env python
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from packaging import version
if version.parse(mpl.__version__) >= version.parse('2.0.0'):
    # Override some of matplotlib 2 new style
    mpl.rcParams['grid.color'] = 'k'
    mpl.rcParams['grid.linestyle'] = 'dotted'
    mpl.rcParams['grid.linewidth'] = 0.5

    mpl.rcParams['figure.figsize'] = [8.0, 6.0]
    mpl.rcParams['figure.dpi'] = 80
    mpl.rcParams['savefig.dpi'] = 100

    mpl.rcParams['font.size'] = 12
    mpl.rcParams['legend.fontsize'] = 'large'
    mpl.rcParams['figure.titlesize'] = 'medium'

    mpl.rcParams['lines.linewidth'] = 1.0
    mpl.rcParams['lines.dashed_pattern'] = [6, 6]
    mpl.rcParams['lines.dashdot_pattern'] = [3, 5, 1, 5]
    mpl.rcParams['lines.dotted_pattern'] = [1, 3]
    mpl.rcParams['lines.scale_dashes'] = False
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json
import cp3_llbb.CommonTools.CMSStyle as CMSStyle
from scipy import interpolate



fig = None
# Load data
theory = {}
with open('sigmaBR_HZA_type-2_MH-500p0_MA-300p00_everytan_a.json') as f:
    params = json.load(f)

x = params['tb']
y = params['sigma']


x = np.asarray(x)
y = np.asarray(y)

fig = plt.figure(figsize=(20,20))
plt.plot(x, y, 'ro')
plt.show()
fig.savefig("sigmaVStanb.png")
