import json
from .classes import BattleResultsData
from .tooltip_builders import *
from gui.Scaleform.genConsts.TOOLTIPS_CONSTANTS import TOOLTIPS_CONSTANTS
from gui.battle_results.components.personal import _UNDEFINED_EFFICIENCY_VALUE
from gui.shared.formatters import numbers
from gui.shared.tooltips import advanced, builders, complex_formatters, contexts

def TotalEfficiencyDetailsHeader_setRecord(origFunc, self, result, reusable):
    origFunc(self, result, reusable)
    battleResults = BattleResultsData(result, reusable)
    self.kills = numbers.formatInt(battleResults.killCount, _UNDEFINED_EFFICIENCY_VALUE)
    self.damageAssistedTooltip = buildDamageAssistedTooltip(battleResults)
    self.damageBlockedTooltip = buildDamageBlockedTooltip(battleResults)
    self.damageDealtTooltip = buildDamageDealtTooltip(battleResults)
    self.damageAssistedStunTooltip = buildStunTooltip(battleResults)
    self.spottedTooltip = buildSpottedTooltip(battleResults)
    self.killsTooltip = buildDestroyedTooltip(battleResults)
    self.criticalDamagesTooltip = buildCritsTooltip(battleResults)


def ComplexBuilder_build(_, self, formatType, advanced_, *args, **kwargs):
    data, linkage = doFormatToolTip(args[0], formatType, self._linkage)
    if self.supportAdvanced(*args):
        disableAnim = self._getDisableAnimFlag()
        linkage = args[0]
        item = self.advancedComplexTooltips[linkage]
        if advanced_:
            buildTooltipData = [
             item, linkage]
            data = advanced.ComplexAdvanced(contexts.ToolTipContext(None)).buildToolTip(buildTooltipData)
            if not disableAnim:
                self._setDisableAnimFlag()
        else:
            data = advanced.ComplexTooltip(contexts.ToolTipContext(None), disableAnim).buildToolTip(data)
        linkage = TOOLTIPS_CONSTANTS.BLOCKS_DEFAULT_UI
    if data:
        return (self._provider, data, linkage)
    else:
        builders._logger.debug('Complex tooltip %s can not be shown: %r', formatType, args)
        return (None, None, None)


def doFormatToolTip(tooltipID, formatType, linkage):
    if not tooltipID:
        return ('', linkage)
    if tooltipID.startswith('#'):
        return (complex_formatters._doFormatToolTipFromKey(tooltipID, formatType), linkage)
    if tooltipID.startswith('~'):
        return extractToolTipFromSerializedData(tooltipID[1:])
    return (complex_formatters._doFormatToolTipFromText(tooltipID, formatType), linkage)


def extractToolTipFromSerializedData(text):
    obj = json.loads(text)
    return (obj['data'], obj['linkage'])
