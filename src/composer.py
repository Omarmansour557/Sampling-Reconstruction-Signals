from math import sin
import random
import string
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from sinusoidals import Sinusoidal
import pyqtgraph as pg
import numpy as np


class Composer(qtw.QWidget):
    moving_data_to_sampler = qtc.pyqtSignal(list, list, float)

    def __init__(self):
        super().__init__()
        self.time = np.linspace(0, 3, 1000)
        self.saved_example = []
        self.list_of_sinusoidals = []
        self.array_of_lines = []
        uic.loadUi("src/ui/Composer.ui", self)

        self.component_graph = pg.PlotWidget()
        self.component_graph.setXRange(-0.2, 3)

        self.composing_graph = pg.PlotWidget()
        self.composing_graph.setXRange(-0.2, 3)

        self.SignalComponents.addWidget(self.component_graph)
        self.ComposingSignal.addWidget(self.composing_graph)

        self.AddWaveBtn.clicked.connect(self.addSinWave)
        self.DeleteButton.clicked.connect(self.deleteSinWave)
        self.SaveExampleButton.clicked.connect(self.saveExample)
        self.StartSamplingButton.clicked.connect(self.startSampling)

    def saveExample(self):
        self.saved_example.append(self.composed_value)
        self.SavedExList.addItem(f'Example: {len(self.saved_example)}')

    def startSampling(self):
        if(self.SavedExList.count() > 0):
            index_of_example = self.SavedExList.currentIndex()
            current_composed_signal = self.saved_example[index_of_example]
            fmax = self.getFmax(self.time, current_composed_signal)
            self.moving_data_to_sampler.emit(
                                self.time.tolist(), current_composed_signal.tolist(), fmax)

    def getFmax(self, time, data):
        amplitude = np.fft.rfft(data)
        frequency = np.fft.rfftfreq(len(data), (time[1] - time[0]))

        fmax = 0
        for i, a in enumerate(amplitude):
            if np.abs(a) > 5:  # (1)
                fmax = frequency[i]
        return fmax

    def addSinWave(self):
        amp = self.AmplitudeSpinBox.value()
        freq = self.FreqSpinBox.value()
        phase = self.PhaseSpinBox.value()
        self.sinusoidals = Sinusoidal(self.time, amp, freq, phase)
        self.list_of_sinusoidals.append(self.sinusoidals)

        self.sine_values = self.sinusoidals.getValues()
        self.label = self.sinusoidals.getLabel()
        self.ComponentsList.addItem(self.label)

        self.plot(self.time, self.sine_values, self.label)

        self.composed_value = self.composedSignal()

        pen = pg.mkPen(color='y')
        self.composing_graph.addLegend()
        self.composing_graph.plot(
            self.time, self.composed_value, name='composed_signal', pen=pen)

    def composedSignal(self):
        self.composing_graph.clear()
        self.sin_waves_values = [sinusoidal.getValues()
                                 for sinusoidal in self.list_of_sinusoidals]
        self.composed_value = np.sum(self.sin_waves_values, axis=0)

        return self.composed_value

    def plot(self, x, y, plotname):
        color = list(np.random.choice(range(256), size=3))
        pen = pg.mkPen(color=(color[0], color[1], color[2]))
        self.component_graph.addLegend()
        self.component_graph.plot(x, y, name=plotname, pen=pen)

    def deleteSinWave(self):
        if len(self.list_of_sinusoidals) > 1:
            self.sine_wave_index = self.ComponentsList.currentIndex()
            self.ComponentsList.removeItem(self.sine_wave_index)
            self.list_of_sinusoidals.pop(self.sine_wave_index)
            self.updateSignalComponents(self.list_of_sinusoidals)
            self.updateComposedGraph(self.sine_wave_index)
            if len(self.list_of_sinusoidals) == 0:
                self.clearCanvas()
        elif len(self.list_of_sinusoidals) == 1:
            self.ComponentsList.removeItem(self.sine_wave_index)
            self.clearCanvas()
            self.list_of_sinusoidals.pop(self.sine_wave_index)

        else:
            self.clearCanvas()

    def updateSignalComponents(self, list_of_sinusoidals):
        self.component_graph.clear()

        for sinusoidal in self.list_of_sinusoidals:
            self.plot(self.time, sinusoidal.getValues(), sinusoidal.getLabel())

    def updateComposedGraph(self, index):
        self.composing_graph.clear()
        self.sin_waves_values = [sinusoidal.getValues()
                                 for sinusoidal in self.list_of_sinusoidals]
        self.composed_value = np.sum(self.sin_waves_values, axis=0)

        pen = pg.mkPen(color='y')
        self.composing_graph.addLegend()

        self.composing_graph.plot(
            self.time, self.composed_value, name='composed_signal', pen=pen)

    def clearCanvas(self):
        self.composing_graph.clear()
        self.component_graph.clear()
