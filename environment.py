class Environment():
    def __init__(self, record={}, parent = None):
        self.record = record
        self.parent = parent

    def define(self, name, value):
        self.record[name] = value
        return value

    def assign(self, name, value):
        pass

    def lookup(self, name):
        # return self.record[name]
        if name in self.record:
            return self.record[name]
        elif self.parent is None:
            raise KeyError('Cannot find variable name: ', name);
        else:
            return self.parent.lookup(name)
