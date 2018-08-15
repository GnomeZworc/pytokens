import os
from .default import variables

def env(var):
    if var in os.environ:
        return os.environ[var]
    else:
        return variables[var]
