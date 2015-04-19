#!/usr/bin/env python
# -*- coding: utf-8 -*- 

def plotHeatmapGrid(name, data , title='', x_label='' , y_label='', x_tick_labels=[], y_tick_labels=[], cmap='YlGnBl'):
    #name is the name of the plot
    #data is a 2x2 array normalized [0,1]
    plt.clf()
    fig = plt.figure()
    ax = fig.gca()
    #AXIS
    #ticks and labels in the middle
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_xticks(np.arange(data.shape[1]), minor=False)
    ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ax.set_xticklabels(x_tick_labels, minor=False)
    ax.set_yticklabels(y_tick_labels, minor=False)
    #for table-like display invert axis
    #ax.invert_yaxis()
    #ax.xaxis.tick_top()
    
    #set colorbar
    
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



def plotHeatmap(name, data , x_label='' , y_label='', x_tick_labels=[], y_tick_labels=[]):
    #data is a 2x2 array normalized [0,1]
    plt.clf()
    fig, ax = plt.subplots()
    #delete top and right axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ## put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ## want a more natural, table-like display
    ##ax.invert_yaxis()
    ##ax.xaxis.tick_top()
    ax.set_xticklabels(x_tick_labels, rotation=90, minor=False)
    ax.set_yticklabels(y_tick_labels, minor=False)
    #set colorbar
    
    #heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    heatmap = ax.pcolor(data, cmap=my_cmap, vmin=0, vmax=1)
    cbar = plt.colorbar(heatmap)
    plt.title(name)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot()
    #save plot
    f_format = name.split('.')[-1]
    name = name.split('.')[0]
    plt.savefig(name+'.'+f_format, format=f_format, bbox_inches='tight')
    #plt.show()

def plot_lineas_especies(name, x, t_total, labels=['A','B','C','D']):
    #graficar sum xy para todas las especies
    t = np.linspace(0,t_total+1,t_total+1)
    plot_xy(name, x, t, 'especies_vs_tiempo', labels)
    #diagramas de fase
    for i,j in combinations ([n for n in range(len(x[0]))],2):
        plot_xy(name.split('.')[0] + '_'+labels[i]+labels[j]+'.' + name.split('.')[-1], x[:,i], x[:,j], 'fase_'+labels[i]+labels[j])
        
        
    
def heatmaps_especie_en_tiempo(name,poblacion, n=[], label=['A', 'B', 'C', 'D']):
    ter = '.'+name.split('.')[-1]
    name = name.split('.')[0]
    #graficar heatmap especie en un tiempo dado
    #n debe ser un array
    if type(n) == int: n = [n]
    for i in range(n_especies):
        plotHeatmap(name+label[i]+'_t0'+ter, poblacion[0,:,:,i]) #estado inicial
        plotHeatmap(name+label[i]+'_tf'+ter, poblacion[-1,:,:,i]) #estado final
        for j in n: #grafica vector de tiempos
            plotHeatmap(name+label+'_t'+str(j)+ter, poblacion[j,:,:,i])

def heatmap_tipo(name,tipo,m_milpa=.5,m_intensivo=1):
    for i in range(len(tipo)):
        for j in range(len(tipo[0])):
            if tipo[i][j] == 'b': tipo[i][j] = 1.
            if tipo[i][j] == 'm': tipo[i][j] = 1-m_milpa
            if tipo[i][j] == 'i': tipo[i][j] = 1-m_intensivo
    tipo = np.array(tipo)
    plotHeatmap(name, tipo) #estado inicial    

#CDICT
cdict = {'red':   [(0,.7,.7),(1,0,0)],
         'green': [(0,0,0),(1,1,1)],
         'blue':  [(0,0,0),(1,0,0)]}
RdGn=colors.LinearSegmentedColormap('my_colormap',cdict,256)
 
cdict = {'red':   [(0.0,  1.0, 1.0),(0.01,  0.5, 0.5),(0.5,  0.0, 0.0),(1.0,  0.0, 0.0)],
        'green': [(0.0,  1.0, 1.0),(0.1, 1.0, 1.0),(1.0,  0.0, 0.0)],
        'blue':  [(0.0,  1.0, 1.0),(0.5,  1.0, 1.0),(1.0,  0.5, 0.5)]}
BlCyWt=colors.LinearSegmentedColormap('my_colormap',cdict,256)