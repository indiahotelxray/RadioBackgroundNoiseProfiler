# module that implements the NoiseProfiler instrument
#
#

import Hamlib
from csv import DictWriter
import time, decimal

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
        self.outFile = open(config["output"]["filename"], config["output"]["filemode"])
        self.outCSV = DictWriter(self.outFile,
                                  fieldnames=self.config["output"]["columns"])


    def takeMeasurementSet(self):
        """
        loop through all bands, all frequencies
        """
        self.sweepID = time.ctime()
        print("taking measurement set...")
        for band in self.config["bands"]:
            self.sweepBandMeasurement(band)

    def sweepBandMeasurement(self, bandDict):
        """
        loop through frequences on a given band
        """
        print("sweeping band %s" % bandDict["name"])
        # sweep freqs
        for freq in self.generateFrequencySet(bandDict):
            sigLevel = self.takeMeasurementAtFrequency(freq)
            self.recordMeasurement(sigLevel, bandDict["name"], freq)
            print("measurement at %f: %f" % (freq, sigLevel))

    def generateFrequencySet(self, band):
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
        # TODO remove use of default averaging samples here for band value.
        measurements = []
        for i in range(self.config["defaults"]["averaging_samples"]):
            time.sleep(0.1)
            measurements.append(self.radio.getSignalLevel())
        # compute average
        return sum(measurements) / len(measurements)

    def recordMeasurement(self, sigLevel, band, freq):
        measureDict = {
            "sweep": self.sweepID,
            "timestamp": time.ctime(),
            "band_name": band,
            "frequency": freq,
            "signal_level": sigLevel
        }
        self.outCSV.writerow(measureDict)

    def __del__(self):
        self.outFile.close()

