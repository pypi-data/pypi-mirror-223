# setup.py is a part of the PYTHIA event generator.
# Copyright (C) 2023 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
# Author: Philip Ilten, August 2023.
#
# This script is used to package Pythia for PyPI.

#==========================================================================

# Define the Pythia version, and the Python package subversion.
ver = "310"
sub = "0"

#==========================================================================
def walk(top, pre):
    """
    Return a data structure for setup's data_files argument of the form,
    [(path, [files]), ...] for each non-empty directory.

    top: top directory to begin listing the data files.
    pre: prefix to append at the start of each relative path.
    """
    import os
    data, pre , top = [], pre.rstrip("/") + "/", top.rstrip("/") + "/"
    for path, subs, files in os.walk(pre):
        if not files: continue
        path += "/"
        data += [(top + path[len(pre):], [path + name for name in files])]
    return data

#==========================================================================

# Configure the Python build.

# Determine the PyBind version to use.
import sys
if sys.version_info.major >= 3 and sys.version_info.minor > 5:
    pybind = "2.10.4"
else:
    pybind = "2.9.2"

# Determine the package data (headers only needed for source).
data = walk("share/Pythia8", "pythia8" + ver + "/share/Pythia8")
if "sdist" in sys.argv:
    data += walk("include", "pythia8" + ver + "/plugins/python/include")

# Set the source files.
from glob import glob
sources = glob("pythia8" + ver + "/src/*.cc") + glob(
    "pythia8" + ver + "/plugins/python/src/*.cpp")

# Configure the build.
from distutils.core import Extension
ext = Extension(
    name="pythia8mc",
    language = "c++",
    define_macros = [
        # Enable GZIP support.
        ("GZIP", ""),
        # Set a dummy XML path. 
        ("XMLDIR", "\"share/Pythia8/xmldoc\""),
        # FastJet multithreading support.
        ("FJCORE_HAVE_LIMITED_THREAD_SAFETY", "")],
    extra_compile_args = ["-std=c++11"],
    extra_link_args = ["-lz"],
    include_dirs = [
        "pythia8" + ver + "/plugins/python/include",
        "pythia8" + ver + "/plugins/python/include/" + pybind],
    sources = sources
)

# Class to remove compiler warnings.
from distutils.command.build_ext import build_ext
from distutils.sysconfig import customize_compiler
class RemoveWarnings(build_ext):
    def build_extensions(self):
        customize_compiler(self.compiler)
        for flag in [
                "-Wall", "-Wunused-but-set-variable", "-Wstrict-prototypes"]:
            try: self.compiler.compiler_so.remove(flag)
            except (AttributeError, ValueError): continue
        build_ext.build_extensions(self)

# Set up.
from distutils.core import setup
setup(
    name = "pythia8mc",
    version = ".".join(["8", ver, sub]),
    author = "Pythia 8 Team",
    author_email = "authors@pythia.org",
    description = "General purpose particle physics Monte Carlo generator.",
    long_description = "PYTHIA is a program for the generation of high-energy physics collision events, i.e. for the description of collisions at high energies between electrons, protons, photons and heavy nuclei. It contains theory and models for a number of physics aspects, including hard and soft interactions, parton distributions, initial- and final-state parton showers, multiparton interactions, fragmentation and decay. It is largely based on original research, but also borrows many formulae and other knowledge from the literature. As such it is categorized as a general purpose Monte Carlo event generator.",
    license = "GNU GPL v2 or later",
    data_files = data,
    url = "https://pythia.org",
    platforms = ["Linux", "MacOS"],
    # Don't allow zipping.
    zip_safe = False,
    # Define the C++ module.
    ext_modules = [ext],
    # Remove compiler warnings.
    cmdclass = {'build_ext': RemoveWarnings}
)
