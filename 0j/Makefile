EXECFILES= kjbuckets.so

all : $(EXECFILES)

kjbuckets.so : 
	 # check resources also deals with case where kjBuckets installed elsewhere
	check_resources

test:
	checktest '0j.py -scores_only DATA/sample_refs' DATA/out1
	echo
	echo "The next test will take a little time. The protein has extremely low complexity ..."
	checktest '0j.py DATA/FBOH_BOMMO' DATA/out2

tarfile:
	make clean
	# This is rather ham-fisted
	tar cf temp.tar `cat FILES` FILES
	mkdir 0j
	mv temp.tar 0j
	(cd 0j && tar xf temp.tar)
	rm 0j/temp.tar
	tar cf 0j.tar 0j
	gzip 0j.tar
	/bin/rm -r 0j

clean:
	rm -f *.pyc *.so
	(cd KJBUCKETS; make clean)

new:
	make clean
	make

