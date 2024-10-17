import inspect, traceback, types
from debug_utils import LOG_ERROR

def overrideIsSuccessful(target, holder, name, getter=None):
    if not hasattr(holder, name):
        return False
    else:
        original = getattr(holder, name)
        overridden = lambda *args, **kwargs: target(original, *args, **kwargs)

        if isinstance(original, types.MethodType):
            numberOfArgsInOriginalMethod = len(inspect.getargspec(original).args)
            # Target has one extra arg because we pass in the original method as the first argument
            numberOfArgsInTargetMethod = len(inspect.getargspec(target).args) - 1
            if (numberOfArgsInOriginalMethod != numberOfArgsInTargetMethod):
                LOG_ERROR('[SAFELOADER] Unable to override method ' + str(holder) + '.' + str(name))
                LOG_ERROR('[SAFELOADER] Expected number of args: ' + str(numberOfArgsInTargetMethod) + ', actual number of args: ' + str(numberOfArgsInOriginalMethod))
                return False

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
