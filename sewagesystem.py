from sewagefilter import SewageFilter


class SewageSystem:

    filters = None

    def __init__(self):
        self.filters = []

    def add_filter(self, sfilter):
        assert isinstance(sfilter, SewageFilter)
        self.filters.append(sfilter)

    def delete_filter(self, name):
        assert isinstance(name, str)
        for fil in self.filters:
            if fil.getName() == name:
                self.filters.remove(self.filters.index(fil))
                return True
                break
            return False