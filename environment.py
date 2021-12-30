class Environment():
    def __init__(self, record={}, parent = None):
        self.record = record
        self.parent = parent

    def __repr__(self):
        return str({'record': self.record, 'parent': self.parent})

    def define(self, name, value):
        self.record[name] = value
        return value

    def assign(self, name, value):
        self.__resolve(name).record[name] = value
        return value

    def lookup(self, name):
        return self.__resolve(name).record[name]

    def __resolve(self, name):
        if name in self.record:
            return self
        elif self.parent is None:
            raise KeyError('Cannot find variable name: ', name);
        else:
            return self.parent.__resolve(name)
