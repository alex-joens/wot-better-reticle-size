from account_helpers.settings_core.settings_constants import GRAPHICS, SPGAim
from debug_utils import LOG_WARNING
from gui.Scaleform.daapi.view.battle.shared.crosshair import CrosshairPanelContainer, settings
from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import _SETTINGS_KEYS, _SETTINGS_VIEWS, _SETTINGS_KEY_TO_VIEW_ID
from gui.Scaleform.daapi.view.external_components import ExternalFlashSettings
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.battle_control.battle_constants import CROSSHAIR_VIEW_ID
from gui.shared.utils.plugins import PluginsCollection
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

class CustomCrosshairContainer(CrosshairPanelContainer):

    def __init__(self, createMarkers, overrideMarkers, customSettings, enableSpgStrategicReticle):
        super(CrosshairPanelContainer, self).__init__(ExternalFlashSettings(BATTLE_VIEW_ALIASES.CROSSHAIR_PANEL, settings.CROSSHAIR_CONTAINER_SWF, settings.CROSSHAIR_ROOT_PATH, settings.CROSSHAIR_INIT_CALLBACK))
        self._CrosshairPanelContainer__plugins = PluginsCollection(self)
        self._CrosshairPanelContainer__plugins.addPlugins(self._getPlugins())
        self._CrosshairPanelContainer__gunMarkers = None
        self._CrosshairPanelContainer__viewID = CROSSHAIR_VIEW_ID.UNDEFINED
        self._CrosshairPanelContainer__zoomFactor = 0.0
        self._CrosshairPanelContainer__scale = 1.0
        self._CrosshairPanelContainer__width = 0.0
        self._CrosshairPanelContainer__height = 0.0
        self._CrosshairPanelContainer__distance = 0
        self._CrosshairPanelContainer__hasAmmo = True
        self._CrosshairPanelContainer__callbackDelayer = None
        self._CrosshairPanelContainer__isFaded = False
        self.createMarkers = createMarkers
        self.overrideMarkers = overrideMarkers
        self.customSettings = customSettings
        self.enableSpgStrategicReticle = enableSpgStrategicReticle
        return

    def createGunMarkers(self, markersInfo, vehicleInfo):
        if self._CrosshairPanelContainer__gunMarkers is not None:
            LOG_WARNING('Set of gun markers is already created.')
            return
        else:
            self._CrosshairPanelContainer__setGunMarkers(self.createMarkers(markersInfo, vehicleInfo, self.enableSpgStrategicReticle))
            return

    def invalidateGunMarkers(self, markersInfo, vehicleInfo):
        if self._CrosshairPanelContainer__gunMarkers is None:
            LOG_WARNING('Set of gun markers is not created')
            return
        else:
            newSet = self.overrideMarkers(self._CrosshairPanelContainer__gunMarkers, markersInfo, vehicleInfo, self.enableSpgStrategicReticle)
            self._CrosshairPanelContainer__clearGunMarkers()
            self._CrosshairPanelContainer__setGunMarkers(newSet)
            return

    def setSettings(self, _):
        self.as_setSettingsS(self.getSettingsVo())


    def getSettingsVo(self):
        settingsCore = dependency.instance(ISettingsCore)
        getter = settingsCore.getSetting
        data = {}
        for mode in _SETTINGS_KEYS:
            data[_SETTINGS_KEY_TO_VIEW_ID[mode]] = {
                'centerAlphaValue': 0,
                'centerType': 0, 
                'netAlphaValue': 0, 
                'netType': 0, 
                'reloaderAlphaValue': 0, 
                'conditionAlphaValue': 0, 
                'cassetteAlphaValue': 0, 
                'reloaderTimerAlphaValue': 0, 
                'zoomIndicatorAlphaValue': 0, 
                'gunTagAlpha': self.customSettings['gunTag'] / 100.0, 
                'gunTagType': self.customSettings['gunTagType'], 
                'mixingAlpha': self.customSettings['mixing'] / 100.0, 
                'mixingType': self.customSettings['mixingType']
            }

        for view in _SETTINGS_VIEWS:
            commonSettings = data.get(view, None)
            if commonSettings is None:
                commonSettings = {}
                data[view] = commonSettings
            commonSettings.update({
                'spgScaleWidgetEnabled': getter(SPGAim.SPG_SCALE_WIDGET), 
                'isColorBlind': settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
            })

        return data
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\betterReticleSize\customCrosshairContainer.pyc
