# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\safeloader\override.py
# Compiled at: 2023-12-31 00:52:33
import traceback, types
from debug_utils import LOG_ERROR

def overrideIsSuccessful(target, holder, name, getter=None):
    if not hasattr(holder, name):
        return False
    else:
        original = getattr(holder, name)
        overridden = lambda *args, **kwargs: target(original, *args, **kwargs)
        try:
            if not isinstance(holder, types.ModuleType) and isinstance(original, types.FunctionType):
                setattr(holder, name, staticmethod(overridden))
            elif isinstance(original, property):
                if getter is not None:
                    setattr(holder, name, property(getter, overridden))
                else:
                    setattr(holder, name, property(overridden))
            else:
                setattr(holder, name, overridden)
        except:
            LOG_ERROR('[SAFELOADER] Unable to override ' + str(holder) + '.' + str(name))
            traceback.print_exc()
            return False

        return True
        return


def resetOverride(holder, name):
    overridden = getattr(holder, name)
    setattr(holder, name, overridden.im_func.__closure__[0].cell_contents)
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\safeloader\override.pyc
