import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def generateGraphs(data, title, xlabel, ylabel, fileName,min,max):
    Figure(figsize = (7,7),dpi = 100)
    y = data
    mu, std = norm.fit(y)
    fig = plt.figure(figsize=(9.5,6.5))
    plt.title(title, fontdict={'fontsize':20})
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel, fontsize=16)
    plt.yticks([])
    plt.hist(y, bins=5, density=True, alpha=0)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    plt.axvline(int(float(min)))
    plt.axvline(int(float(max)))
    plt.savefig(fileName)
