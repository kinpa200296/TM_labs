class Token(object):

    def __init__(self, name, value):
        if not isinstance(name, unicode):
            raise ValueError('name should be a unicode string')
        if not isinstance(value, unicode):
            raise ValueError('value should be a unicode string')
        self.name = name
        self.value = value
        self.line = 0
        self.column = 0

    def __repr__(self):
        return self.__str__().__repr__()

    def __str__(self):
        return '{name}: {value}'.format(name=self.name, value=self.value)

    def show_as_invalid(self):
        return 'Invalid token at ({line}, {column}): {value}'.format(line=self.line,
                                                                       column=self.column,
                                                                       value=self.value)
