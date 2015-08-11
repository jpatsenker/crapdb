from sewagefilter import SewageFilter
from sewagefilter import BrokenFilterError
import shutil
import os

class SewageSystem:

    filters = None

    def __init__(self):
        self.filters = [SewageFilter]

    def add_filter(self, sfilter):
        assert isinstance(sfilter, SewageFilter)
        self.filters.append(sfilter)

    def delete_filter(self, name):
        assert isinstance(name, str)
        for fil in self.filters:
            if fil.get_name() == name:
                self.filters.remove(fil)
                return True
        return False

    def filter_crap(self, input_file, output_file, diagnostics_file, temp_dir, exclude_filters = None):
        if exclude_filters is None:
            exclude_filters = []

        shutil.copyfile(input_file, temp_dir + os.path.basename(input_file))

        tfile_base = temp_dir + os.path.basename(input_file)
        tfiles = [tfile_base]

        for fnum in range(len(self.filters) - len(exclude_filters)):
            tfiles.append(tfile_base + "." + str(fnum))

        for fnum in range(len(self.filters)):
            for exnum in exclude_filters:
                if self.filters[exnum] == self.filters[fnum]:
                    continue
            try:
                self.filters[fnum].filter_crap(tfiles[fnum], tfiles[fnum+1], diagnostics_file)
            except BrokenFilterError:
                print "Oh no! Broken filter: " + self.filters[fnum].get_name() + " (#" + str(fnum) + ") \n Sewage Clogged!!! \n"
                exit(1)

        shutil.copyfile(tfiles[-1], output_file)