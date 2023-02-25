# module that implements the NoiseProfiler instrument
#
#

import Hamlib
from csv import DictWriter
import os, time, decimal

class Radio():
    # setup radio - encapsulate hamlib functionality
    def __init__(self, modelID, device, rate):
        Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_NONE)
        self.rig = Hamlib.Rig(modelID)
        self.rig.set_conf("rig_pathname", device)
        self.rig.set_conf("retry", "5")
        self.rig.state.rigport.parm.serial.rate = rate
        self.rig.open()

    def setFreq(self, f, attOff=True):
        self.rig.set_vfo(Hamlib.RIG_VFO_A)
        self.rig.set_freq(Hamlib.RIG_VFO_A,f*1000*1000)

    #def setAttenuator(self, att):
    #    self.radio.set

    def setMode(self, m):
        self.rig.set_mode(m)

    def getSignalLevel(self):
        return self.rig.get_level_i(Hamlib.RIG_LEVEL_STRENGTH)

class Instrument():
    def __init__(self, config):
        self.config = config
        # setup radio
        self.radio = Radio(config["radio"]["model"], config["radio"]["device"], config["radio"]["rate"])
        # setup output
        fileMode = config["output"]["filemode"]
        fileName = config["output"]["filename"]
        if not os.path.exists(fileName):
            fileMode = 'w'
        self.outFile = open(fileName, fileMode)
        self.outCSV = DictWriter(self.outFile,
                                  fieldnames=self.config["output"]["columns"])
        if fileMode == 'w': # new file, needs  header
            self.outCSV.writeheader()

    def takeMeasurementSet(self):
        """
        loop through all bands, all frequencies
        """
        self.sweepID = time.time()
        print("taking measurement set...")
        for band in self.config["bands"]:
            self.sweepBandMeasurement(band)

    def sweepBandMeasurement(self, bandDict):
        """
        loop through frequences on a given band
        """
        print("sweeping band %s" % bandDict["name"])
        # set mode to CW for consistency
        # TODO: turn off attenuator
        self.radio.setMode(Hamlib.RIG_MODE_CW)
        # sweep freqs
        for freq in self.generateFrequencies(bandDict):
            sigLevel = self.takeMeasurementAtFrequency(freq)
            self.recordMeasurement(sigLevel, bandDict["name"], freq)
            print("measurement at %f: %f" % (freq, sigLevel))

    def generateFrequencies(self, band):
        """
        merge defautls into band dict and compute steps
        """
        settings = dict()
        settings.update(self.config["defaults"])
        settings.update(band)
        
        f = decimal.Decimal(settings["start"])
        end = decimal.Decimal(settings["end"])
        step = decimal.Decimal(settings["step"])
        while f <= end:
            yield float(f)
            f += step

    def takeMeasurementAtFrequency(self, f):
        """
        take one measurement and return signal
        """
        # TODO: implement several measurement methods:
        #   point-averaging : several measuremments at this point
        #   point-min: several measurements and take average
        #   sweep-average: spaced measurements across a small range
        #   sweep-min: take minimum over a sweep
        #   random-average: random over a small range and average
        #   random-min: random over a small range take minimum
        self.radio.setFreq(f)
        # take a bunch of measurements
        # TODO: move measurement loop to band
        measurements = []
        for i in range(self.config["method"]["averaging_samples"]):
            time.sleep(0.1)
            measurements.append(self.radio.getSignalLevel())
        return _sumMethods[self.config["method"]["summarize"]](measurements)

    def recordMeasurement(self, sigLevel, band, freq):
        measureDict = {
            "sweep": self.sweepID,
            "timestamp": time.time(),
            "band_name": band,
            "frequency": freq,
            "signal_level": sigLevel
        }
        self.outCSV.writerow(measureDict)

    def __del__(self):
        self.outFile.close()


_sumMethods = {
  "min": min, "max": max, "aver": lambda x: sum(x)/len(x)
}

