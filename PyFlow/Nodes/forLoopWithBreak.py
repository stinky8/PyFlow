from Core.AbstractGraph import *
from Core.Settings import *
from Core import Node


class forLoopWithBreak(Node, NodeBase):
    def __init__(self, name, graph):
        super(forLoopWithBreak, self).__init__(name, graph)
        self.stop = False
        self.inExec = self.addInputPin('inExec', DataTypes.Exec, self.compute, hideLabel=True)
        self.firstIndex = self.addInputPin('start', DataTypes.Int)
        self.lastIndex = self.addInputPin('stop', DataTypes.Int)
        self.step = self.addInputPin('step', DataTypes.Int)
        self.breakExec = self.addInputPin('break', DataTypes.Exec, self.interrupt)
        self.step.setData(1)

        self.loopBody = self.addOutputPin('LoopBody', DataTypes.Exec)
        self.index = self.addOutputPin('Index', DataTypes.Int)
        self.completed = self.addOutputPin('Completed', DataTypes.Exec)

        pinAffects(self.firstIndex, self.index)
        pinAffects(self.lastIndex, self.index)
        pinAffects(self.step, self.index)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Int], 'outputs': [DataTypes.Exec, DataTypes.Int]}

    def interrupt(self):
        self.stop = True

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter']

    @staticmethod
    def description():
        return 'For loop with ability to break'

    def compute(self):
        indexFrom = self.firstIndex.getData()
        indexTo = self.lastIndex.getData()
        step = self.step.getData()
        for i in range(indexFrom, indexTo, step):
            if self.stop:
                break
            self.index.setData(i)
            self.loopBody.call()
        self.completed.call()
        self.stop = False