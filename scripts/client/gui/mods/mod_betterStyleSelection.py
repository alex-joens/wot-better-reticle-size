# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\mod_betterStyleSelection.py
# Compiled at: 2023-12-31 00:41:20
from .jakLibrary import JakLib
from .jakLibrary.config_parameters import ConfigParameter, ConfigSection, ParameterSettings
from .jakLibrary.config_validators import isBool
from .safeloader.decorators import SafeInit, SafeOverride
from gui.shared.gui_items.customization.c11n_items import Style
from helpers.i18n import makeString
__mod_name_key__ = 'betterStyleSelection.modname'
__mod_color__ = '#FFA500'

class State:

    def __init__(self):
        self.initialized = False
        self.styleSortingEnabled = False


STATE = State()
_STYLE_SORTING_CONFIG = ConfigSection('common', [
 ConfigParameter('styleSortingEnabled', isBool, True, ParameterSettings(1, {'type': 'CheckBox', 'text': 'betterStyleSelection.styleSortingEnabled.title', 
    'tooltip': 'betterStyleSelection.styleSortingEnabled.description'}))], __mod_name_key__, 'betterStyleSelection', False, True)
UNIQUE_STYLE_GROUP_ID = '#vehicle_customization:styles/unique_styles'
UNIQUE_STYLE_NAME = makeString(UNIQUE_STYLE_GROUP_ID)

@SafeOverride(Style, 'groupID')
def new_StyleGroupId(_, self):
    if STATE.styleSortingEnabled and (getattr(self, 'is3D', False) or isStyleVehicleSpecific(self)):
        return UNIQUE_STYLE_GROUP_ID
    return self.descriptor.parentGroup.itemPrototype.userKey


@SafeOverride(Style, 'groupUserName')
def new_StyleGroupUserName(_, self):
    if STATE.styleSortingEnabled and (getattr(self, 'is3D', False) or isStyleVehicleSpecific(self)):
        return UNIQUE_STYLE_NAME
    return self.descriptor.parentGroup.itemPrototype.userString


def isStyleVehicleSpecific(style):
    for node in style.descriptor.filter.include:
        if node.vehicles:
            return True

    return False


@SafeInit
def init():
    if STATE.initialized is False:
        JakLib.initializeModWithConfig(_STYLE_SORTING_CONFIG, onModSettingsChanged)
    STATE.initialized = True


def onModSettingsChanged(updatedConfig):
    if updatedConfig.enabled is False:
        STATE.styleSortingEnabled = False
    else:
        STATE.styleSortingEnabled = updatedConfig.styleSortingEnabled
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\mod_betterStyleSelection.pyc
