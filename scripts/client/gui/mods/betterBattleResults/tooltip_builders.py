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
