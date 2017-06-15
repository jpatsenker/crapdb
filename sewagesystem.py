import shutil
import subprocess
import os

from filters.sewagefilter import SewageFilter
from analyzers.sewageanalyzer import SewageAnalyzer
from aux import logtools


class SewageSystem:
	"""
	The Sewage System object
	Runs input/output through all the modules, managing input/output files on the way
	THIS CLASS WORKS PLEASE AVOID MODIFICATION
	"""

	modules = None

	def __init__(self):
		self.modules = []

	def add_module(self, smod):
		"""
		Add module to the pipeline
		:param smod:
		:return:
		"""
		assert isinstance(smod, SewageFilter) or isinstance(smod, SewageAnalyzer)
		self.modules.append(smod)

	def delete_module(self, name):
		"""
		Delete module from pipeline
		:param name:
		:return:
		"""
		assert isinstance(name, str)
		for fil in self.modules:
			if fil.get_name() == name:
				self.modules.remove(fil)
				return True
		return False

	def flush_the_toilet(self, input_file, output_file, diagnostics_file, temp_dir, exclude_modules = None, log=None):
		"""
		Run the pipeline
		:param input_file:
		:param output_file:
		:param diagnostics_file:
		:param temp_dir:
		:param exclude_modules:
		:param log:
		:return:
		"""

		#handle params
		aFiles = []
		if exclude_modules is None:
			exclude_modules = []

		#logging
		logtools.add_to_log("ALLOCATING FILES FOR CURRENT JOB", log)

		logtools.add_start(log)
		logtools.add_line_to_log(log, 'Running CMD: rm -f ' +  temp_dir + os.path.basename(input_file) + "*")
		subprocess.Popen(['rm', '-f', temp_dir + os.path.basename(input_file) + "*"]).wait()

		logtools.add_line_to_log(log, 'Running CMD: cp ' + input_file + ' ' + temp_dir + os.path.basename(input_file))

		#copy input file to temp dir, with temp name
		shutil.copyfile(input_file, temp_dir + os.path.basename(input_file))

		logtools.add_end(log)

		#init temp files
		tfile_base = temp_dir + os.path.basename(input_file)
		tfiles = [tfile_base]


		#create all temp files
		for fnum in range(len(self.modules) - len(exclude_modules)):
			tfiles.append(tfile_base + "." + str(fnum))
			open(tfiles[-1], "w").close()

		#run through each module
		for fnum in range(len(self.modules)):
			#if this module is excluded then skip
			con = False
			for exnum in exclude_modules:
				if self.modules[exnum] == self.modules[fnum]:
					con = True
			if con:
				continue
			#Not the most object oriented thing, definitely exists a better solution, but this works currently
			#For filter do this
			if isinstance(self.modules[fnum], SewageFilter):
				#try:
				if log is not None:
					if not self.modules[fnum].has_logfile():
						self.modules[fnum].set_logfile(log)
					logtools.add_to_log(self.modules[fnum].get_name(), log, description="Running filter. File transition: " + tfiles[fnum] + " -> " + tfiles[fnum+1])
					logtools.add_start(log)
				if os.stat(tfiles[fnum]).st_size != 0:
					self.modules[fnum].filter_crap(tfiles[fnum], tfiles[fnum+1], diagnostics_file)
				if log is not None:
					logtools.add_end(log)
				#except TypeError as e:
				#    print "Its this type: " + str(self.modules[fnum]) + "\n"
				#    print str(e) + "\n"
				#    exit(1)
			else: #For Analyzer do this
				assert isinstance(self.modules[fnum], SewageAnalyzer)
				#try:
				aFile = str(tfile_base) + self.modules[fnum].get_name() + str(fnum)
				try:
					os.remove(aFile)
				except (OSError, IOError):
					pass
				if log is not None:
					logtools.add_to_log(self.modules[fnum].get_name(), log, description="Running analysis. File transition: " + tfiles[fnum] + " -> " + tfiles[fnum+1])
					logtools.add_start(log)
				self.modules[fnum].analyze_crap(tfiles[fnum], aFile, graphic=False)
				shutil.copyfile(tfiles[fnum], tfiles[fnum+1])
				aFiles.append(aFile)
				if log is not None:
					logtools.add_end(log)
				#except TypeError as e:
				#    print "Its this type: " + str(self.modules[fnum]) + "\n"
				#    print str(e) + "\n"
				#    exit(1)

		shutil.copyfile(tfiles[-1], output_file)
		return aFiles