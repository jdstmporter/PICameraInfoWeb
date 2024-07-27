import importlib.util
import sys



def isAvailable(name):
    if name in sys.modules:
        print(f"{name!r} already in sys.modules")
        return True
    elif (mod := importlib.util.find_spec(name)) is not None:
        print(f'{name!r} exist at {mod.origin}')
        return True
    else:
        print('Not found')
        return False