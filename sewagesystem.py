from sewagefilter import SewageFilter
from sewagefilter import BrokenFilterError
from sewageanalyzer import SewageAnalyzer
import shutil
import subprocess
import os
import logtools

class SewageSystem:

    modules = None

    def __init__(self):
        self.modules = []

    def add_module(self, smod):
        assert isinstance(smod, SewageFilter) or isinstance(smod, SewageAnalyzer)
        self.modules.append(smod)

    def delete_module(self, name):
        assert isinstance(name, str)
        for fil in self.modules:
            if fil.get_name() == name:
                self.modules.remove(fil)
                return True
        return False

    def flush_the_toilet(self, input_file, output_file, diagnostics_file, temp_dir, exclude_modules = None, log=None):
        aFiles = []
        if exclude_modules is None:
            exclude_modules = []

        #print ['rm', '-f', temp_dir + os.path.basename(input_file) + "*"]
        subprocess.Popen(['rm', '-f', temp_dir + os.path.basename(input_file) + "*"]).wait()

        shutil.copyfile(input_file, temp_dir + os.path.basename(input_file))

        tfile_base = temp_dir + os.path.basename(input_file)
        tfiles = [tfile_base]

        for fnum in range(len(self.modules) - len(exclude_modules)):
            tfiles.append(tfile_base + "." + str(fnum))
            open(tfiles[-1], "w").close()

        for fnum in range(len(self.modules)):
            con = False
            for exnum in exclude_modules:
                if self.modules[exnum] == self.modules[fnum]:
                    con = True
            if con:
                continue
            if isinstance(self.modules[fnum], SewageFilter):
                try:
                    self.modules[fnum].filter_crap(tfiles[fnum], tfiles[fnum+1], diagnostics_file)
                    if log is not None:
                        logtools.add_to_log(self.modules[fnum].get_name(), log, description="Running filter. File transition: " + tfiles[fnum] + " -> " + tfiles[fnum+1])
                except BrokenFilterError:
                    print "Oh no! Broken filter: " + self.modules[fnum].get_name() + " (#" + str(fnum) + ") \n Sewage Clogged!!! \n"
                    exit(1)
                except TypeError:
                    print "Yo its this type: " + str(self.modules[fnum] + "\n")
                    exit(1)
            else:
                assert isinstance(self.modules[fnum], SewageAnalyzer)
                try:
                    aFile = str(tfile_base) + self.modules[fnum].get_name() + str(fnum)
                    try:
                        os.remove(aFile)
                    except (OSError, IOError):
                        pass
                    self.modules[fnum].analyze_crap(tfiles[fnum], aFile, graphic=False)
                    shutil.copyfile(tfiles[fnum], tfiles[fnum+1])
                    aFiles.append(aFile)
                    if log is not None:
                        logtools.add_to_log(self.modules[fnum].get_name(), log, description="Running analysis. File transition: " + tfiles[fnum] + " -> " + tfiles[fnum+1])
                except TypeError:
                    print "Yo its this type: " + str(self.modules[fnum] + "\n")
                    exit(1)

        shutil.copyfile(tfiles[-1], output_file)
        return aFiles