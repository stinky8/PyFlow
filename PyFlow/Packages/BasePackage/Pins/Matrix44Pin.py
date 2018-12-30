from pyrr import Matrix44

from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class Matrix44Pin(PinBase):
    """doc string for Matrix44Pin"""
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(Matrix44Pin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(Matrix44())

    def color(self):
        return (150, 0, 20, 255)

    def supportedDataTypes(self):
        return ('Matrix44Pin',)

    @staticmethod
    def pinDataTypeHint():
        return 'Matrix44Pin', Matrix44()

    def serialize(self):
        data = PinBase.serialize(self)
        m = self.currentData()
        data['value'] = [m.c1.tolist(), m.c2.tolist(), m.c3.tolist(), m.c4.tolist()]
        return data

    def setData(self, data):
        if isinstance(data, Matrix44):
            self._data = data
        elif isinstance(data, list) and len(data) == 4:
            self._data = Matrix44([data[0], data[1], data[2], data[3]])
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, self._data)