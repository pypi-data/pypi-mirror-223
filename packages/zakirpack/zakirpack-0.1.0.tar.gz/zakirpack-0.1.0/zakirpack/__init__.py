import sys

if sys.version_info[:2] == (3, 6):
    from .eCon_36 import *
elif sys.version_info[:2] == (3, 7):
    from .eCon_37 import *
elif sys.version_info[:2] == (3, 8):
    from .eCon_38 import *
elif sys.version_info[:2] == (3, 9):
    from .eCon_39 import *
elif sys.version_info[:2] == (3, 10):
    from .eCon_310 import *
else:
    raise ImportError("Unsupported Python version")
