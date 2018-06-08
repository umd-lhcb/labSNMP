# labSNMP
## Prerequisites
Tested with `Python 2.7.13`.
If only the command line control is need, use `pip` to install `pysnmp`.

## Compile a MIB file to a Python file
Suppose both your source ANSI MIB file and target output director are `.`:
```
mibdump.py --mib-source . --mib-source http://mibs.snmplabs.com/asn1/@mib@ --destination-directory . <mib_filename>
```

## Control the Tripp Lite power supply
It has a total of 14 channels.

### To control all channels
Set state (an integer) to `tlpPduDeviceMainLoadCommand.1`

### To control a single channel
Set state (an integer) to `tlpPduOutletCommand.1.x`.

### Some interesting commands
```
tlpDeviceNumDevices
tlpPduCircuitTotalCurrent
tlpPduControlRamp
```

## Control the Wiener crate
It has a total of 12 output channels.

### To control a single channel
Set state (an integer) to `outputSwitch.x`.

### Some interesting commands
```
outputSwitch
outputVoltage
outputCurrent
outputSupervisionBehavior
```
