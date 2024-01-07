# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (v2.7.18:8d21aa21f2, Apr 20 2020, 13:25:05) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\login_notification.py
# Compiled at: 2023-12-31 00:51:55
from .lang import l10n
from ..safeloader.constants import MOD_SAFELOAD_STATUS
from ..safeloader.decorators import ModLibrary
from ..safeloader.loader import addNotifySafeloadSuccessCallback, removeNotifySafeloadSuccessCallback
from gui import SystemMessages
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader, GuiGlobalSpaceID
_DEFAULT_LOADED_COLOR = '#008000'
_FAILED_TO_LOAD_COLOR = '#080000'

@ModLibrary
class LoginNotificationManager(object):

    def __init__(self):
        self._loginNotificationShown = False
        self._loginNotificationEnabled = False
        self._errorNotificationEnabled = True
        self._loadedMods = []
        self._modsThatFailedToLoad = []

    def init(self):
        dependency.instance(IAppLoader).onGUISpaceEntered += self.__onGUISpaceEntered
        addNotifySafeloadSuccessCallback(self.__safeloadSuccessCallback)

    def fini(self):
        dependency.instance(IAppLoader).onGUISpaceEntered -= self.__onGUISpaceEntered
        removeNotifySafeloadSuccessCallback(self.__safeloadSuccessCallback)

    def onModSettingsChanged(self, newSettings):
        if not newSettings.enabled:
            self._loginNotificationEnabled = False
            self._errorNotificationEnabled = False
        else:
            self._loginNotificationEnabled = newSettings.loginNotificationEnabled
            self._errorNotificationEnabled = newSettings.errorNotificationEnabled

    def __safeloadSuccessCallback(self, modInfo, status):
        modNameKey = getattr(modInfo, '__mod_name_key__')
        modColor = getattr(modInfo, '__mod_color__', _DEFAULT_LOADED_COLOR)
        if status == MOD_SAFELOAD_STATUS.Success:
            self.__addLoadedMod(modNameKey, modColor)
        elif status == MOD_SAFELOAD_STATUS.Failure:
            self.__addModThatFailedToLoad(modNameKey)

    def __addLoadedMod(self, modNameKey, modColor):
        if modNameKey == 'betterReticleSize.modname':
            self._loadedMods.append((modNameKey, modColor))

    def __addModThatFailedToLoad(self, modNameKey):
        self._modsThatFailedToLoad.append((modNameKey, _FAILED_TO_LOAD_COLOR))

    def __onGUISpaceEntered(self, spaceID):
        if spaceID == GuiGlobalSpaceID.LOGIN:
            self._loginNotificationShown = False
        elif spaceID == GuiGlobalSpaceID.LOBBY:
            if self._loginNotificationShown is False:
                self._loginNotificationShown = True
                if self._loginNotificationEnabled:
                    self.__notifyOnLoginThatModsAreRunning()
                if self._errorNotificationEnabled and len(self._modsThatFailedToLoad) > 0:
                    self.__notifyOnLoginIfModsFailedToLoad()

    def __notifyOnLoginThatModsAreRunning(self):
        msg = _joinMods(self._loadedMods, 'No mods were loaded', ' is active!', ' are active!')
        type = SystemMessages.SM_TYPE.GameGreeting
        SystemMessages.pushMessage(msg, type)

    def __notifyOnLoginIfModsFailedToLoad(self):
        msg = _joinMods(self._modsThatFailedToLoad, '', ' failed to load', ' failed to load')
        type = SystemMessages.SM_TYPE.Error
        SystemMessages.pushMessage(msg, type)


def _joinMods(modList, ifNone, suffixIfOne, suffixIfMultiple):
    if len(modList) == 0:
        return ifNone
    else:
        formattedModList = map((lambda modInfo: '<font color="' + modInfo[1] + '"><b>' + l10n(modInfo[0]) + '</b></font>'), modList)
        if len(formattedModList) == 1:
            return formattedModList[0] + suffixIfOne
        maybeOxford = ' and ' if len(formattedModList) == 2 else ', and '
        return (', ').join(formattedModList[:-1]) + maybeOxford + formattedModList[-1] + suffixIfMultiple
# okay decompiling C:\dev\wot-mods\betterReticleSize-src\scripts\client\gui\mods\jakLibrary\login_notification.pyc
