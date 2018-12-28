import sys
from distutils.core import setup, Extension

kjbuckets_ext = Extension("kjbuckets",
			  sources=["kjbucketsmodule.c"],
			  extra_compile_args=["-funroll-loops"],
			  include_dirs=["."])

setup (name = "kjbuckets",
       description = "kjBuckets implementation of sets",
       author = "Aaron Robert Watters",
       maintainer = "Michael J. Wise",

       ext_modules = [ kjbuckets_ext ]
)
