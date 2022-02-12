from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import pyqtgraph as pg
import utils
from scipy import signal
import numpy as np

class Sampler(qtw.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/Sampler.ui", self)
        self.original_signal = pg.PlotWidget()
        self.SamplerLayout.addWidget(self.original_signal)
        self.reconstruct_signal = pg.PlotWidget()
        self.ReconstructLayout.addWidget(self.reconstruct_signal)        
        
        self.flag = True

        self.ToggleVisibilityBtn.clicked.connect(self.toggleVisibility) 
        self.LoadButton.clicked.connect(self.loadSignal)
        self.SamplingSlider.valueChanged.connect(self.updateReconstruction)

        self.fmax = 0
        self.sampling_values = []
        self.time_interval = 0
        self.analog_time = []
        self.orignal_signal = []
        self.recovered_signal = []
        self.loaded = False
        self.SamplingAutomatic.clicked.connect(self.startSamplingAutomatic)

    def updateReconstruction(self):
        self.factor = self.SamplingSlider.value()/10
        self.sampling_frequency = self.factor * self.fmax
        self.SliderLabel.setText(f'{self.factor} fmax')
        self.reconstructSignal(self.orignal_signal, self.analog_time, self.sampling_frequency) 

    def startSamplingAutomatic(self):
        if(self.loaded):
            self.SamplingSlider.setValue(0)
            self.timer = qtc.QTimer()
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.autoSample)
            self.timer.start()

    def autoSample(self):
        if (self.SamplingSlider.value() == 30):
            self.timer.stop()

        else:
            count = self.SamplingSlider.value()+1
            self.SamplingSlider.setValue(count)









    def reconstructSignal(self, orignal_signal, analog_time, sampling_frequency):
        if self.loaded:
            sampling_time, sampling_values = self.sample(
                orignal_signal, analog_time, sampling_frequency)
        if(len(sampling_values)>0):
            self.resampled_original_signal = signal.resample(sampling_values, len(self.analog_time))
            self.clearCanvas()
            self.plotAllSignals(self.resampled_original_signal, sampling_time, sampling_values, self.analog_time, self.orignal_signal )



    def sample(self, orignal_signal, analog_time, sampling_frequency):
        time_interval = analog_time[-1]
        number_of_samples = int(np.floor(sampling_frequency * time_interval))
        if(number_of_samples):
            sampling_time = np.arange(0, time_interval, 1/sampling_frequency)
            sampling_values = [orignal_signal[np.searchsorted(analog_time, t)]for t in sampling_time]
            return (sampling_time, sampling_values)
        else:
            ([], [])    







    def toggleVisibility(self):
        self.flag = self.flag^True
        print(self.flag)
        if(not self.flag):
            self.reconstruct_signal.hide()
        else:
            self.reconstruct_signal.show()
            # self.reconstruct_signal.resize(300, 300)
            
            
            
        
    def loadSignal(self):
        self.loaded, name, (self.analog_time, self.orignal_signal) = utils.open_csv(self) 
        if self.loaded:
            self.time_interval = self.analog_time[-1]
            self.plot(self.analog_time, self.orignal_signal)
            self.fmax = self.getFmax(self.analog_time, self.orignal_signal)
            self.fmaxLCD.display(self.fmax)

    def loadSignalFromComposer(self, time, data, fmax):
        self.analog_time = time
        self.orignal_signal = data
        self.fmax = fmax
        self.plot(self.analog_time, self.orignal_signal)
        self.fmaxLCD.display(self.fmax)



    def plot(self, x, y):
        
        pen = pg.mkPen(color='r')
        self.original_signal.plot(x, y,pen=pen)        
            

    def clearCanvas(self):
        self.reconstruct_signal.clear()
        self.original_signal.clear()
        

    def plotAllSignals(self, resampled_original_signal, sampling_time, sampling_values, analog_time, orignal_signal ):
        pen1 = pg.mkPen(color='r')
        self.reconstruct_signal.plot(analog_time, resampled_original_signal,name ='omar' , pen=pen1)
        self.plot(analog_time, orignal_signal  )
        pen3 = pg.mkPen(color='g', style=qtc.Qt.DashLine)
        self.original_signal.plot(sampling_time, sampling_values, name='abosaied' ,pen=pen3, symbol ='o',symbolSize=6)



    def getFmax(self, time, data):
        amplitude = np.fft.rfft(data)
        frequency = np.fft.rfftfreq(len(data), (time[1] - time[0]))

        fmax=0
        for i, a in enumerate(amplitude):
            if np.abs(a) > 5 : # (1)
                fmax = frequency[i]
        return fmax