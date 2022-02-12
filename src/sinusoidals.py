
import numpy as np



class Sinusoidal:
    def __init__(self , time=[], amp=1 ,freq=1, phase=0):
        self.amplitude = amp
        self.freq = freq
        self.time = time
        self.phase = phase
        self.siusoidals_values = []
        
    
    def makeSinusoidal(self):
        t, a, f, p = self.time, self.amplitude, self.freq, self.phase
        self.siusoidals_values = a*np.sin(2*np.pi*(f*t) + p)


    def getValues(self):
        if not self.time.any(): return []  
        self.makeSinusoidal()
        return self.siusoidals_values

    def getLabel(self):
        return f'{self.amplitude}@{self.freq} HZ + {self.phase}'


        


