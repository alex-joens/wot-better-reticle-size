# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\safeloader\loader.py
# Compiled at: 2023-12-31 00:52:29
from .constants import SAFELOADER_ATTRIBUTE_NAME
from debug_utils import LOG_ERROR
from gui import mods

class _SafeLibrary:

    def __init__(self, name, instance):
        self.name = name
        self.instance = instance


class Safeloader:

    def __init__(self):
        self.libs = []
        self.mods = []
        self.safeloadCallbacks = []

    def loadMods(self):
        for modModule in self.mods:
            modModule.safeInit()


def addLibrary(name, instance):
    getattr(mods, SAFELOADER_ATTRIBUTE_NAME).libs.append(_SafeLibrary(name, instance))


def getLibrary(name):
    loader = getattr(mods, SAFELOADER_ATTRIBUTE_NAME)
    return next((x for x in loader.libs if x.name == name), None)


def register(modModule):
    getattr(mods, SAFELOADER_ATTRIBUTE_NAME).mods.append(modModule)


def addNotifySafeloadSuccessCallback(callback):

    def wrappedCallback(modInfo, status):
        try:
            callback(modInfo, status)
        except:
            import traceback
            LOG_ERROR('[SAFELOADER] Callback function in ' + callback.__module__ + ' threw an exception:')
            for line in traceback.format_stack():
                LOG_ERROR('[SAFELOADER] ' + line.strip())

    getattr(mods, SAFELOADER_ATTRIBUTE_NAME).safeloadCallbacks.append((callback, wrappedCallback))


def removeNotifySafeloadSuccessCallback(callback):
    callbacks = getattr(mods, SAFELOADER_ATTRIBUTE_NAME).safeloadCallbacks
    callbacks = callbacks.filter((lambda x: x[0] != callback))
    setattr(mods, SAFELOADER_ATTRIBUTE_NAME, callbacks)


def notifyOfSafeloadingStatus(modInfo, status):
    map((lambda x: x[1](modInfo, status)), getattr(mods, SAFELOADER_ATTRIBUTE_NAME).safeloadCallbacks)
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\safeloader\loader.pyc
