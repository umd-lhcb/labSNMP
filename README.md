# Compile a MIB file to a Python file
```
mibdump.py --mib-source . --mib-source http://mibs.snmplabs.com/asn1/@mib@ --destination-directory . <mib_filename>
```

# Control the Tripp Lite power supply
## Some interesting commands
```
tlpDeviceNumDevices
tlpPduCircuitTotalCurrent
tlpPduControlRamp
```

## To control all channels
Set state (an integer) to `tlpPduDeviceMainLoadCommand.1`

## To control a single change
Set state (an integer) to `tlpPduOutletCommand.1.x`.
In our power supply, we have a total of 14 channels.
