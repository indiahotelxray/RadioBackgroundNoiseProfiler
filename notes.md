

## Documention:
# Hamlib Example
Python Example provded by Hamlib [ "py3test.py"](https://github.com/Hamlib/Hamlib/blob/master/bindings/py3test.py)

Another repo on github, shows how to set bitrate; Hamlib default does not work for FT818: [WebHam](https://github.com/ub3app/WebHam/blob/fecd73456dbe8457bbbb85d1143872308a3d005d/package/webham.py)

# Don't use the S-Meter
The Hamlib Doucmentations points me to [this page](http://www.seed-solutions.com/gregordy/Amateur%20Radio/Experimentation/SMeterBlues.htm) that discusses the unreliabiltiy of the S-meter.  I am looking to spot relative differences over time with the same equipment, _and_ want to see noise received at my radio by all paths, rather than some hypothetical measurement with an SWR.  Thus I should probably perform tests with the same configuration repeatedly over a short interval, but long enough for the radio and power supply to literally warm up to see if that makes much of an impact.
