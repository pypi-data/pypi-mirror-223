import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Everything-Tkinter'])

from .language import LanguageType


meliq = LanguageType('en', 6, 32)
meliq.display_matrix()