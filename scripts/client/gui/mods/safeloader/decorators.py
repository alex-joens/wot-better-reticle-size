# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\safeloader\decorators.py
# Compiled at: 2023-12-31 00:52:24
from .constants import MOD_SAFELOAD_STATUS, SAFEOVERRIDE_ATTRIBUTE_NAME
from .loader import addLibrary, getLibrary, notifyOfSafeloadingStatus, register
from .override import overrideIsSuccessful, resetOverride
import sys
from functools import wraps
from debug_utils import LOG_ERROR

def SafeOverride(holder, name, getter=None):

    def registerOverride(target):
        modModule = sys.modules[target.__module__]
        if not hasattr(modModule, SAFEOVERRIDE_ATTRIBUTE_NAME):
            setattr(modModule, SAFEOVERRIDE_ATTRIBUTE_NAME, list())
        getattr(modModule, SAFEOVERRIDE_ATTRIBUTE_NAME).append((target, holder, name, getter))
        return target

    return registerOverride


def SafeInit(*modulesWithOverrides):

    def wrapInit(originalInit):
        modModule = sys.modules[originalInit.__module__]

        @wraps(originalInit)
        def safeInit():
            anyFailed = False
            appliedOverrides = []
            overrideList = _getOverrides(modModule, *modulesWithOverrides)
            for override in overrideList:
                target, holder, name, getter = override
                if overrideIsSuccessful(target, holder, name, getter):
                    appliedOverrides.append((holder, name))
                else:
                    anyFailed = True
                    break

            if anyFailed:
                _rollback(appliedOverrides)
                _notifyFailure(modModule)
                return
            notifyOfSafeloadingStatus(modModule, MOD_SAFELOAD_STATUS.Success)
            originalInit()

        setattr(modModule, 'safeInit', safeInit)

        def init():
            register(modModule)

        return init

    return wrapInit


SafeInit = SafeInit()

def GlobalLibrary(libName, *initArgs, **initKwargs):

    def decorator(origClass):
        instanceName = 'g_' + libName + '_' + origClass.__name__
        instance = getLibrary(instanceName)
        if instance is None:
            instance = origClass(*initArgs, **initKwargs)
            addLibrary(instanceName, instance)
        setattr(origClass, instanceName, instance)
        _replacePublicMethodsWithStaticMethods(origClass, instanceName)
        return origClass

    return decorator


def ModLibrary(*initArgs, **initKwargs):

    def decorator(origClass):
        instanceName = 'g_' + origClass.__name__
        instance = getattr(origClass, instanceName, None)
        if instance is None:
            instance = origClass(*initArgs, **initKwargs)
            setattr(origClass, instanceName, instance)
        _replacePublicMethodsWithStaticMethods(origClass, instanceName)
        return origClass

    return decorator


ModLibrary = ModLibrary()

def _doNotInit(*args, **kwargs):
    LOG_ERROR("[SAFELOADER] You probably shouldn't be trying to __init__ this class. Use the static methods instead.")


def _replacePublicMethodsWithStaticMethods(origClass, instanceName):
    setattr(origClass, '_instance__init__', getattr(origClass, '__init__'))
    newInit = lambda *args, **kwargs: _doNotInit(*args, **kwargs)
    setattr(origClass, '__init__', newInit)
    for func in dir(origClass):
        if func.startswith('_') or func.startswith('g_'):
            continue
        origFunc = getattr(origClass, func)
        setattr(origClass, '_instance__' + func, origFunc)
        _addNewStaticMethod(origClass, instanceName, func)


def _addNewStaticMethod(origClass, instanceName, func):
    newFuncName = func
    if not getattr(getattr(origClass, instanceName), '__safeloader_external_library', False):
        newFuncName = '_instance__' + func
    newFunc = lambda *args, **kwargs: getattr(getattr(origClass, instanceName), newFuncName)(*args, **kwargs)
    setattr(origClass, func, staticmethod(newFunc))


def _getOverrides(modModule, *modulesWithOverrides):
    allModules = [
     modModule]
    allModules.extend(modulesWithOverrides)
    allOverrides = []
    for module in allModules:
        if hasattr(module, SAFEOVERRIDE_ATTRIBUTE_NAME):
            allOverrides.extend(getattr(module, SAFEOVERRIDE_ATTRIBUTE_NAME))

    return allOverrides


def _rollback(appliedOverrides):
    for appliedOverride in appliedOverrides:
        holder, name = appliedOverride
        resetOverride(holder, name)


def _notifyFailure(modModule):
    modName = modModule.__name__.partition('gui.mods.')[2]
    if len(modName) == 0:
        modName = modModule.__name__
    LOG_ERROR('[SAFELOADER] Unable to initialize ' + modName)
    notifyOfSafeloadingStatus(modModule, MOD_SAFELOAD_STATUS.Failure)
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\safeloader\decorators.pyc
