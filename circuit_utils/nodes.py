import copy
class Value(object):
    # TODO: Add D and D' to possible values to support fault propagation
    def __init__(self, value: str):
        try:
            value = value.upper()
        except AttributeError:
            pass
        if value == 0 or value == '0':
            self.value = 0
        elif value == 1 or value == '1':
            self.value = 1
        else:
            self.value = 'U'

    def __eq__(self, other):
        if self.value == 1:
            if other == 1 or other == '1':
                return True
        elif self.value == 0:
            if other == 0 or other == '0':
                return True
        elif self.value == 'U':
            if other == 'U' or other == 'u':
                return True
        return False

    def __and__(self, other):
        if self == 1:
            if other == 1:
                return Value('1')
            if other == 'U':
                return Value('U')
        return Value('0')

    def __or__(self, other):
        if self == 1 or other == 1:
            return Value(1)
        if self == 'U' or other == 'U':
            return Value('U')
        return Value(0)

    def __invert__(self):
        if self == 1:
            return Value(0)
        if self == 0:
            return Value(1)
        return Value('U')

    def __str__(self):
        return str(self.value)


class Gate(object):
    def __init__(self, name: str, inputs=[]):
        self.input_names = inputs
        self.input_nodes = []
        self.output_nodes = []
        self.name = name
        self.value = Value('U')
        self.value_new = Value('U')
        self.type = None
        self.logic = self.logic

    def update(self):
        self.value = self.value_new

    def logic(self):
        # Do not change
        pass

class Node(object):
# class Node(object):
    def __init__(self, gate: Gate):
        self.gate = gate
        self.name = gate.name
        self.gate_type = gate.type
        self.update = gate.update
        self.logic = gate.logic
        self.input_names = gate.input_names
        self.value = gate.value
        self.type = 'wire'
        self.output_nodes = gate.output_nodes
        self.input_nodes = gate.input_nodes

    @property
    def value_new(self):
        return self.gate.value_new

    @property
    def value(self):
        return self.gate.value

    @value.setter
    def value(self, other:Value):
        self.gate.value = other

    @value_new.setter
    def value_new(self, other: Value):
        self.gate.value_new = other




    # @property
    # def gate(self):
    #     return self._gate
        # self.name = gate.name
        # self.gate_type = gate.type
        # self.update = gate.update
        # self.logic = gate.logic
        # self.input_names = gate.input_names
        # self.value_new = gate.value_new
        # self.value = gate.value
        # self.type = 'wire'
        # self.input_nodes = gate.input_nodes
        # self.output_nodes = gate.output_nodes

    def __eq__(self, other):
        if self.value == other:
            return True
        return False

    def __str__(self):
        # TODO: Improve the readout of node information
        return f"{str(self.type)}\t{str(self.name)} = {self.value}"

    def reset(self):
        self.value = Value('U')
        self.value_new = Value('U')

    def set(self, value: Value):
        self.value = value
        self.value_new = value


# TODO: Add D-logic support for the different gates
class AndGate(Gate):
    def __init__(self, name, inputs: []):
        super(AndGate, self).__init__(name, inputs)
        self.type = "AND"

    def logic(self):
        if any(node == 0 for node in self.input_nodes):
            self.value_new = Value(0)
        elif all(node == 1 for node in self.input_nodes):
            self.value_new = Value(1)
        else:
            self.value_new = Value('U')


class OrGate(Gate):
    def __init__(self, name, inputs: []):
        super(OrGate, self).__init__(name, inputs)
        self.type = "OR"

    def logic(self):
        if any(node == 1 for node in self.input_nodes):
            self.value_new = Value(1)
        elif any(node == 'U' for node in self.input_nodes):
            self.value_new = Value('U')
        else:
            self.value_new = Value(0)


class NandGate(Gate):
    def __init__(self, name, inputs: []):
        super(NandGate, self).__init__(name, inputs)
        self.type = "NAND"

    def logic(self):
        if any(node == 0 for node in self.input_nodes):
            self.value_new = Value(1)
        elif any(node == 'U' for node in self.input_nodes):
            self.value_new = Value('U')
        self.value_new = Value(0)


class NotGate(Gate):
    def __init__(self, name, inputs: []):
        super(NotGate, self).__init__(name, inputs)
        self.type = "NOT"

    def logic(self):
        self.value_new = ~self.input_nodes[0].value


class XnorGate(Gate):
    def __init__(self, name, inputs: []):
        super(XnorGate, self).__init__(name, inputs)
        self.type = "XNOR"

    def logic(self):
        pass
        # TDDO: logic


class XorGate(Gate):
    def __init__(self, name, inputs: []):
        super(XorGate, self).__init__(name, inputs)
        self.type = "XOR"

    def logic(self):
        pass
        # TODO: logic


class NorGate(Gate):
    def __init__(self, name, inputs: []):
        super(NorGate, self).__init__(name, inputs)
        self.type = "NOR"

    def logic(self):
        if any(node == 1 for node in self.input_nodes):
            self.value_new = Value(0)
        if any(node == 'U' for node in self.input_nodes):
            self.value_new = Value('U')
        self.value_new = Value(1)


class BuffGate(Gate):
    def __init__(self, name, inputs: []):
        super(BuffGate, self).__init__(name, inputs)
        self.type = "BUFF"

    def logic(self):
        self.value_new = self.input_nodes[0].value
