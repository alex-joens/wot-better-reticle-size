import inspect, traceback, types
from debug_utils import LOG_ERROR

def overrideIsSuccessful(target, holder, name, getter=None):
    if not hasattr(holder, name):
        LOG_ERROR('[SFAFELOADER] ' + str(holder) + ' does not have an attribute named "' + str(name) + '"')
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


# Try to reset the override, effectively uninstalling the mod
def resetOverride(holder, name):
    try:
        overridden = getattr(holder, name)
        if isinstance(overridden, property):
            # The original property is the first arg of the setter if it exists, else it's the first arg of the getter
            if overridden.fset is not None:
                originalProperty = overridden.fset.__closure__[0].cell_contents
                setattr(holder, name, originalProperty)
            else:
                originalProperty = overridden.fget.__closure__[0].cell_contents
                setattr(holder, name, originalProperty)
        else:
            setattr(holder, name, overridden.im_func.__closure__[0].cell_contents)
    except:
        # If the override couldn't be rolled back, the game will be in an unstable state.
        # It is safer to crash the game to let the player know something is wrong, so they can remove the faulty mod.
        LOG_ERROR('[SAFELOADER] Unable to safely rollback ' + str(holder) + '.' + str(name))
        traceback.print_exc()
        raise Exception() 

