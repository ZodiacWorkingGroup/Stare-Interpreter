class stack:
    def __init__(self, *args, **kwargs):
        self._l = list(*args, **kwargs)

    def pop(self, index=-1):
        r = self[index]
        del self[index]
        return r

    def peek(self):
        return self[-1]

    def __str__(self):
        return ' '.join([str(x) for x in self[::-1]])

    def __repr__(self):
        r = ''
        intlength = max([len(str(x))+2 for x in self])
        r += '_'*(intlength+6)
        r += '\n'
        for x in self[::-1]:
            r += '|'
            desiredlen = intlength+4
            desiredlen -= len(str(x))
            r += '_'*(desiredlen//2)
            r += str(x)
            r += '_'*(desiredlen-desiredlen//2)
            r += '|\n'
        return r

    def push(self, value):
        self._l.append(value)

    def __getitem__(self, key):
        return self._l[key]

    def __delitem__(self, key):
        del self._l[key]

    def __setitem__(self, key, value):
        self._l[key] = value