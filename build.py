#!/usr/bin/env python3
## INFO ##
## INFO ##

# Import python modules
from os.path import join

# Import tmtools modules
try:
    from tmtools.convert import Language
except ImportError:
    from sys import exit
    print('[ ERROR ] tmtools modules are missing: '
          'install it from http://github.com/petervaro/tmtools')
    exit(-1)

# Module level constants
CURRENT_DIR = '.'
LANG_PATH  = join(CURRENT_DIR, 'langs')


#------------------------------------------------------------------------------#
# Import C11 modules
from C11 import syntax

# Setup names and locations
lang = Language(name='C11',
                path=LANG_PATH,
                scope='c.11',
                comments={'lines' : '//',
                          'blocks': ('/*', '*/')},
                test_name='C11_TEST',
                test_path='~/.config/sublime-text-3/Packages/User/C11_TEST')
# Convert and save language file
lang.from_dict(syntax)
lang.write()
