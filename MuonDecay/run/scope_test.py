import pyvisa
import ctypes
from configs import cfg_scope as config
from time import time, ctime, sleep
from datetime import timedelta


rm = pyvisa.ResourceManager()                 # Calling PyVisa library
scope = rm.open_resource(str(config.ScopeID))
scope.write('CURVe?')
size = scope.chunk_size
start = time()
#pyvisa.ctwrapper.functions.read(rm.visalib, scope.session, size)
buffer = ctypes.create_string_buffer(size)

lib = pyvisa.highlevel.VisaLibraryBase(scope)


# return_count = c_ulong()
# y = scope.visalib.lib.viRead(scope.session, buffer, size, byref(return_count))
finish = time()
print(f'Time: {timedelta(seconds=finish - start)}')