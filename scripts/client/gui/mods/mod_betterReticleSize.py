from .betterReticleSize import CUSTOM_GUN_MARKER_LINKAGES, DEFAULT_GUN_MARKER_LINKAGES
from .betterReticleSize.customServerCrosshair import GetCustomServerCrosshair
from .betterReticleSize.strings import CUSTOM_AIMING_CIRCLE_SHAPE_OPTIONS, CUSTOM_CROSSHAIR_SHAPE_OPTIONS
from .jakLibrary import JakLib
from .jakLibrary.config_parameters import ConfigParameter, ConfigSection, ParameterSettings
from .jakLibrary.config_validators import isBool, isNumber, isNumberBetween
from .safeloader.decorators import SafeInit, SafeOverride

import AvatarInputHandler, aih_constants, BattleReplay, BigWorld, Math, VehicleGunRotator
from aih_constants import CTRL_MODE_NAME, GUN_MARKER_FLAG, GUN_MARKER_TYPE
from constants import AIMING_MODE, ARENA_PERIOD, SERVER_TICK_LENGTH
from gui.Scaleform.daapi.view.battle.shared import SharedPage
from gui.Scaleform.daapi.view.battle.shared.crosshair import CrosshairPanelContainer, gm_factory
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCache, ISettingsCore

__mod_name_key__ = 'betterReticleSize.modname'
__mod_color__ = '#00A000'
DEFAULT_GUN_MARKER_MIN_SIZE = aih_constants.GUN_MARKER_MIN_SIZE
DEFAULT_RETICLE_SCALE_FACTOR = 1
CORRECT_RETICLE_SCALE_FACTOR = 1.71

class State:
    def __init__(self):
        self.reticleScaleFactor = DEFAULT_RETICLE_SCALE_FACTOR
        self.showClientAndServerReticle = False
        self.initialized = False
        self.reticleFlashObject = None
        self.primaryReticle = None
        self.customServerReticle = None
        self.customServerReticleSettings = {
            'gunTag': 0,
            'gunTagType': 0, 
            'mixing': 0, 
            'mixingType': 0
        }
        self.enableSpgStrategicReticle = False

STATE = State()

_RETICLE_CONFIG = ConfigSection(
    'reticle', [
        ConfigParameter(
            'gunMarkerMinimumSize',
            isNumberBetween(0, 32),
            0,
            ParameterSettings(
                1,
                {
                    'type': 'Slider',
                    'text': 'betterReticleSize.gunMarkerMinimumSize.title', 
                    'minimum': 0, 
                    'maximum': 32, 
                    'snapInterval': 1, 
                    'format': '{{value}}px', 
                    'tooltip': 'betterReticleSize.gunMarkerMinimumSize.description'
                }
            )
        ),
        ConfigParameter(
            'percentCorrection',
            isNumberBetween(0, 100), 
            100, 
            ParameterSettings(
                1, 
                {
                    'type': 'Slider', 
                    'text': 'betterReticleSize.percentCorrection.title', 
                    'minimum': 0, 
                    'maximum': 100, 
                    'snapInterval': 1, 
                    'format': '{{value}}%', 
                    'tooltip': 'betterReticleSize.percentCorrection.description'
                }
            )
        ),
        ConfigParameter(
            'showClientAndServerReticle_beta', 
            isBool, 
            False, 
            ParameterSettings(
                2, 
                {
                    'type': 'CheckBox', 
                    'text': 'betterReticleSize.showClientAndServerReticle.title', 
                    'tooltip': 'betterReticleSize.showClientAndServerReticle.description'
                }
            )
        ),
        ConfigParameter(
            'showServerSpgStrategicReticle', 
            isBool, 
            False, 
            ParameterSettings(
                2, 
                {
                    'type': 'CheckBox', 
                    'text': 'betterReticleSize.showServerSpgStrategicReticle.title', 
                    'tooltip': 'betterReticleSize.showServerSpgStrategicReticle.description'
                }
            )
        ),
        ConfigParameter(
            'serverReticleAimingCircleShape', 
            isNumber,
            0, 
            ParameterSettings(
                2, 
                {
                    'type': 'Dropdown', 
                    'text': 'betterReticleSize.serverReticleAimingCircleShape.title', 
                    'tooltip': 'betterReticleSize.serverReticleAimingCircleShape.description', 
                    'options': map((lambda option: {'label': option}), CUSTOM_AIMING_CIRCLE_SHAPE_OPTIONS)
                }
            )
        ),
        ConfigParameter(
            'serverReticleAimingCircleOpacity', 
            isNumberBetween(0, 100), 
            50, 
            ParameterSettings(
                2,
                {
                    'type': 'Slider', 
                    'text': 'betterReticleSize.serverReticleAimingCircleOpacity.title', 
                    'minimum': 0, 
                    'maximum': 100, 
                    'snapInterval': 1, 
                    'format': '{{value}}%', 
                    'tooltip': 'betterReticleSize.serverReticleAimingCircleOpacity.description'
                }
            )
        ),
        ConfigParameter(
            'serverReticleGunMarkerShape', 
            isNumber,
            0, 
            ParameterSettings(
                2, 
                {
                    'type': 'Dropdown', 
                    'text': 'betterReticleSize.serverReticleGunMarkerShape.title', 
                    'tooltip': 'betterReticleSize.serverReticleGunMarkerShape.description', 
                    'options': map((lambda option: {'label': option}), CUSTOM_CROSSHAIR_SHAPE_OPTIONS)
                }
            )
        ),
        ConfigParameter(
            'serverReticleGunMarkerOpacity', 
            isNumberBetween(0, 100), 
            50, 
            ParameterSettings(
                2, 
                {
                    'type': 'Slider', 
                    'text': 'betterReticleSize.serverReticleGunMarkerOpacity.title', 
                    'minimum': 0, 
                    'maximum': 100, 
                    'snapInterval': 1, 
                    'format': '{{value}}%', 
                    'tooltip': 'betterReticleSize.serverReticleGunMarkerOpacity.description'
                }
            )
        )
    ], __mod_name_key__, 'betterReticleSize', True
)

@SafeOverride(AvatarInputHandler.AvatarInputHandler, 'updateClientGunMarker')
def new_AvatarInputHandler_updateClientGunMarker(_, self, pos, direction, size, relaxTime, collData):
    if self.ctrlModeName in (CTRL_MODE_NAME.ARCADE, CTRL_MODE_NAME.STRATEGIC, CTRL_MODE_NAME.SNIPER):
        size = tuple(i / STATE.reticleScaleFactor for i in size)
    self.ctrl.updateGunMarker(GUN_MARKER_TYPE.CLIENT, pos, direction, size, relaxTime, collData)


@SafeOverride(AvatarInputHandler.AvatarInputHandler, 'updateServerGunMarker')
def new_AvatarInputHandler_updateServerGunMarker(_, self, pos, direction, size, relaxTime, collData):
    if self.ctrlModeName in (CTRL_MODE_NAME.ARCADE, CTRL_MODE_NAME.STRATEGIC, CTRL_MODE_NAME.SNIPER):
        size = tuple(i / STATE.reticleScaleFactor for i in size)
    self.ctrl.updateGunMarker(GUN_MARKER_TYPE.SERVER, pos, direction, size, relaxTime, collData)


@SafeOverride(AvatarInputHandler.AvatarInputHandler, 'updateDualAccGunMarker')
def new_AvatarInputHandler_updateDualAccGunMarker(origFunc, self, pos, direction, size, relaxTime, collData):
    if self.ctrlModeName in (CTRL_MODE_NAME.ARCADE, CTRL_MODE_NAME.STRATEGIC, CTRL_MODE_NAME.SNIPER):
        size = tuple(i / STATE.reticleScaleFactor for i in size)
    origFunc(self, pos, direction, size, relaxTime, collData)


@SafeOverride(SharedPage, '__init__')
def new_SharedPage_init(origFunc, self, components=None, external=None):
    origFunc(self, components, external)
    if STATE.showClientAndServerReticle is True:
        ensureServerAimingIsEnabled()
        for item in self._external:
            if isinstance(item, CrosshairPanelContainer):
                STATE.primaryReticle = item

        STATE.customServerReticle = GetCustomServerCrosshair(STATE.customServerReticleSettings, STATE.enableSpgStrategicReticle)
        self._external.append(STATE.customServerReticle)


def ensureServerAimingIsEnabled():
    settingsCache = dependency.instance(ISettingsCache)
    if not settingsCache.isSynced():
        settingsCache.onSyncCompleted += enableServerAimingViaCallback
    else:
        enableServerAiming()


def enableServerAiming():
    settingsCore = dependency.instance(ISettingsCore)
    if settingsCore.getSetting('useServerAim') is 0:
        settingsCore.isChangesConfirmed = True
        settingsCore.applySettings({'useServerAim': True})
        confirmators = settingsCore.applyStorages(True)
        settingsCore.confirmChanges(confirmators)
        settingsCore.clearStorages()


def enableServerAimingViaCallback():
    settingsCache = dependency.instance(ISettingsCache)
    settingsCache.onSyncCompleted -= enableServerAimingViaCallback
    enableServerAiming()


@SafeOverride(AvatarInputHandler.AvatarInputHandler, 'showClientGunMarkers')
def new_AvatarInputHandler_showClientGunMarkers(origFunc, self, isShown):
    if STATE.showClientAndServerReticle is True:
        self.ctrl.setGunMarkerFlag(isShown, GUN_MARKER_FLAG.CLIENT_MODE_ENABLED)
        self.ctrl.setGunMarkerFlag(isShown, GUN_MARKER_FLAG.SERVER_MODE_ENABLED)
    else:
        origFunc(self, isShown)


@SafeOverride(AvatarInputHandler.AvatarInputHandler, 'showServerGunMarker')
def new_AvatarInputHandler_showServerGunMarker(origFunc, self, isShown):
    if STATE.showClientAndServerReticle is True:
        if not BattleReplay.isPlaying():
            BattleReplay.g_replayCtrl.setUseServerAim(False)
            self.ctrl.setGunMarkerFlag(isShown, GUN_MARKER_FLAG.SERVER_MODE_ENABLED)
    else:
        origFunc(self, isShown)


@SafeOverride(AvatarInputHandler.AvatarInputHandler, '_AvatarInputHandler__onArenaStarted')
def new_AvatarInputHandler_onArenaStarted(origFunc, self, period, *args):
    if STATE.showClientAndServerReticle is True:
        isBattle = period == ARENA_PERIOD.BATTLE
        self._AvatarInputHandler__isArenaStarted = isBattle
        self.ctrl.setGunMarkerFlag(isBattle, GUN_MARKER_FLAG.CONTROL_ENABLED)
        self.showServerGunMarker(isBattle)
        self.showClientGunMarkers(isBattle)
    else:
        origFunc(self, period, *args)


@SafeOverride(gm_factory._ControlMarkersFactory, '_getMarkerType')
def new_ControlMarkersFactory_getMarkerType(origFunc, self):
    if STATE.showClientAndServerReticle is True:
        return GUN_MARKER_TYPE.CLIENT
    else:
        return origFunc(self)


@SafeOverride(VehicleGunRotator.VehicleGunRotator, 'clientMode', (lambda self: self._VehicleGunRotator__clientMode))
def new_VehicleGunRotator_clientMode_setter(origProp, self, value):
    if STATE.showClientAndServerReticle is True:
        if self.clientMode == value:
            return
        self._VehicleGunRotator__clientMode = value
        if not self._VehicleGunRotator__isStarted:
            return
        if self.clientMode:
            self._VehicleGunRotator__time = BigWorld.time()
            self.stopTrackingOnServer()
    else:
        origProp.fset(self, value)


@SafeOverride(VehicleGunRotator.VehicleGunRotator, 'setShotPosition')
def new_VehicleGunRotator_setShotPosition(origFunc, self, vehicleID, shotPos, shotVec, dispersionAngle, forceValueRefresh=False):
    if STATE.showClientAndServerReticle is True:
        if self.clientMode and not self.showServerMarker and not forceValueRefresh:
            return
        else:
            dispersionAngles = self._VehicleGunRotator__dispersionAngles[:]
            dispersionAngles[0] = dispersionAngle
            if not self.clientMode and VehicleGunRotator.VehicleGunRotator.USE_LOCK_PREDICTION:
                lockEnabled = BigWorld.player().inputHandler.getAimingMode(AIMING_MODE.TARGET_LOCK)
                if lockEnabled:
                    predictedTargetPos = self.predictLockedTargetShotPoint()
                    if predictedTargetPos is None:
                        return
                    dirToTarget = predictedTargetPos - shotPos
                    dirToTarget.normalise()
                    shotDir = Math.Vector3(shotVec)
                    shotDir.normalise()
                    if shotDir.dot(dirToTarget) > 0.0:
                        return
            markerPosition = self._VehicleGunRotator__getGunMarkerPosition(shotPos, shotVec, dispersionAngles)
            mPos, mDir, mSize, mIdealSize, _, _, collData = markerPosition
            if self.clientMode and self.showServerMarker:
                self._avatar.inputHandler.updateServerGunMarker(mPos, mDir, (mSize, mIdealSize), SERVER_TICK_LENGTH, collData)
            return

    else:
        origFunc(self, vehicleID, shotPos, shotVec, dispersionAngle, forceValueRefresh)
    return


@SafeOverride(VehicleGunRotator.VehicleGunRotator, 'updateRotationAndGunMarker')
def new_VehicleGunRotator_updateRotationAndGunMarker(origFunc, self, shotPoint, timeDiff):
    origFunc(self, shotPoint, timeDiff)
    if STATE.showClientAndServerReticle and not self.clientMode:
        shotPos, shotVec = self.getCurShotPosition()
        markerPosition = self._VehicleGunRotator__getGunMarkerPosition(shotPos, shotVec, self._VehicleGunRotator__dispersionAngles)
        mPos, mDir, mSize, mIdealSize, _, _, collData = markerPosition
        relaxTime = 0.001
        if not (BattleReplay.g_replayCtrl.isPlaying and BattleReplay.g_replayCtrl.isUpdateGunOnTimeWarp):
            relaxTime = self._VehicleGunRotator__ROTATION_TICK_LENGTH
        self._avatar.inputHandler.updateServerGunMarker(mPos, mDir, (mSize, mIdealSize), relaxTime, collData)


@SafeInit
def init():
    if STATE.initialized is False:
        JakLib.initializeModWithConfig(_RETICLE_CONFIG, onModSettingsChanged)
    STATE.initialized = True


def onModSettingsChanged(updatedConfig):
    if updatedConfig.enabled is False and STATE.initialized is True:
        aih_constants.GUN_MARKER_MIN_SIZE = DEFAULT_GUN_MARKER_MIN_SIZE
        STATE.reticleScaleFactor = DEFAULT_RETICLE_SCALE_FACTOR
        STATE.showClientAndServerReticle = False
    else:
        aih_constants.GUN_MARKER_MIN_SIZE = updatedConfig.gunMarkerMinimumSize
        correctionFactor = updatedConfig.percentCorrection / 100
        STATE.reticleScaleFactor = CORRECT_RETICLE_SCALE_FACTOR * correctionFactor + (DEFAULT_RETICLE_SCALE_FACTOR - correctionFactor)
        STATE.showClientAndServerReticle = updatedConfig.showClientAndServerReticle_beta
    if STATE.showClientAndServerReticle is True:
        gm_factory._GUN_MARKER_LINKAGES = CUSTOM_GUN_MARKER_LINKAGES
    else:
        gm_factory._GUN_MARKER_LINKAGES = DEFAULT_GUN_MARKER_LINKAGES
    STATE.customServerReticleSettings['gunTag'] = updatedConfig.serverReticleGunMarkerOpacity
    STATE.customServerReticleSettings['gunTagType'] = updatedConfig.serverReticleGunMarkerShape
    STATE.customServerReticleSettings['mixing'] = updatedConfig.serverReticleAimingCircleOpacity
    STATE.customServerReticleSettings['mixingType'] = updatedConfig.serverReticleAimingCircleShape
    STATE.enableSpgStrategicReticle = updatedConfig.showServerSpgStrategicReticle


def fini():
    STATE.initialized = False
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\mod_betterReticleSize.pyc
