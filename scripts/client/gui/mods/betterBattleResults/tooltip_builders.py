# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\betterBattleResults\tooltip_builders.py
# Compiled at: 2023-12-31 00:48:38
from strings import *
from .classes import BuildTooltipData, CustomEfficiencyTooltipData
import json
from gui.impl import backport
from gui.Scaleform.genConsts.BATTLE_EFFICIENCY_TYPES import BATTLE_EFFICIENCY_TYPES
from gui.Scaleform.genConsts.TOOLTIPS_CONSTANTS import TOOLTIPS_CONSTANTS
from gui.shared.tooltips import contexts

def buildCritsTooltip(battleResults):
    if battleResults.critsCount == 0:
        return
    else:
        values = [
         backport.getIntegralFormat(battleResults.critsCount)]
        return _buildTooltip(values, BATTLE_EFFICIENCY_TYPES.CRITS)


def buildDamageAssistedTooltip(battleResults):
    totalAssist = battleResults.damageAssistedRadio + battleResults.damageAssistedTrack
    if totalAssist == 0:
        return
    else:
        values = [
         backport.getIntegralFormat(battleResults.damageAssistedRadio),
         backport.getIntegralFormat(battleResults.damageAssistedTrack),
         backport.getIntegralFormat(totalAssist)]
        return _buildTooltip(values, BATTLE_EFFICIENCY_TYPES.ASSIST)


def buildDamageBlockedTooltip(battleResults):
    if battleResults.damageBlockedByArmor == 0:
        return
    else:
        values = [
         backport.getIntegralFormat(battleResults.ricochets),
         backport.getIntegralFormat(battleResults.noDamageDirectHitsReceived),
         backport.getIntegralFormat(battleResults.damageBlockedByArmor)]
        return _buildTooltip(values, BATTLE_EFFICIENCY_TYPES.ARMOR)


def buildDamageDealtTooltip(battleResults):
    if battleResults.damageDealt == 0:
        return
    else:
        values = [
         backport.getIntegralFormat(battleResults.damageDealt),
         backport.getIntegralFormat(battleResults.piercings)]
        return _buildTooltip(values, BATTLE_EFFICIENCY_TYPES.DAMAGE)


def buildDestroyedTooltip(battleResults):
    if battleResults.killCount == 0:
        return
    else:
        values = [
         backport.getIntegralFormat(battleResults.killCount)]
        return _buildTooltip(values, BATTLE_EFFICIENCY_TYPES.DESTRUCTION)


def buildSpottedTooltip(battleResults):
    if battleResults.spotted == 0:
        return
    else:
        values = [
         backport.getIntegralFormat(battleResults.spotted)]
        return _buildTooltip(values, BATTLE_EFFICIENCY_TYPES.DETECTION)


def buildStunTooltip(battleResults):
    if battleResults.stunDuration == 0:
        return
    else:
        values = [
         backport.getIntegralFormat(battleResults.stunAssisted),
         backport.getIntegralFormat(battleResults.stunCount),
         backport.getFractionalFormat(battleResults.stunDuration)]
        return _buildTooltip(values, BATTLE_EFFICIENCY_TYPES.ASSIST_STUN)


_provider = CustomEfficiencyTooltipData(contexts.FinalStatisticContext())

def _buildTooltip(values, tooltipType):
    names = list(map(strings.get, battleEfficiencyTypeToLabels[tooltipType]))
    tooltipData = BuildTooltipData(tooltipType, values, names)
    data = _provider.buildToolTip(tooltipData)
    linkage = TOOLTIPS_CONSTANTS.FINAL_STSTS_UI
    serialized = json.dumps({'data': data, 'linkage': linkage})
    return '~' + serialized
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\betterBattleResults\tooltip_builders.pyc
