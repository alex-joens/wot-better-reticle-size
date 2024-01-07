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


def resetOverride(holder, name):
    overridden = getattr(holder, name)
    setattr(holder, name, overridden.im_func.__closure__[0].cell_contents)
