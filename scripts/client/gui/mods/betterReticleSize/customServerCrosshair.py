from . import CUSTOM_ARCADE_GUN_MARKER_NAME, CUSTOM_SNIPER_GUN_MARKER_NAME, CUSTOM_DUAL_GUN_ARCADE_MARKER_NAME, CUSTOM_DUAL_GUN_SNIPER_MARKER_NAME, CUSTOM_SPG_MARKER_NAME
from .customCrosshairContainer import CustomCrosshairContainer
from aih_constants import GUN_MARKER_TYPE
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_components import GunMarkersComponents
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_components import DefaultGunMarkerComponent, SPGGunMarkerComponent
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _GunMarkersFactory
from gui.battle_control.battle_constants import CROSSHAIR_VIEW_ID as _VIEW_ID

class _CustomServerControlMarkersFactory(_GunMarkersFactory):

    def create(self, enableSpgStrategicReticle):
        if self._vehicleInfo.isSPG():
            markers = self._createSPGMarkers(enableSpgStrategicReticle)
        elif self._vehicleInfo.isDualGunVehicle():
            markers = self._createDualGunMarkers()
        else:
            markers = self._createDefaultMarkers()
        return markers

    def _createDualGunMarkers(self):
        return (
         self._createArcadeMarker(CUSTOM_DUAL_GUN_ARCADE_MARKER_NAME),
         self._createSniperMarker(CUSTOM_DUAL_GUN_SNIPER_MARKER_NAME))

    def _createDefaultMarkers(self):
        return (
         self._createArcadeMarker(CUSTOM_ARCADE_GUN_MARKER_NAME),
         self._createSniperMarker(CUSTOM_SNIPER_GUN_MARKER_NAME))

    def _createSPGMarkers(self, enableSpgStrategicReticle):
        if enableSpgStrategicReticle:
            return (
                self._createArcadeMarker(CUSTOM_ARCADE_GUN_MARKER_NAME),
                self._createSPGMarker(CUSTOM_SPG_MARKER_NAME)
            )
        else:
            return (
                self._createArcadeMarker(CUSTOM_ARCADE_GUN_MARKER_NAME),
            )

    def _createArcadeMarker(self, name):
        dataProvider = self._getMarkerDataProvider(GUN_MARKER_TYPE.SERVER)
        return self._createMarker(DefaultGunMarkerComponent, _VIEW_ID.ARCADE, GUN_MARKER_TYPE.SERVER, dataProvider, name)

    def _createSniperMarker(self, name):
        dataProvider = self._getMarkerDataProvider(GUN_MARKER_TYPE.SERVER)
        return self._createMarker(DefaultGunMarkerComponent, _VIEW_ID.SNIPER, GUN_MARKER_TYPE.SERVER, dataProvider, name)

    def _createSPGMarker(self, name):
        dataProvider = self._getSPGDataProvider(GUN_MARKER_TYPE.SERVER)
        return self._createMarker(SPGGunMarkerComponent, _VIEW_ID.STRATEGIC, GUN_MARKER_TYPE.SERVER, dataProvider, name)


def _createComponents(markersInfo, vehiclesInfo, enableSpgStrategicReticle):
    return GunMarkersComponents(_CustomServerControlMarkersFactory(markersInfo, vehiclesInfo, None).create(enableSpgStrategicReticle))


def _overrideComponents(components, markersInfo, vehiclesInfo, enableSpgStrategicReticle):
    return GunMarkersComponents(_CustomServerControlMarkersFactory(markersInfo, vehiclesInfo, components).create(enableSpgStrategicReticle))


def GetCustomServerCrosshair(customSettings, enableSpgStrategicReticle):
    return CustomCrosshairContainer(_createComponents, _overrideComponents, customSettings, enableSpgStrategicReticle)
