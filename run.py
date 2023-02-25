#!/usr/bin/python3

from NoiseProfiler.Hardware import Instrument
import sys, json

with open(sys.argv[1], 'r') as cf:
    config = json.loads(cf.read())

myInstrument = Instrument(config)

myInstrument.takeMeasurementSet()
