#!/usr/bin/env python
"""Stateful programmatic web browsing.

Stateful programmatic web browsing, after Andy Lester's Perl module
WWW::Mechanize.
"""

from mechanize import __version__
def unparse_version(tup):
    major, minor, bugfix, state_char, pre = tup
    fmt = "%s.%s.%s"
    args = [major, minor, bugfix]
    if state_char is not None:
        fmt += "%s"
        args.append(state_char)
    if pre is not None:
        fmt += "-pre%s"
        args.append(pre)
    return fmt % tuple(args)
VERSION = unparse_version(__version__)
NAME = "mechanize"
PACKAGE = True
LICENSE = "BSD"
PLATFORMS = ["any"]
CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet
Topic :: Internet :: File Transfer Protocol (FTP)
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Internet :: WWW/HTTP :: Indexing/Search
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: System :: Archiving :: Mirroring
Topic :: System :: Networking :: Monitoring
Topic :: System :: Systems Administration
Topic :: Text Processing :: Markup
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: XML
"""

#-------------------------------------------------------
# the rest is constant for most of my released packages:

import sys, string
from distutils.core import setup

_setup = setup
def setup(**kwargs):
    if not hasattr(sys, "version_info") or sys.version_info < (2, 3):
        # Python version compatibility
        # XXX probably download_url came in earlier than 2.3
        for key in ["classifiers", "download_url"]:
            if kwargs.has_key(key):
                del kwargs[key]
    # Only want packages keyword if this is a package,
    # only want py_modules keyword if this is a single-file module,
    # so get rid of packages or py_modules keyword as appropriate.
    if kwargs["packages"] is None:
        del kwargs["packages"]
    else:
        del kwargs["py_modules"]
    apply(_setup, (), kwargs)

if PACKAGE:
    packages = [NAME]
    py_modules = None
else:
    py_modules = [NAME]
    packages = None

doclines = string.split(__doc__, "\n")

setup(name = NAME,
      version = VERSION,
      license = LICENSE,
      platforms = PLATFORMS,
      classifiers = filter(None, string.split(CLASSIFIERS, "\n")),
      author = "John J. Lee",
      author_email = "jjl@pobox.com",
      description = doclines[0],
      url = "http://wwwsearch.sourceforge.net/%s/" % NAME,
      download_url = ("http://wwwsearch.sourceforge.net/%s/src/"
                      "%s-%s.tar.gz" % (NAME, NAME, VERSION)),
      long_description = string.join(doclines[2:], "\n"),
      py_modules = py_modules,
      packages = packages,
      )
