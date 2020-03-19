import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod # for later

def derive(y,t,N, beta, gamma):        
    """The SIR model differential equations."""

    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I 
    dRdt = gamma * I
    return dSdt, dIdt, dRdt
    
class SIR:
    
    def __init__(self, N=1000, I0=1, R0=0, beta=0.4, gamma=1./10, days=250):
        """Setup for the model.
        
        N:     Total population, N.
        I0,R0: Initial number of infected and recovered individuals.
        beta:  Contact rate, beta, 
        gamma: Mean recovery rate,(in 1/days).
        t:     A grid of time points (in days)
        """
        
        self.N  = N
        self.I0 = I0
        self.R0 = R0
        self.S = 0
        self.I = 0
        self.R = 0
        self.beta = beta
        self.gamma = gamma
        self.t = np.linspace(0, days, days) 
    
    def projection(self):
        """Expected change in the disease's distribution in the population. """
        
        S0 = self.N - self.I0 - self.R0 # Everyone else, S0, is susceptible to infection initially.
        # Initial conditions vector
        y0 = S0, self.I0, self.R0
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(derive, y0, self.t, args=(self.N, self.beta, self.gamma))
        self.S, self.I, self.R = ret.T

    def plot_projection(self):
        """Plot the data on three separate curves for S(t), I(t) and R(t)"""
        
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        ax.plot(self.t, self.S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(self.t, self.I/1000, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(self.t, self.R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number (1000s)')
        ax.set_ylim(0,1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.show()
        
class City(SIR):
    
    def __init__(self, name, position, area, air, port):
        super().__init__()
        self.name = name
        self.position = position
        self.area = area
        self.air = air
        self.port = port
    
    def get_name(self):
        return self.name
    
    def get_position(self):
        return self.position