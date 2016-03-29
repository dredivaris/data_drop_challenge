from collections import OrderedDict


class ComparisonDict(OrderedDict):
    def __eq__(self, other):
        if set(self.keys()) != set(other.keys()):
            return False
        for key in self.keys():
            if str(self[key]).strip() != str(other[key]).strip():
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], tuple):
            for key, val in args[0]:
                self[key] = val
        else:
            super().__init__(*args, **kwargs)
