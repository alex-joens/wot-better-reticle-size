# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\mod_betterBattleResults.py
# Compiled at: 2023-12-31 00:40:46
from .jakLibrary import JakLib
from .jakLibrary.config_parameters import ConfigParameter, ConfigSection, ParameterSettings
from .jakLibrary.config_validators import isBool
from .jakLibrary.lang import setLanguage
from .safeloader.decorators import SafeInit, SafeOverride
from .betterBattleResults.strings import loadStrings
from .betterBattleResults.overrides import TotalEfficiencyDetailsHeader_setRecord, ComplexBuilder_build
from gui.battle_results.components.personal import TotalEfficiencyDetailsHeader
from gui.shared.tooltips import builders
__mod_name_key__ = 'betterBattleResults.modname'
__mod_color__ = '#00D0D0'

class State:

    def __init__(self):
        self.initialized = False
        self.richTooltipEnabled = False


STATE = State()
_BETTER_BATTLE_RESULTS_CONFIG = ConfigSection('common', [
 ConfigParameter('richTooltipEnabled', isBool, True, ParameterSettings(1, {'type': 'CheckBox', 'text': 'betterBattleResults.richTooltip.title', 
    'tooltip': 'betterBattleResults.richTooltip.description'}))], __mod_name_key__, 'betterBattleResults')

@SafeOverride(TotalEfficiencyDetailsHeader, 'setRecord')
def new_TotalEfficiencyDetailsHeader_setRecord(origFunc, self, result, reusable):
    if STATE.richTooltipEnabled:
        TotalEfficiencyDetailsHeader_setRecord(origFunc, self, result, reusable)
    else:
        origFunc(self, result, reusable)


@SafeOverride(builders.ComplexBuilder, 'build')
def new_ComplexBuilder_build(_, self, formatType, advanced_, *args, **kwargs):
    return ComplexBuilder_build(_, self, formatType, advanced_, *args, **kwargs)


@SafeInit
def init():
    if STATE.initialized is False:
        loadStrings()
        JakLib.initializeModWithConfig(_BETTER_BATTLE_RESULTS_CONFIG, onModSettingsChanged)
    STATE.initialized = True


def onModSettingsChanged(updatedConfig):
    setLanguage(updatedConfig.language)
    loadStrings()
    if updatedConfig.enabled is False:
        STATE.richTooltipEnabled = False
    else:
        STATE.richTooltipEnabled = updatedConfig.richTooltipEnabled
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\mod_betterBattleResults.pyc
