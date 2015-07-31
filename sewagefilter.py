from abc import ABCMeta, abstractmethod

class SewageFilter:
    __metaclass__ = ABCMeta

    name = None

    @abstractmethod
    def filter_crap(self, input_file, output_file):
        pass