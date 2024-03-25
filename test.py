## from search current path and db.ini

import os, sys
from pathlib import Path

print(os.path.abspath(__file__))

print(os.getcwd())
