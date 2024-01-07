from ..jakLibrary.lang import l10nOrNone
from gui.battle_results.components import style
from gui.Scaleform.genConsts.BATTLE_EFFICIENCY_TYPES import BATTLE_EFFICIENCY_TYPES
from gui.Scaleform.locale.BATTLE_RESULTS import BATTLE_RESULTS
from helpers import i18n

_L10N_PREFIX = 'betterBattleResults.tooltipOverride.'
_ASSIST_PART1 = 'assist.part1'
_ASSIST_PART2 = 'assist.part2'
_ASSIST_TOTAL = 'assist.total'
_BLOCKED_PART1 = 'blocked.part1'
_BLOCKED_PART2 = 'blocked.part2'
_BLOCKED_PART3 = 'blocked.part3'
_CRITS_TOTAL = 'crits.total'
_DAMAGE_PART1 = 'damage.part1'
_DAMAGE_PART2 = 'damage.part2'
_DESTROYED_TOTAL = 'destroyed.total'
_SPOTTED_TOTAL = 'spotted.total'
_STUN_PART1 = 'stun.part1'
_STUN_PART2 = 'stun.part2'
_STUN_PART3 = 'stun.part3'
strings = {}
battleEfficiencyTypeToLabels = {
    BATTLE_EFFICIENCY_TYPES.ARMOR: [
        _BLOCKED_PART1,
        _BLOCKED_PART2,
        _BLOCKED_PART3
    ], 
    BATTLE_EFFICIENCY_TYPES.CRITS: [
        _CRITS_TOTAL
    ], 
    BATTLE_EFFICIENCY_TYPES.DAMAGE: [
        _DAMAGE_PART1,
        _DAMAGE_PART2
    ], 
    BATTLE_EFFICIENCY_TYPES.DETECTION: [
        _SPOTTED_TOTAL
    ], 
    BATTLE_EFFICIENCY_TYPES.DESTRUCTION: [
       _DESTROYED_TOTAL
    ], 
    BATTLE_EFFICIENCY_TYPES.ASSIST: [
        _ASSIST_PART1,
        _ASSIST_PART2,
        _ASSIST_TOTAL
    ], 
    BATTLE_EFFICIENCY_TYPES.ASSIST_STUN: [
        _STUN_PART1,
        _STUN_PART2,
        _STUN_PART3
    ]
}

def loadStrings():
    tooltipParamsStyle = style.getTooltipParamsStyle()
    tooltipParamsStyleSeconds = style.getTooltipParamsStyle(BATTLE_RESULTS.COMMON_TOOLTIP_PARAMS_VAL_SECONDS)
    strings[_ASSIST_PART1] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ASSIST_PART1, vals=tooltipParamsStyle)
    strings[_ASSIST_PART2] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ASSIST_PART2, vals=tooltipParamsStyle)
    strings[_ASSIST_TOTAL] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ASSIST_TOTAL, vals=tooltipParamsStyle)
    strings[_BLOCKED_PART1] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ARMOR_PART1)
    strings[_BLOCKED_PART2] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ARMOR_PART2)
    strings[_BLOCKED_PART3] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_ARMOR_PART3, vals=tooltipParamsStyle)
    strings[_CRITS_TOTAL] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_CRITS_TOTAL)
    strings[_DAMAGE_PART1] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_DAMAGE_PART1, vals=tooltipParamsStyle)
    strings[_DAMAGE_PART2] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_DAMAGE_PART2)
    strings[_DESTROYED_TOTAL] = i18n.makeString(BATTLE_RESULTS.TEAM_STATS_LABELS_KILLED)
    strings[_SPOTTED_TOTAL] = i18n.makeString(BATTLE_RESULTS.TEAM_STATS_LABELS_SPOTTED)
    strings[_STUN_PART1] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_STUN_PART1, vals=tooltipParamsStyle)
    strings[_STUN_PART2] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_STUN_PART2)
    strings[_STUN_PART3] = i18n.makeString(BATTLE_RESULTS.COMMON_TOOLTIP_STUN_PART3, vals=tooltipParamsStyleSeconds)

    for key in strings:
        override = l10nOrNone(_L10N_PREFIX + key)
        if override is not None:
            if key in [_ASSIST_PART1, _ASSIST_PART2, _ASSIST_TOTAL, _BLOCKED_PART3, _DAMAGE_PART1, 
             _STUN_PART1]:
                strings[key] = override + ' ' + style.getTooltipParamsStyle()
            else:
                if key in [_STUN_PART3]:
                    strings[key] = override + ' ' + style.getTooltipParamsStyle(BATTLE_RESULTS.COMMON_TOOLTIP_PARAMS_VAL_SECONDS)
                else:
                    strings[key] = override
