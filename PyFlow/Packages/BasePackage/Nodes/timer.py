from PyFlow.Core import NodeBase
from Qt.QtCore import QTimer


## Timer node
class timer(NodeBase):
    def __init__(self, name, graph):
        super(timer, self).__init__(name, graph)
        self.out = self.addOutputPin("OUT", 'ExecPin', None, self.compute)
        self.beginPin = self.addInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.addInputPin("Stop", 'ExecPin', None, self.stop)
        self.resetPin = self.addInputPin("Reset", 'ExecPin', None, self.reset)
        self.interval = self.addInputPin("Delta(ms)", 'FloatPin')
        self.interval.setDefaultValue(0.2)
        self._timer = QTimer()
        self._timer.timeout.connect(self.compute)

    def kill(self):
        self._timer.stop()
        self._timer.timeout.disconnect()
        NodeBase.kill(self)

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['FloatPin', 'ExecPin'], 'outputs': ['ExecPin']}

    def reset(self):
        self.stop()
        self.start()

    def stop(self):
        self._timer.stop()

    def start(self):
        dt = self.interval.getData() * 1000.0
        self._timer.start(dt)

    @staticmethod
    def category():
        return 'Utils'

    def compute(self):
        self.out.call()