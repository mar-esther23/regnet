import sys, copy, random
import numpy as np
from itertools import combinations, product
from scipy.integrate import odeint
from scipy.signal import convolve2d
from matplotlib import pyplot as plt
from matplotlib import colorbar as cbar
from matplotlib import colors as colors


def plotHeatmap(name, data , x_label='' , y_label='', x_tick_labels=[], y_tick_labels=[]):
    #data is a 2x2 array normalized [0,1]
    plt.clf()
    fig = plt.figure()
    ax = fig.gca()
    #delete top and right axis
    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ## put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(data.shape[1]), minor=False)
    ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ## want a more natural, table-like display
    ##ax.invert_yaxis()
    ##ax.xaxis.tick_top()
    ax.set_xticklabels(x_tick_labels, minor=False)
    ax.set_yticklabels(y_tick_labels, minor=False)
    #set colorbar
    cdict = {'red':   [(0,.7,.7),(1,0,0)],
             'green': [(0,0,0),(1,1,1)],
             'blue':  [(0,0,0),(1,0,0)]}
    my_cmap=colors.LinearSegmentedColormap('my_colormap',cdict,256)
    #heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    heatmap = ax.pcolor(data, cmap=my_cmap, vmin=0, vmax=1,edgecolors='k', lw=.25)
    cbar = plt.colorbar(heatmap)
    plt.title(name)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot()
    #grid to separeate states
    grid = ['-','-','None']
    for i in range(len(grid)):
        plt.axvline(x=i+1, lw=2, ls=grid[i], color='k')
    
    
    #save plot
    f_format = name.split('.')[-1]
    name = name.split('.')[0]
    plt.savefig(name+'.'+f_format, format=f_format, bbox_inches='tight')
    #plt.show()

attr =  [(0,0,0),
        (0,0,1),
        (1,0,1),
        (1,1,0),]
attr = np.array(attr)
attr = np.transpose(attr)
print attr

plotHeatmap('prueba.png', attr , x_label='tipo' , y_label='nodo', x_tick_labels=[0,1,5,6], y_tick_labels=['a','b','c'])