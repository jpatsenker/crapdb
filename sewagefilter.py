from abc import ABCMeta, abstractmethod

class SewageFilter:
    __metaclass__ = ABCMeta

    __name__ = None

    def __init__(self):
        super(SewageFilter, self).__init__()



    @abstractmethod
    def filter_crap(self, input_file, output_file):
        pass


    def get_name(self):
        return self.__name__