# RadioBackgroundNoiseProfiler
Project to document radio background noise on a regular basis at my house to assess measures to address RFI.

# What's Here

- `run.py`: launch the script with `python3 run.py <configFilename>`
- `NoiseProfiler` module: contains all the required code to use hamlib to sweep frequencies to measure S-level
- `ft818.config`: a config file (JSON) that specifies how to perform the sweep, including what radio to use, what output file, and bands to check.
- `noise_profile.csv`: example output
