# For controlling the Tripp Lite power supply
## First available command
`tlpDeviceNumDevices`

## Some interesting commands
`tlpPduCircuitTotalCurrent`
`tlpPduControlRamp`

## To control all channels
Set state (an integer) to `tlpPduDeviceMainLoadCommand.1`

## To control a single change
Set state (an integer) to `tlpPduOutletCommand.1.x`.
In our power supply, we have a total of 14 channels.
