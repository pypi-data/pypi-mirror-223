try:
    from ...__config__ import LIBTIEPIE as DLL_PATH
except ImportError:
    DLL_PATH = 'libtiepie-hw.so.1'
