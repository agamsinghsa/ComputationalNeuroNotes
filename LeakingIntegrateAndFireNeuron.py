import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import random

class LeakingIntegrateAndFireNeuron:
    def __init__(self, tau=10, threshold=-50, resting_voltage=-70, refractory_period=5):
        self.tau = tau
        self.threshold = threshold
        self.resting_voltage = resting_voltage
        self.potential = self.resting_voltage
        self.refractory_period = refractory_period
        self.refractory_time_remaining = 0
        self.spike_value = 30

    def update_potential(self, input_current, dt=1):
        if self.refractory_time_remaining > 0:
            self.refractory_time_remaining -= dt
            return self.resting_voltage
        else:
            self.potential = self.potential*(1-dt/self.tau) + input_current * dt + self.resting_voltage*( dt/self.tau )
            if self.potential >= self.threshold:
                self.refractory_time_remaining = self.refractory_period
                self.potential = self.resting_voltage
                return self.spike_value
            return self.potential

# Create an instance of the LIF neuron
n = LeakingIntegrateAndFireNeuron()

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax.set_title("Neuron Potential")

x1 = [0]
potentials = [0]
TIME_HORIZON = 100

def animate(i):
    # read value from the slider
    if i < TIME_HORIZON:
        potentials.append(n.update_potential(slider.val))
        x1.append(x1[-1]+1)
    else:
        potentials.append(n.update_potential(slider.val))
        x1.append(x1[-1]+1)
        del x1[0]
        del potentials[0]

    plt.xlim(max(x1[-1]-TIME_HORIZON,0), x1[-1]+3)
    ax.set_ylim(-80, 40)
    ax.clear()
    lines = ax.plot(x1, potentials, scaley=True, scalex=True, color="red")
    slider.ax.set_xlim(1, 8)
    return lines

# create the slider
axslider = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(axslider, 'Input Current', 1, 8, valinit=4.4, valstep=0.1)

anim = FuncAnimation(fig, animate, repeat=False, blit=True, interval=1)
plt.show()
