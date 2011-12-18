import os, sys
from CannedZen.BaseInteract import InteractRegistrar
from CannedZen.Registration import GlobalSettings

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py' or module == "BaseInteract.py": continue
    __import__(module[:-3], locals(), globals())