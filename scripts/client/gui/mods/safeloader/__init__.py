# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\safeloader\__init__.py
# Compiled at: 2023-12-31 00:52:06
from gui import mods
from gui.game_loading import loading as gameLoading
from .constants import SAFELOADER_ATTRIBUTE_NAME
from .loader import Safeloader
SAFELOADER = Safeloader()

def _injectSafeloaderIfNotInjectedYet():
    if not hasattr(mods, SAFELOADER_ATTRIBUTE_NAME):
        setattr(mods, SAFELOADER_ATTRIBUTE_NAME, SAFELOADER)
        regular_step = getattr(gameLoading, 'step')

        def new_step():
            setattr(gameLoading, 'step', regular_step)
            safeloader = getattr(mods, SAFELOADER_ATTRIBUTE_NAME)
            safeloader.loadMods()
            print '[SAFELOADER] All mods have been loaded!'
            regular_step()

        setattr(gameLoading, 'step', new_step)


_injectSafeloaderIfNotInjectedYet()
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\safeloader\__init__.pyc
