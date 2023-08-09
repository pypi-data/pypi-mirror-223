from gpioDevice import GPIODevice
from i2cDevice import I2CDevice
from debounce import Debouncer
from device import Device
from pin import InputPin, OutputPin, Pin


# maybe this doesn't make sense. Since we should use callbacks,
# how do we specify a callback function inside a json. It could be the name of
# a external script, but we lose some context
# user can define a local/global vars, then set her to execute external scripts
"""
{
    "i2c-0": {
        "address": 0x20
    },
    "pin":{
        "id":0,
        "debouncer": {
            "updatePeriod": 0,
            "addPeriod": 0,
            "blockSize": 0
        },
        "device": "i2c-0",
        "device": "gpio",
        "device": "sim",
        "mode": "input"
    }
}
"""

class Parser:
    def __init__(self) -> None:
        self.devices = {}
        self.pins = {}

    def getDevice(self, st):  #<i2c,gpio,sim>-<address>
        st = str(st).strip().lower()
        if st not in self.devices.keys(): self.devices[st] = self._createDevice(st)
        return self.devices[st]

    def getDebouncer(self, st):  #<updatePeriod>-<addPeriod>-<blockSize>
        st = str(st).strip().lower()
        values = st.split('-')
        updatePeriod = int(values[0])
        addPeriod = int(values[1])
        blockSize = int(values[2])
        return Debouncer(updatePeriod, addPeriod, blockSize)

    def getPin(self, st):  #<input,output>-<id>,<debouncer>,<device>
        st = str(st).strip().lower()
        if st not in self.pins.keys(): self.pins[st] = self._createPin(st)
        return self.pins[st]

    def _createDevice(self, st):
        if st.startswith("i2c"):
            address = int(st[st.find('-')+1:])
            return I2CDevice(address)
        elif st.startswith("gpio"):
            return GPIODevice()
        elif st.startswith("sim"):
            return Device()


    def _createPin(self, st):
        values = st.split(',')

        debouncer = self.getDebouncer(values[1])
        dev = self.getDevice(values[2])

        mode, id = values[0].split('-')
        id = int(id)

        # TODO: Binary type, it groups some input pins or output pins and give the response on decimal form, but use the pins to binary it
        if mode == 'input': return InputPin(id, debouncer, dev)
        if mode == 'output': return OutputPin(id, debouncer, dev)
        return Pin(id, debouncer, dev)

