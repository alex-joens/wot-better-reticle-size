# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\betterBattleResults\classes.py
# Compiled at: 2023-12-31 00:47:18
from gui.battle_results.reusable.shared import VehicleSummarizeInfo
from gui.Scaleform.genConsts.BATTLE_EFFICIENCY_TYPES import BATTLE_EFFICIENCY_TYPES
from gui.Scaleform.locale.BATTLE_RESULTS import BATTLE_RESULTS
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.shared.tooltips import common, efficiency, formatters, TOOLTIP_TYPE

class BattleResultsData(object):

    def __init__(self, result, reusable):
        self.noDamageDirectHitsReceived = 0
        self.damageBlockedByArmor = 0
        self.ricochets = 0
        self.piercings = 0
        self.critsCount = 0
        self.damageDealt = 0
        self.damageAssistedRadio = 0
        self.damageAssistedTrack = 0
        self.killCount = 0
        self.spotted = 0
        self.stunAssisted = 0
        self.stunCount = 0
        self.stunDuration = 0
        for _, enemies in reusable.getPersonalDetailsIterator(result):
            for enemy in enemies:
                if type(enemy) is not VehicleSummarizeInfo:
                    continue
                self.noDamageDirectHitsReceived += enemy.noDamageDirectHitsReceived
                self.damageBlockedByArmor += enemy.damageBlockedByArmor
                self.ricochets += enemy.rickochetsReceived
                self.piercings += enemy.piercings
                self.damageDealt += enemy.damageDealt
                self.damageAssistedRadio += enemy.damageAssistedRadio
                self.damageAssistedTrack += enemy.damageAssistedTrack
                self.critsCount += enemy.critsInfo['critsCount']
                self.killCount += enemy.targetKills
                self.spotted += enemy.spotted
                self.stunAssisted += enemy.damageAssistedStun
                self.stunCount += enemy.stunNum
                self.stunDuration += enemy.stunDuration


class BuildTooltipData(object):

    def __init__(self, type, values, descriptions):
        self.type = type
        self._dict = {'values': values, 'discript': descriptions}

    def toDict(self):
        return self._dict


class CustomLinerItemPacker(efficiency.HeaderItemPacker):

    def pack(self, data):
        items = super(CustomLinerItemPacker, self).pack(data)
        values = data.get('values', None)
        discript = data.get('discript', None)
        if values is not None and discript is not None:
            packer = formatters.packTextParameterBlockData
            blocks = [ packer(value=values[i], name=discript[i]) for i in range(0, len(values)) ]
            blockToInsert = formatters.packBuildUpBlockData(blocks)
            items.append(blockToInsert)
        return items


class CustomArmorItemPacker(CustomLinerItemPacker):

    def __init__(self):
        super(CustomArmorItemPacker, self).__init__(BATTLE_RESULTS.COMMON_TOOLTIP_ARMOR_HEADER, RES_ICONS.MAPS_ICONS_LIBRARY_EFFICIENCY_48X48_ARMOR)


class CustomDamageItemPacker(CustomLinerItemPacker):

    def __init__(self):
        super(CustomDamageItemPacker, self).__init__(BATTLE_RESULTS.COMMON_TOOLTIP_DAMAGE_HEADER, RES_ICONS.MAPS_ICONS_LIBRARY_EFFICIENCY_48X48_DAMAGE)


class CustomDestructionItemPacker(CustomLinerItemPacker):

    def __init__(self):
        super(CustomDestructionItemPacker, self).__init__(BATTLE_RESULTS.COMMON_TOOLTIP_KILL_HEADER, RES_ICONS.MAPS_ICONS_LIBRARY_EFFICIENCY_48X48_DESTRUCTION)


class CustomSpottedItemPacker(CustomLinerItemPacker):

    def __init__(self):
        super(CustomSpottedItemPacker, self).__init__(BATTLE_RESULTS.COMMON_TOOLTIP_SPOTTED_HEADER, RES_ICONS.MAPS_ICONS_LIBRARY_EFFICIENCY_48X48_DETECTION)


class CustomCritsItemPacker(CustomLinerItemPacker):

    def __init__(self):
        super(CustomCritsItemPacker, self).__init__(BATTLE_RESULTS.COMMON_TOOLTIP_CRITS_HEADER, RES_ICONS.MAPS_ICONS_LIBRARY_EFFICIENCY_48X48_MODULE)


class CustomAssistItemPacker(CustomLinerItemPacker):

    def __init__(self):
        super(CustomAssistItemPacker, self).__init__(BATTLE_RESULTS.COMMON_TOOLTIP_ASSIST_HEADER, RES_ICONS.MAPS_ICONS_LIBRARY_EFFICIENCY_48X48_HELP)


class CustomStunItemPacker(CustomLinerItemPacker):

    def __init__(self):
        super(CustomStunItemPacker, self).__init__(BATTLE_RESULTS.COMMON_TOOLTIP_STUN_HEADER, RES_ICONS.MAPS_ICONS_LIBRARY_EFFICIENCY_48X48_STUN)


class CustomEfficiencyTooltipData(common.BlocksTooltipData):
    _packers = {BATTLE_EFFICIENCY_TYPES.ARMOR: CustomArmorItemPacker, BATTLE_EFFICIENCY_TYPES.DAMAGE: CustomDamageItemPacker, BATTLE_EFFICIENCY_TYPES.DESTRUCTION: CustomDestructionItemPacker, BATTLE_EFFICIENCY_TYPES.DETECTION: CustomSpottedItemPacker, BATTLE_EFFICIENCY_TYPES.ASSIST: CustomAssistItemPacker, 
       BATTLE_EFFICIENCY_TYPES.CRITS: CustomCritsItemPacker, 
       BATTLE_EFFICIENCY_TYPES.CAPTURE: efficiency.CaptureItemPacker, 
       BATTLE_EFFICIENCY_TYPES.DEFENCE: efficiency.DefenceItemPacker, 
       BATTLE_EFFICIENCY_TYPES.ASSIST_STUN: CustomStunItemPacker}

    def __init__(self, context):
        super(CustomEfficiencyTooltipData, self).__init__(context, TOOLTIP_TYPE.EFFICIENCY)
        self._setWidth(300)

    def _packBlocks(self, data):
        if data is not None and data.type in self._packers:
            return self._packers[data.type]().pack(data.toDict())
        else:
            return []
            return
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\betterBattleResults\classes.pyc
