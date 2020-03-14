#Stopwatch
import contextlib
import time

@contextlib.contextmanager
def stopwatch(processmessage, completemessage):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        print(processmessage)
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (completemessage, t1 - t0))
        
