import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# if sys.version_info < (2, 6): json?

setup(

      name = "ndevutils",
      version = "0.5",

      description = """Interactive utilities for developers using the NDEV HTTP service.""",
      long_description = read('README.md'),

      url = "", # TODO: add github URL

      author = "Local Projects, Inc",
      author_email = "sundar@localprojects.net",

      packages = find_packages(),

      install_requires = [
           "numpy",
           "requests == 2.3.0",
           "scikits.samplerate",
      ],

      classifiers = [ 
           'Development Status :: 4 - Beta',
           'Programming Language :: Python',
           'Intended Audience :: Developers',
           'Environment :: Console',
           'Topic :: Utilities',
      ],

)
