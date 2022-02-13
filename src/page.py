from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from composer import Composer
from sampler import Sampler


class Page(qtw.QTabWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/Page.ui", self)

        self.composer = Composer()
        self.composerLayout.addWidget(self.composer)

        self.sampler = Sampler()
        self.samplerLayout.addWidget(self.sampler)

        self.setCurrentWidget(self.Sampling)
        self.composer.moving_data_to_sampler.connect(self.startSampling)

    def startSampling(self, time, data, fmax):
        self.sampler.original_signal.clear()
        self.sampler.loadSignalFromComposer(time, data, fmax)
        self.sampler.loaded = True
        self.setCurrentWidget(self.Sampling)
