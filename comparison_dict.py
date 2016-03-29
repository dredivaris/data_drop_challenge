class ComparisonDict(dict):
    def __eq__(self, other):
        if set(self.keys()) != set(other.keys()):
            return False
        for key in self.keys():
            if str(self[key]).strip() != str(other[key]).strip():
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
