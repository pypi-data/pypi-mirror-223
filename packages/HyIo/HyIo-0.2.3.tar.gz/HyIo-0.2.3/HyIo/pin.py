import device


class Pin:
    def __init__(self, id, debouncer, device) -> None:
        self.id = id
        self.debouncer = debouncer
        self.device = device
        self._oldValue = 0

    def setup(self, mode=device.NONE):
        self.device.setup(self.id, mode)

    def _updatePinOnDeviceFunction(self):
        self.device.update(self.id)

    def _setPinOnDeviceFunction(self):
        self.device.set(self.id, self.get())

    def _getFromDeviceFunction(self):
        return self.device.get(self.id)

    def update(self, currentTime):
        currentValue = self.get()
        if currentValue == self._oldValue:
            return False
        self._oldValue = currentValue
        return True

    def get(self):
        return self.debouncer.get()

    def set(self, value):
        pass


class InputPin(Pin):
    def __init__(self, id, debouncer, device) -> None:
        super().__init__(id, debouncer, device)

    def setup(self):
        return super().setup(device.INPUT)

    def update(self, currentTime):
        self.debouncer.updateValueIfNeed(currentTime, self._updatePinOnDeviceFunction)  # function is executed inside
        self.debouncer.addToBufferIfNeed(currentTime, self._getFromDeviceFunction())  # get executed here
        return super().update(currentTime)


class OutputPin(Pin):
    def __init__(self, id, debouncer, device) -> None:
        super().__init__(id, debouncer, device)
        self._lastOutValue = 0

    def setup(self):
        return super().setup(device.OUTPUT)

    def update(self, currentTime):
        self.debouncer.addToBufferIfNeed(currentTime, self._lastOutValue)
        self.debouncer.updateValueIfNeed(currentTime, self._setPinOnDeviceFunction)  # function is executed inside
        return super().update(currentTime)

    def set(self, value):
        self._lastOutValue = value
